from flask import Blueprint, render_template
from src.models.models import db


bp = Blueprint('errors', __name__)


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500
