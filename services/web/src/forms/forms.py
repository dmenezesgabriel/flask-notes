from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, EqualTo
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class Register(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), length(min=3, max=20)])
    email = StringField(
        'Email', validators=[DataRequired()]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), length(min=3, max=20)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


class Login(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField(
        'Password', validators=[DataRequired(), length(min=3, max=20)])
    submit = SubmitField('Submit')


class Note(FlaskForm):
    title = StringField(
        'Title', validators=[DataRequired(), length(min=1, max=80)])
    body = CKEditorField('Body', widget=TextArea(), validators=[DataRequired(),
                         length(min=1, max=5000)])
    submit = SubmitField('Submit')
