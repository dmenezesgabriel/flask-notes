import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Application default configuration
    """

    # App
    # Flask and some of its extensions use the value of the secret key as a
    # cryptographic key, useful to generate signatures or tokens.
    # The Flask-WTF extension uses it to protect web forms against a
    # nasty attack called Cross-Site Request Forgery or
    # CSRF (pronounced "seasurf").
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/src/static"
    MEDIA_FOLDER = f"{os.getenv('APP_FOLDER')}/src/media"
    NOTES_PER_PAGE = 5

    # Extensions
    # CK editor
    CKEDITOR_HEIGHT = 400

    # Babel
    LANGUAGES = ['en', 'pt']

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
    # Signal the application every time a change is about to be made
    # in the database.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email server
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_ADMIN = os.getenv('MAIL_ADMIN')
