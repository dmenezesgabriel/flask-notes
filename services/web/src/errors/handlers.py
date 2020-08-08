from flask import Blueprint, render_template, request
from flask_babel import _
from src.models import db
from src.api.errors import error_response as api_error_response


bp = Blueprint('errors', __name__)


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def page_not_found(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template(
        'error/404.html', title=_('Page Not Found 404')), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template(
        'error/500.html', title=_('Internal Server Error')), 500
