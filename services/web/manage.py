from flask.cli import FlaskGroup
from src import create_app
from src.models.models import db, TimestampMixin, User, Note


# Configure flask CLI tool to run and manage from the command line
cli = FlaskGroup(create_app=create_app)


@cli.command('create_db')
def create_db():
    print(db)
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
