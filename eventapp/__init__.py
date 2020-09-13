import os
from flask import Flask
from eventapp.models import db
from eventapp.routes.user_route import mod as user_mod
from eventapp.routes.event_route import mod as event_mod
from eventapp.routes.signup_event import mod as signup_mod
from eventapp.seeds import init_app as seeds_init_app
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    if os.environ['FLASK_ENV'].lower() == 'production':
        app.config.from_object('eventapp.config.ProductionConfig')
    elif os.environ['FLASK_ENV'] == 'development':
        app.config.from_object('eventapp.config.DevConfig')
    else:
        app.config.from_object('eventapp.config.TestConfig')
    db.init_app(app)
    seeds_init_app(app)

    app.register_blueprint(user_mod, url_prefix='/api/v1')
    app.register_blueprint(event_mod, url_prefix='/api/v1')
    app.register_blueprint(signup_mod, url_prefix='/api/v1')
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app
