from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired, length, EqualTo, Email, ValidationError)
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from src.models.models import User


class Register(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), length(min=3, max=20)])
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), length(min=3, max=20)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    # When you add any methods that match the pattern validate_<field_name>,
    # WTForms takes those as custom validators and invokes them in addition
    # to the stock validators.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class Login(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField(
        'Password', validators=[DataRequired(), length(min=3, max=20)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class Note(FlaskForm):
    title = StringField(
        'Title', validators=[DataRequired(), length(min=1, max=80)])
    body = CKEditorField('Body', widget=TextArea(), validators=[DataRequired(),
                         length(min=1, max=5000)])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), length(min=3, max=20)])
    email = StringField(
        'Email', validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password', validators=[DataRequired(), length(min=3, max=20)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
    submit = SubmitField('Request Password Reset')
