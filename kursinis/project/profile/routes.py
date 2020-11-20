from flask import Blueprint,render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from project.profile.forms import UpdateInfo
from project import db
from project.models import User, Item_Type
from werkzeug.security import generate_password_hash


profile = Blueprint('profile',__name__, template_folder='templates',static_folder='static',static_url_path='/profile/static')

@profile.context_processor
def inject_types():
	types = Item_Type.query.all()
	return dict(types=types)

@profile.route('/profile',methods=['POST','GET'])
@login_required
def profile_page():
	form = UpdateInfo()
	if request.method == 'POST':
		if form.validate_on_submit():

			email = form.email.data
			username = form.username.data
			password = form.password.data

			current_user.password = generate_password_hash(password,method='sha256')

			current_user.info.first_name = form.first_name.data
			current_user.info.last_name = form.last_name.data
			current_user.info.phone_number = form.phone_number.data 
			current_user.info.address = form.address.data

			existing_name = User.query.filter_by(username=username).first()

			if existing_name is None:
				current_user.username = form.username.data
			else:
				flash('Username is taken!','danger')

			existing_email = User.query.filter_by(email=email).first()
			if existing_email is None:
				current_user.email = form.email.data
			else:
				flash('Email address already exists!','danger')

			db.session.commit()
			return redirect(url_for('profile.profile_page'))
	
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.first_name.data = current_user.info.first_name
		form.last_name.data = current_user.info.last_name
		form.phone_number.data = current_user.info.phone_number
		form.address.data = current_user.info.address

	return render_template('profile.html',title='Profile page',form=form)
