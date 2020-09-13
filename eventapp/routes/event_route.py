from flask import request
from flask import Blueprint
from flask_restful import Api, Resource
from eventapp.models import db, Event, Admin, User, EventSignup
from eventapp.routes.response import SUCCESS, FAILURE
from flask import jsonify, make_response
from eventapp.services.signature_util import generate_signature
from eventapp.errors import SignatureError, UserNotFountError, EventNotFountError, AlreadySignupError

mod = Blueprint('event', __name__)
api = Api(mod)


class EventsEndPoint(Resource):
    def get(self):
        resp = {'status': SUCCESS}
        http_code = 200
        try:
            events = Event.query.all()
            resp['data'] = events
        except Exception as err:
            print(f'EventsEndPoint error happened {err}')
            raise err
        resp_str = jsonify(resp)
        return make_response(resp_str, http_code)


api.add_resource(EventsEndPoint, '/events')
