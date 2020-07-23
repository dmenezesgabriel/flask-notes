from flask import Flask, jsonify
from src.views import auth, notes, user, errors
from src.models.models import db, migrate
from flask_ckeditor import CKEditor
# from src.routes import setup_routes
from src.helpers.login import login_manager
from config import Config


_blueprints = (auth.bp, notes.bp, user.bp, errors.bp)


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
    login_manager.login_message_category = "info"
    # WSGIWYG editor
    CKEditor(app)
    # Register blueprints
    init_blueprints(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return jsonify(hello="world")

    return app
