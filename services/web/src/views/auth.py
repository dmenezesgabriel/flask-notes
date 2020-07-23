from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.urls import url_parse
from sqlalchemy.exc import DataError
from src.models.models import db, User
from src.forms.forms import Register, Login
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = Register()
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password).decode('utf-8')
        email = request.form['email']
        error = None

        user = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()

        if user is not None:
            error = 'User {} is already registered.'.format(username)
        elif user_email is not None:
            error = 'Email {} is already registered.'.format(email)

        if not form.validate_on_submit():
            error = 'Invalid form params'
            flash(error, 'danger')
            return render_template('auth/register.html', form=form)

        if error is None:
            try:
                new_user = User(
                    username=username,
                    password=password_hash,
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
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
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

        if user is None or not check_password_hash(user.password, password):
            error = 'Invalid username or password.'

        if error is None:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('notes.index')
            return redirect(next_page)

        flash(error, 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('notes.index'))
