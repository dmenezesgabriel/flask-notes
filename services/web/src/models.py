from datetime import datetime
from time import time
import hashlib
import jwt
from flask import current_app
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
import redis
import rq
from src.extensions import login_manager, db
from search import add_to_index, remove_from_index, query_index


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(UserMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(20), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    notes = db.relationship('Note', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)

    def launch_task(self, name, description, *args, **kwargs):
        """Submit the task to RQ along with adding it to the database"""
        rq_job = current_app.task.queue.enqueue(
            'src.tasks.' + name, self.id, *args, **kwargs)
        task = Task(
            id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        """Get all tasks in progress"""
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        """Get only one task in progress"""
        return Task.query.filter_by(
            name=name, user=self, complete=False).first()


class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(
            cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class Note(SearchableMixin, TimestampMixin, db.Model):
    __searchable__ = ['title', 'body']

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return f'<Note {self.body}>'


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
