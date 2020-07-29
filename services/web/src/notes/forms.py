from flask import request
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class NoteForm(FlaskForm):
    title = StringField(
        _l('Title'), validators=[DataRequired(), length(min=1, max=80)])
    body = CKEditorField(
        _l('Body'),
        widget=TextArea(),
        validators=[DataRequired(), length(min=1, max=5000)]
    )
    submit = SubmitField(_l('Submit'))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
