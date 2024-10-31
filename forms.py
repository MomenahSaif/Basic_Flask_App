from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
import re

class SignupForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=4, max=25), 
                    Regexp('^[A-Za-z0-9]*$', message='Username must contain only letters and numbers.')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), 
        Regexp('^[0-9]*$', message='Phone number must contain only digits.')])
    password = PasswordField('Password', 
        validators=[DataRequired(), Length(min=6), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Signup')

    # Custom validator to check if the username already exists
    def validate_username(self, username):
        from app import get_user_by_username  # Importing the function to check username
        user = get_user_by_username(username.data)
        if user:
            raise ValidationError('Username is already taken.')

    # Custom validator to check if the email already exists
    def validate_email(self, email):
        from app import get_user_by_email  # Importing the function to check email
        user = get_user_by_email(email.data)
        if user:
            raise ValidationError('Email is already registered.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
