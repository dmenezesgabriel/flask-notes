from flask.cli import FlaskGroup
from src import create_app
from src.models.models import db, TimestampMixin, User, Note
from flask_bcrypt import generate_password_hash


# Configure flask CLI tool to run and manage from the command line
cli = FlaskGroup(create_app=create_app)


@cli.command('create_db')
def create_db():
    print(db)
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user_a = User(username="teste", email="teste@teste.com")
    user_a.set_password("teste")
    user_b = User(username="teste2", email="teste2@teste.com")
    user_b.set_password("teste2")
    db.session.add(user_a)
    db.session.add(user_b)
    db.session.commit()


if __name__ == "__main__":
    cli()
