from wtforms.validators import Required, Length, EqualTo, ValidationError, Optional
from wtforms import PasswordField, StringField, BooleanField, SubmitField, FileField
from flask_wtf import FlaskForm

from flask_login import current_user

from . import Parent


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[Required(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):

    fullname = StringField('Fullname', validators=[Required()])
    username = StringField('Username', validators=[Required(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[Required(), Length(min=8), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm password')
    address = StringField('Address', validators=[Required()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        if Parent.query.filter_by(username=username.data).first():
            raise ValidationError('That username is already taken, please choose a different one.')
        if ' ' in username.data:
            raise ValidationError('Your username cannot contain spaces.')


class UpdateForm(FlaskForm):

    fullname = StringField('Fullname', validators=[Required()])
    username = StringField('Username', validators=[Required(), Length(min=2, max=30)])
    address = StringField('Address', validators=[Required()])
    picture = FileField('Profile picture', validators=[Optional])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data and Parent.query.filter_by(username=username.data).first():
            raise ValidationError('That username is already taken, please choose a different one.')
        if ' ' in username.data:
            raise ValidationError('Your username cannot contain spaces.')
