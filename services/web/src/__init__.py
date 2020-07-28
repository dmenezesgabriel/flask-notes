import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, request
from src.notes.routes import bp as notes_bp
from src.errors.handlers import bp as error_bp
from src.auth.routes import bp as auth_bp
from src.profile.routes import bp as profile_bp
from src.extensions import babel, db, login_manager, mail, migrate, moment
from flask_ckeditor import CKEditor
from config import Config


_blueprints = (auth_bp, notes_bp, profile_bp, error_bp)


def init_blueprints(app):
    for bp in _blueprints:
        app.register_blueprint(bp)


def create_app(config_class=Config):
    """
    Application Factory funcion which makes possibleto instantiate different
    app environments

    Returns
    ----------------
    Flask app object
    """
    # Create and configure the app
    app = Flask(__name__)

    app.config.from_object(config_class)
    # Init app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    # WSGIWYG editor
    CKEditor(app)
    # Register blueprints
    init_blueprints(app)

    # Logging config
    if not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/flask-notes.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            """%(asctime)s %(levelname)s: %(message)s """
            """[in %(pathname)s:%(lineno)d]"""))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask Notes startup')

    return app


@babel.localeselector
def get_locale():
    """
    Accept-Language header provides a a list of preferred languages,
    each with a weight.

    ex: Accept-Language: da, en-gb;q=0.8, en;q=0.7
    """

    return request.accept_languages.best_match(app.config['LANGUAGES'])