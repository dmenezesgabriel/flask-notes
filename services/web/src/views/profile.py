from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_babel import _
from src.models.models import db, User
from flask_login import login_required, current_user
from src.forms.forms import EditProfileForm


bp = Blueprint('user', __name__)


@bp.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('user/profile.html', title=_('Profile'), user=user)


@bp.route('/edit_profile', methods=('GET', 'POST'))
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(_('Your changes have been saved.'), 'success')
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('user/edit_profile.html', title='Edit Profile',
                           form=form)
