from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_wtf.recaptcha import RecaptchaField
from wtforms import HiddenField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import Roles, User
from .utils import Unique


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired()
    ])
    birth_number = StringField('Birth Number', validators=[
        DataRequired()
    ])
    address = StringField('Address', validators=[
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    phone = StringField('Phone Number', validators=[
    ])
    card_number = StringField('Card Number', validators=[
        DataRequired()
    ])
    account_number = StringField('Account Number', validators=[
        DataRequired()
    ])
    recaptcha = RecaptchaField()
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    password = StringField('Password', validators=[
        DataRequired()
    ])

    role = SelectField('Role', choices=[(Roles.ADMIN.value, 'Admin'),
                                        (Roles.ACCOUNTANT.value, 'Accountant'),
                                        (Roles.SECRETARY.value, 'Secretary')])
    submit = SubmitField('Create User')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is already used. Please choose a different one.')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email address is already used. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Login')


# noinspection PyMethodMayBeStatic
class UpdateAccountForm(FlaskForm):
    """Form for users to allow them update their account"""

    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])
    ])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is already used. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email address is already used. Please choose a different one.')


class UpdateUserForm(FlaskForm):
    """Form for administrator to update other users accounts"""

    id = IntegerField(widget=HiddenField())
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Unique(User, User.username, message='The username is already used. Please choose a different one.')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Unique(User, User.email, message='The email address is already used. Please choose a different one.')
    ])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])
    ])
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Request Password Reset')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Reset Password')
