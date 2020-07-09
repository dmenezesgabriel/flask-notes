import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import DataError
from src.models.models import db, User
from src.forms.forms import Register, Login


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = Register()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        user = User.query.filter_by(username=username).first()

        if user is not None:
            error = 'User {} is already registered.'.format(username)

        if not form.validate_on_submit():
            error = 'Invalid form params'
            flash(error, 'danger')
            return render_template('auth/register.html', form=form)

        if error is None:
            try:
                new_user = User(
                    username=username,
                    password=generate_password_hash(password),
                    email=email
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))
                message = 'registered with success'
                flash(message, 'success')
            except DataError:
                db.session.rollback()
                error = 'Number of characters exceeds maximum'
                flash(error, 'danger')

        flash(error, 'danger')

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = Login()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if not form.validate_on_submit():
            error = 'Invalid form params'
            flash(error, 'danger')
            return render_template('auth/login.html', form=form)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error, 'danger')

    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
