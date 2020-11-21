from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from flask_login import current_user
from project.models import User, Sizes

class AddToCart(FlaskForm):
    submit = SubmitField('Add To Cart',validators=[InputRequired()])
    size = SelectField(u'Size', choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('2XL', '2XL')])
    amount = SelectField(u'Amount', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])

class WriteReview(FlaskForm):
	submit = SubmitField('Write',validators=[InputRequired()])
	rating = SelectField(u'Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
	content = TextAreaField('Comment', validators=[DataRequired()])