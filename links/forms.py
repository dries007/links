from flask_wtf import Form
from wtforms import PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms_alchemy import model_form_factory

from links import db
from links.models import User, Token, Link


BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(cls):
        return db.session


class LoginForm(ModelForm):
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log in')


class ProfileEditForm(ModelForm):
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Save')

    class Meta:
        model = User
        only = ['name', 'email']


class ChangePasswordForm(ModelForm):
    current = PasswordField('Current Password', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=6)])
    confirm = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Change password')


class AddTokenForm(ModelForm):
    submit = SubmitField('Add')

    class Meta:
        model = Token
        only = ['identity']


class AddLinkForm(ModelForm):
    submit = SubmitField('Add')

    class Meta:
        model = Link
        only = ['url']
