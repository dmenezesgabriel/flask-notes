from rq import get_current_job
from src.extensions import db
from src.models import Task
from src import create_app


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
