import json
import sys
import time
from flask import render_template
from rq import get_current_job
from flask_babel import _
from src.extensions import db
from src.models import Task
from src import create_app
from src.models import User, Note
from src.helpers.email import send_email


app = create_app()
app.app_context().push()


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification(
            'task_progress',
            {'task_id': job.get_id(), 'progress': progress}
        )

        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_notes(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_notes = user.notes.count()
        for note in user.notes.order_by(Note.created_at.asc()):
            data.append({'body': note.body,
                         'created_at': note.created_at.isoformat()})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_notes)

        # Send email with data to user
        # Babel translation on templates conflicts with app.context() on
        # g.locale() due to request
        send_email(
            '[Flask Notes] Your blog notes',
            sender=app.config['MAIL_ADMIN'],
            recipients=[user.email],
            text_body=render_template('email/export_notes.txt', user=user),
            html_body=render_template('email/export_notes.html', user=user),
            attachments=[
                ('notes.json', 'application/json',
                 json.dumps({'notes': data}, indent=4))
            ],
            sync=True
        )
    except Exception:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
        _set_task_progress(100)
