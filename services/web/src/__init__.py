import os
from flask import Flask, jsonify
from src.views import auth, notes
from src.models.models import db


def create_app(test_config=None):
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
    app = Flask(__name__, instance_relative_config=True)
    # Deafault config
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_PATH=os.path.join(app.instance_path, 'database-prod.db')
    )

    if test_config is None:
        # load the instance config, if exists, when not testing
        # Overrides the default configuration
        app.config.from_object('src.config.Config')
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Init app
    db.init_app(app)
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return jsonify(hello="world")

    app.register_blueprint(auth.bp)
    app.register_blueprint(notes.bp)
    app.add_url_rule('/', endpoint='index')

    return app