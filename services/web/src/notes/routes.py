from flask import (
    Blueprint, redirect, render_template, request, url_for, current_app, g)
from werkzeug.exceptions import abort
from flask_login import login_required, current_user
from flask_babel import _
from src.models import db, Note
from src.notes.forms import NoteForm


bp = Blueprint('notes', __name__)


@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    notes = (
        current_user.notes
        .order_by(Note.created_at.desc())
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
    form = NoteForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_note = Note(
                title=form.title.data,
                body=form.body.data,
                author_id=current_user.id
            )
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('notes.index'))

    return render_template('notes/create.html', title=_('New Note'), form=form)


def get_note(id, check_author=True):
    note = current_user.notes.filter_by(id=id).first()
    if note is None:
        abort(404, _("Note id {} doesn't exist.".format(id)))
    return note


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    note = get_note(id)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        db.session.commit()
        return redirect(url_for('notes.index'))
    elif request.method == 'GET':
        form.title.data = note.title
        form.body.data = note.body

    return render_template(
        'notes/update.html', title=_('Edit Note'), note=note, form=form)


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    note = get_note(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes.index'))


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('notes.index'))
    page = request.args.get('page', 1, type=int)
    notes_search, total = Note.search(g.search_form.q.data, page,
                                      current_app.config['NOTES_PER_PAGE'])
    # Filter only user notes
    user_notes = notes_search.filter_by(author_id=current_user.id)
    # Pagination
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['NOTES_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), notes=user_notes,
                           next_url=next_url, prev_url=prev_url)
