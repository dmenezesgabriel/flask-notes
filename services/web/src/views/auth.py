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
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(
                user.password, form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('notes.index')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('notes.index'))
