from datetime import datetime
from time import time
import hashlib
import jwt
from flask import current_app
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from src.extensions import login_manager, db


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
    password_hash = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    notes = db.relationship('Note', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
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


class Note(TimestampMixin, db.Model):
    __tablename__ = "Notes"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return f'<Post {self.body}>'
