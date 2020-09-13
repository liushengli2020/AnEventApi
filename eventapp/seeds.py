from eventapp.models import db
import os
import click
from flask.cli import with_appcontext
from flask import current_app
from flask_fixtures import load_fixtures_from_file


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()


def init_db():
    click.echo("Initialized the database.")
    db.create_all()
    seed_files = ['users.yaml', 'events.yaml', 'event_signups.yaml', 'admins.yaml', 'email_senders.yaml']
    default_fixtures_dir = os.path.join(current_app.root_path, 'fixtures')
    fixtures_dirs = [default_fixtures_dir]
    for filename in seed_files:
        load_fixtures_from_file(db, filename, fixtures_dirs)


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.cli.add_command(init_db_command)


