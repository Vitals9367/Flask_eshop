from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from flask_login import current_user
from project.models import User

class UpdateInfo(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=2, max=20),InputRequired()])
    email = StringField('Email',
                        validators=[Email(),InputRequired()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password'),InputRequired()])
    first_name = StringField('First Name',validators=[InputRequired()])
    last_name = StringField('Last Name',validators=[InputRequired()])
    phone_number = StringField('Phone number',validators=[InputRequired()])
    address = StringField('Address',validators=[InputRequired()])
    submit = SubmitField('Save',validators=[InputRequired()])
