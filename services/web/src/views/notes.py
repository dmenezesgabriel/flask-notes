from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from sqlalchemy.exc import DataError
from src.views.auth import login_required
from src.models.models import db, User, Note


bp = Blueprint('notes', __name__)


@bp.route('/')
@login_required
def index():
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
             .filter_by(author_id=g.user.id)
             .order_by(Note.created_at.desc())
             .join(User, User.id == Note.author_id).all()

    )
    return render_template('notes/index.html', notes=notes)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            try:
                new_note = Note(title=title, body=body, author_id=g.user.id)
                db.session.add(new_note)
                db.session.commit()
                return redirect(url_for('notes.index'))
            except DataError:
                db.session.rollback()
                error = 'Number of characters exceeds maximum'
                flash(error)

    return render_template('notes/create.html')


def get_note(id, check_author=True):
    note = (
             Note.query
             .filter_by(id=id)
             .join(User, Note.author_id == User.id)
             .first()
    )

    if note is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and note.author_id != g.user.id:
        abort(403)

    return note


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    note = get_note(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            try:
                note.title = title
                note.body = body
                db.session.commit()
                return redirect(url_for('notes.index'))
            except DataError:
                db.session.rollback()
                error = 'Number of characters exceeds maximum'
                flash(error)

    return render_template('notes/update.html', note=note)


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    note = get_note(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes.index'))
