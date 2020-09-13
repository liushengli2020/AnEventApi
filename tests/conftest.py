import os

import pytest

from eventapp import create_app
from eventapp.seeds import init_db



@pytest.fixture
def app():
    os.environ['FLASK_ENV'] = 'testing'
    # create the app with common test config
    app = create_app()

    # create the database and load test data
    with app.app_context():
        init_db()

    yield app

    # close and remove the temporary database



@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


