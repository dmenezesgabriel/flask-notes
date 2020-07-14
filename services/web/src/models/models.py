from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from src.helpers.login import login_manager


db = SQLAlchemy()
migrate = Migrate()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(20), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    notes = db.relationship('Note', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Note(TimestampMixin, db.Model):
    __tablename__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return f'<Post {self.body}>'
