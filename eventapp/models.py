from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()


@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id: int
    name: str
    email: str
    password: str
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)
    events = db.relationship('EventSignup', backref='user', lazy=True)
    admin = db.relationship('Admin', backref='users', lazy=True)
    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


@dataclass
class Event(db.Model):
    __tablename__ = 'events'
    id: int
    name: str
    location: str
    start_time: str
    end_time: str
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    location = db.Column(db.String(50), unique=False)
    start_time = db.Column(db.String(120), unique=False)
    end_time = db.Column(db.String(120), unique=False)
    users = db.relationship('EventSignup', backref='events', lazy=True)

    def __init__(self, name=None, location=None, start_time=None, end_time=None):
        self.name = name
        self.location = location
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<event %r>' % self.name


@dataclass
class EventSignup(db.Model):
    __tablename__ = 'event_signups'
    __table_args__ = (
        db.UniqueConstraint('event_id', 'user_id', name='unique_event_user'),
    )
    id: int
    event_id: int
    user_id: int
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, event_id=None, user_id=None):
        self.event_id = event_id
        self.user_id = user_id

    def __repr__(self):
        return '<EventSignup %r>' % self.id


@dataclass
class Admin(db.Model):
    __tablename__ = 'admins'
    id: int
    user_id: int
    admin_key: str
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_key = db.Column(db.String(60), unique=True)

    def __init__(self, user_id=None, admin_key=None):
        self.user_id = user_id
        self.admin_key = admin_key

    def __repr__(self):
        return '<Admin %r>' % self.id


@dataclass
class EmailSender(db.Model):
    __tablename__ = 'email_senders'
    id: int
    smtp_server: str
    port: int
    sender_email: int
    password: str
    id = db.Column(db.Integer, primary_key=True)
    smtp_server = db.Column(db.String(60), unique=False)
    port = db.Column(db.Integer, unique=False)
    sender_email = db.Column(db.String(120), unique=False)
    password = db.Column(db.String(60), unique=False)

    def __init__(self, smtp_server=None, port=None, sender_email=None, password=None):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password

    def __repr__(self):
        return '<EmailSender %r>' % self.id
