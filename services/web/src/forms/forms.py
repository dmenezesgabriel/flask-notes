from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, EqualTo


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


# class Note(FlaskForm):
#     title
#     body