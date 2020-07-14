from flask import render_template
from src.models.models import db


def page_not_found(error):
    return render_template('error/404.html'), 404


def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500


def setup_error_handler(app):
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)
