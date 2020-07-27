from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, jsonify, request, g
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from src.views import auth, notes, profile, errors
from src.models.models import db, migrate
from flask_ckeditor import CKEditor
from flask_login import current_user
from src.helpers.login import login_manager
from src.helpers.email import mail
from config import Config


_blueprints = (auth.bp, notes.bp, profile.bp, errors.bp)
moment = Moment()
babel = Babel()


def init_blueprints(app):
    for bp in _blueprints:
        app.register_blueprint(bp)


def create_app():
    """
    Application Factory funcion which makes possibleto instantiate different
    app environments

    Parameters
    ----------------
    :test_config:

    Returns
    ----------------
    Flask app object
    """
    # Create and configure the app
    app = Flask(__name__)

    app.config.from_object(Config)
    # Init app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = _l('Please log in to access this page.')
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    # WSGIWYG editor
    CKEditor(app)
    # Register blueprints
    init_blueprints(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return jsonify(hello="world")

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()
            g.locale = str(get_locale())

    # Logging config
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/flask-notes.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask Notes startup')

    @babel.localeselector
    def get_locale():
        """
        Accept-Language header provides a a list of preferred languages,
        each with a weight.

        ex: Accept-Language: da, en-gb;q=0.8, en;q=0.7
        """

        return request.accept_languages.best_match(app.config['LANGUAGES'])

    return app
