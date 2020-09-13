import os
from flask import request
from flask import Blueprint
from flask_restful import Api, Resource
from eventapp.models import db, Event, Admin, User, EventSignup
from eventapp.routes.response import SUCCESS, FAILURE
from flask import jsonify, make_response
from eventapp.services.signature_util import generate_signature
from eventapp.services.sendmail import send_notif_mail
from eventapp.errors import SignatureError, UserNotFountError, EventNotFountError, AlreadySignupError

mod = Blueprint('signup', __name__)
api = Api(mod)

is_sendmail = os.environ['FLASK_ENV'].lower() == 'production'

class SignupsEndPoint(Resource):
    def post(self, event_id):
        resp = {'status': SUCCESS}
        http_code = 201
        try:
            admin_id = request.headers.get('admin_id')
            if admin_id:
                self.signup_event_by_admin(admin_id, event_id)

            else:
                self.signup_event(event_id)
        except UserNotFountError:
            http_code = 404
            resp['status'] = FAILURE
            error = {'code': 200404, 'message': 'user not found'}
            resp['data'] = error
        except EventNotFountError:
            http_code = 404
            resp['status'] = FAILURE
            error = {'code': 200404, 'message': 'event not found'}
            resp['data'] = error
        except SignatureError:
            http_code = 401
            resp['status'] = FAILURE
            error = {'code': 200401, 'message': 'signature check failed'}
            resp['data'] = error
        except AlreadySignupError:
            http_code = 409
            resp['status'] = FAILURE
            error = {'code': 200409, 'message': 'user already signed up'}
            resp['data'] = error
        except Exception as err:
            print(f'EventsEndPoint error happened {err}')
            raise err
        resp_str = jsonify(resp)
        return make_response(resp_str, http_code)

    def signup_event_by_admin(self, admin_id, event_id):
        try:
            admin_signature = request.headers.get('admin_signature')
            admin_user = Admin.query.filter_by(user_id=admin_id).first()
            if not admin_user:
                raise UserNotFountError

            expected_signature = generate_signature(admin_user.admin_key, request.path)
            if expected_signature != admin_signature:
                raise SignatureError

            user_id = request.json['user_id']
            if user_id is not None:
                self.signup_with_id(user_id, event_id)
            else:
                raise ValueError("Missing parameter")
        except Exception as err:
            print(f'EventsEndPoint signup_event_by_admin error happened {err}')
            raise err

    def signup_with_id(self, user_id, event_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise UserNotFountError
            event = Event.query.filter_by(id=event_id).first()
            if not event:
                raise EventNotFountError
            exist_signup = EventSignup.query \
                .filter_by(event_id=event_id) \
                .filter_by(user_id=user_id).first()
            if exist_signup:
                raise AlreadySignupError
            signup = EventSignup(event_id, user_id)
            db.session.add(signup)
            db.session.commit()
            if is_sendmail:
                send_notif_mail(user_id, event_id, False)
        except Exception as err:
            print(f'EventsEndPoint signup_with_id error happened {err}')
            raise err
        return True

    def signup_event(self, event_id):
        try:
            signature = request.headers.get('signature')
            user_id = request.json['user_id']
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise UserNotFountError
            expected_signature = generate_signature(user.password, request.path)
            if expected_signature != signature:
                raise SignatureError
            self.signup_with_id(user_id, event_id)
        except Exception as err:
            print(f'EventsEndPoint signup_event error happened {err}')
            raise err

    def get(self, event_id):
        resp = {'status': SUCCESS}
        http_code = 200
        try:
            admin_signature = request.headers.get('admin_signature')
            admin_id = request.headers.get('admin_id')
            admin_user = Admin.query.filter_by(user_id=admin_id).first()
            if not admin_user:
                raise UserNotFountError

            expected_signature = generate_signature(admin_user.admin_key, request.path)
            if expected_signature != admin_signature:
                raise SignatureError
            signups = EventSignup.query.filter_by(event_id=event_id).all()
            users = []
            for signup in signups:
                user = User.query.filter_by(id=signup.user_id).first()
                if user:
                    users.append({'id':user.id, 'name': user.name, 'email': user.email})
            resp['data'] = users
        except UserNotFountError:
            http_code = 404
            resp['status'] = FAILURE
            error = {'code': 200404, 'message': 'user not found'}
            resp['data'] = error
        except SignatureError:
            http_code = 401
            resp['status'] = FAILURE
            error = {'code': 200401, 'message': 'signature check failed'}
            resp['data'] = error
        except Exception as err:
            print(f'EventsEndPoint error happened {err}')
            raise err
        resp_str = jsonify(resp)
        return make_response(resp_str, http_code)


class SignupEndPoint(Resource):
    def delete(self, event_id, user_id):
        resp = {'status': SUCCESS}
        http_code = 200
        try:
            admin_id = request.headers.get('admin_id')
            if admin_id:
                self.quit_event_by_admin(admin_id, event_id, user_id)
            else:
                self.quit_event(event_id, user_id)
        except UserNotFountError:
            http_code = 404
            resp['status'] = FAILURE
            error = {'code': 200404, 'message': 'user not found'}
            resp['data'] = error
        except EventNotFountError:
            http_code = 404
            resp['status'] = FAILURE
            error = {'code': 200404, 'message': 'event not found'}
            resp['data'] = error
        except SignatureError:
            http_code = 401
            resp['status'] = FAILURE
            error = {'code': 200401, 'message': 'signature check failed'}
            resp['data'] = error
        except Exception as err:
            print(f'EventsEndPoint error happened {err}')
            raise err
        resp_str = jsonify(resp)
        return make_response(resp_str, http_code)

    def quit_event_by_admin(self, admin_id, event_id, user_id):
        try:
            admin_signature = request.headers.get('admin_signature')
            admin_user = Admin.query.filter_by(user_id=admin_id).first()
            if not admin_user:
                raise UserNotFountError

            expected_signature = generate_signature(admin_user.admin_key, request.path)
            if expected_signature != admin_signature:
                raise SignatureError
            self.quit_with_id(event_id, user_id)
        except Exception as err:
            print(f'EventsEndPoint signup_event_by_admin error happened {err}')
            raise err

    def quit_with_id(self, event_id, user_id):
        try:
            signup = EventSignup.query.filter_by(event_id=event_id).filter_by(user_id=user_id).first()
            if not signup:
                raise EventNotFountError
            db.session.delete(signup)
            db.session.commit()
            if is_sendmail:
                send_notif_mail(user_id, event_id, True)
        except Exception as err:
            print(f'EventsEndPoint signup_with_id error happened {err}')
            raise err
        return True

    def quit_event(self, event_id, user_id):
        try:
            signature = request.headers.get('signature')
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise UserNotFountError
            expected_signature = generate_signature(user.password, request.path)
            if expected_signature != signature:
                raise SignatureError
            self.quit_with_id(event_id, user_id)
        except Exception as err:
            print(f'EventsEndPoint signup_event error happened {err}')
            raise err


api.add_resource(SignupsEndPoint, '/event/<event_id>/users')
api.add_resource(SignupEndPoint, '/event/<event_id>/user/<user_id>')
