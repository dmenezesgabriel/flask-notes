from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import DataError
from src.models.models import db, User
from flask_login import login_required, current_user
from src.forms.forms import EditProfileForm


bp = Blueprint('user', __name__)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.username == username:
        return render_template('user/user.html', user=user)
    else:
        return render_template('error/404.html'), 404


@bp.route('/user/<username>/update', methods=('GET', 'POST'))
@login_required
def update(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm(obj=user)

    if current_user.username != username:
        return render_template('error/404.html'), 404

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        error = None

        user.username = username
        user.email = email
        try:
            if not form.validate_on_submit():
                error = 'Invalid form params'
                flash(error, 'danger')
                return render_template(
                    'user/update.html', user=user, form=form)

            db.session.commit()
            return redirect(
                url_for('user.user', username=current_user.username))
        except DataError:
            db.session.rollback()
            error = 'Number of characters exceeds maximum'
            flash(error, 'danger')

    return render_template('user/update.html', user=user, form=form)
