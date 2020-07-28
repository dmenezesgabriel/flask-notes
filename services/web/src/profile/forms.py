from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired, length, Email, ValidationError)
from src.models import User


class EditProfileForm(FlaskForm):
    username = StringField(
        _l('Username'), validators=[DataRequired(), length(min=3, max=20)])
    email = StringField(
        _l('Email'), validators=[DataRequired(), Email()]
    )
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))
