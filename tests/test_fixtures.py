import unittest
from eventapp import create_app
from eventapp.models import db, User, Event, EventSignup, Admin, EmailSender


from flask_fixtures import FixturesMixin
import os
# Configure the app with the testing configuration
app = create_app()


# Make sure to inherit from the FixturesMixin class
class TestFixtures(unittest.TestCase, FixturesMixin):

    # Specify the fixtures file(s) you want to load.
    # Change the list below to ['authors.yaml'] if you created your fixtures
    # file using YAML instead of JSON.
    fixtures =  ['users.yaml', 'events.yaml', 'event_signups.yaml', 'admins.yaml', 'email_senders.yaml']

    # Specify the Flask app and db we want to use for this set of tests
    app = app
    db = db
    # Your tests go here

    def test_users(self):
        users = User.query.all()
        assert len(users) == User.query.count() == 4
        assert users[0].admin is not None
        assert len(users[0].events) == 1
        assert len(users[1].events) == 1

    def test_events(self):
        events = Event.query.all()
        assert len(events) == Event.query.count() == 2
        assert len(events[0].users) == 1
        assert len(events[1].users) == 1

    def test_event_signups(self):
        event_signups = EventSignup.query.all()
        assert len(event_signups) == EventSignup.query.count() == 2

    def test_admins(self):
        admins = Admin.query.all()
        assert len(admins) == Admin.query.count() == 1

    def test_email_senders(self):
        email_senders = EmailSender.query.all()
        assert len(email_senders) == EmailSender.query.count() == 1