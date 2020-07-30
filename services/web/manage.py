import os
import click
from flask import current_app
from flask.cli import FlaskGroup
from rq import Connection, Worker
from src import create_app
from src.models import db, TimestampMixin, User, Note


# Configure flask CLI tool to run and manage from the command line
cli = FlaskGroup(create_app=create_app)


@cli.command('create_db')
def create_db():
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


@cli.command('run_worker')
def run_worker():
    redis_connection = current_app.redis
    with Connection(redis_connection):
        worker = Worker(current_app.task_queue)
        worker.work()


@cli.group()
def translate():
    """Translation and location commands"""
    pass


@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('Extract command failed')
    if os.system('pybabel update -i messages.pot -d src/translations'):
        raise RuntimeError('Update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d src/translations'):
        raise RuntimeError('compile command failed')


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d src/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


if __name__ == "__main__":
    cli()
