from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from flask_babel import _
from src.models import db, User
from flask_login import login_required, current_user
from src.profile.forms import EditProfileForm
from src.models import Notification


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
    return render_template('user/edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@bp.route('/export_notes')
@login_required
def export_notes():
    if current_user.get_task_in_progress('export_notes'):
        flash(_('An export task is currently in progress'), 'info')
    else:
        current_user.launch_task('export_notes', _('Exporting notes...'))
        db.session.commit()
    return redirect(url_for('user.profile', username=current_user.username))
