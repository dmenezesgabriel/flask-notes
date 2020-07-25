from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.urls import url_parse
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
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                password=(
                    generate_password_hash(form.password.data).decode('utf-8')
                ),
                email=form.email.data
            )
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('auth.login'))

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
