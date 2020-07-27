from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from sqlalchemy.exc import DataError
from flask_login import login_required, current_user
from flask_babel import _
from src.models.models import db, User, Note
from src.forms import forms


bp = Blueprint('notes', __name__)


@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    notes = (
        Note.query
        .with_entities(
            Note.id,
            Note.created_at,
            Note.updated_at,
            Note.title,
            Note.body,
            Note.author_id,
            User.id.label('user_id'),
            User.username
        )
        .filter_by(author_id=current_user.id)
        .order_by(Note.created_at.desc())
        .join(User, User.id == Note.author_id)
        .paginate(page, current_app.config['NOTES_PER_PAGE'], False)

    )
    # Pagination
    next_url = (
        url_for('notes.index', page=notes.next_num)
        if notes.has_next else None
    )
    prev_url = (
        url_for('notes.index', page=notes.prev_num)
        if notes.has_prev else None
    )

    return render_template(
        'notes/index.html',
        title=_('Notes'),
        notes=notes.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = forms.Note()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not form.validate_on_submit():
            flash(_('Invalid form params'), 'danger')
            return render_template('notes/create.html', form=form)

        else:
            try:
                new_note = Note(
                    title=title, body=body, author_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                return redirect(url_for('notes.index'))
            except DataError:
                db.session.rollback()
                flash(_('Number of characters exceeds maximum'), 'danger')

    return render_template('notes/create.html', title=_('New Note'), form=form)


def get_note(id, check_author=True):
    note = (
        Note.query
        .filter_by(id=id)
        .join(User, Note.author_id == User.id)
        .first()
    )

    if note is None:
        abort(404, _("Note id {} doesn't exist.".format(id)))

    if check_author and note.author_id != current_user.id:
        abort(403)

    return note


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    note = get_note(id)
    form = forms.Note(obj=note)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        note.title = title
        note.body = body
        try:
            if not form.validate_on_submit():
                flash(_('Invalid form params'), 'danger')
                return render_template(
                    'notes/update.html', note=note, form=form)

            db.session.commit()
            return redirect(url_for('notes.index'))
        except DataError:
            db.session.rollback()
            flash(_('Number of characters exceeds maximum'), 'danger')

    return render_template(
        'notes/update.html',
        title=_('Edit Note'),
        note=note, form=form
    )


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    note = get_note(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes.index'))
