from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from src.models.models import db, User
from src.forms.forms import (
    Register, Login, ResetPasswordRequestForm, ResetPasswordForm)
from src.helpers.email import send_password_reset_email


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = Register()
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
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
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        # When a user that is not logged in accesses a view function protected
        # with the @login_required decorator, the decorator is going to
        # redirect to the login page, but it is going to include some
        # extra information in this redirect, so that the application can then
        # return the user to the previous age which he was trying yo access
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('notes.index')
        return redirect(next_page)

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('notes.index'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists before send email
        if user:
            send_password_reset_email(user)
        # Flash message will appears even if the user exists so that clients
        # cannot use this form to figure out if a given user
        # is a member or not.
        flash('Check your email for the instructions to reset your password',
              'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('notes.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
