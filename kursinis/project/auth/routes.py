from flask import Blueprint,render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from project.models import User, User_Info, Cart
from project.auth.forms import RegistrationForm,LoginForm

auth = Blueprint('auth',__name__, template_folder='templates',static_folder='static',static_url_path='/auth/static')

@auth.route('/login',methods=['POST','GET'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			email = form.email.data
			remember = True if request.form.get('remember') else False
			user = User.query.filter_by(email=email).first()

			if user and check_password_hash(user.password,form.password.data):
				login_user(user, remember=remember)
				next_page = request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('main.index'))
			else:
				flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Sing In', form=form)

@auth.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegistrationForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			email = form.email.data
			name = form.username.data
			password = form.password.data

			existing_name = User.query.filter_by(username=name).first()

			if existing_name is None:
				existing_email = User.query.filter_by(email=email).first()
				if existing_email is None:
					new_user = User(email=email, username=name,password=generate_password_hash
					(password,method='sha256'))
					new_user.info = User_Info()
					new_user.cart = Cart()
					db.session.add(new_user)
					db.session.commit()
					login_user(new_user)
					return redirect(url_for('main.index'))
				else:
					flash('Email address already exists!','danger')
			else:
				flash('Username is taken!','danger')

	return render_template('register.html', title='Sing Up', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))
