from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# validators return true/false
class SignupForm(Form):
	first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")]) 
	last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
	email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password."), Length(min = 6, message="Password must be 6 characters or more.")])
	submit = SubmitField('Sign Up', validators=[DataRequired()])
	
class LoginForm(Form):
	email = StringField("Email", validators=[DataRequired("Please enter your email address."), Email("Please enter a valid email address.")])
	
	password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
	submit = SubmitField('Sign In')
	
class AddressForm(Form):
	address = StringField('Address', validators=[DataRequired("Please enter an address.")])
	submit = SubmitField('Search')