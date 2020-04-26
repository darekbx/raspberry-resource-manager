from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
#from flask_wtf.file import FileField, FileAllowed, FileRequired

from app.models import User

class LoginForm(FlaskForm):
	name = StringField('Login', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	submit = SubmitField('Log In')

	def validate(self):
		initial_validation = super(LoginForm, self).validate()
		if not initial_validation:
			return False
		user = User.query.filter_by(name=self.name.data).first()
		if not user:
			self.name.errors.append('Unknown name')
			return False
		if not user.verify_password(self.password.data):
			self.password.errors.append('Invalid password')
			return False
		return True

class RegisterForm(FlaskForm):
	name = StringField('Login', validators = [DataRequired()])
	password = PasswordField('Password', validators = [
		DataRequired(),	
        EqualTo('password_repeat', message='Passwords must match'),
		Length(min=8, max=128, message='Password is too short')
	])
	password_repeat = PasswordField('Repeat password', validators = [DataRequired()])
	submit = SubmitField('Register')

	def validate(self):
		initial_validation = super(RegisterForm, self).validate()
		if not initial_validation:
			return False
		user = User.query.filter_by(name=self.name.data).first()
		if user:
			self.name.errors.append('User already exists')
			return False
		return True

# class UploadForm(Form):

#     validators = [
#         FileRequired(message='There was no file!'),
#         FileAllowed(['txt'], message='Must be a txt file!')
#     ]

#     input_file = FileField('', validators=validators)
#     submit = SubmitField(label="Upload")