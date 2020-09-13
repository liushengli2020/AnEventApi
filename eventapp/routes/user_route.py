from flask import request
from flask import Blueprint
from flask_restful import Api, Resource
from eventapp.models import db, User,Admin
from eventapp.routes.response import SUCCESS, FAILURE
from flask import jsonify, make_response

mod = Blueprint('user', __name__)
api = Api(mod)


class UsersEndPoint(Resource):
    def post(self):
        resp = {'status': SUCCESS}
        http_code = 201
        try:
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']
            email_existed_user = User.query.filter_by(email=email).first()
            name_existed_user = User.query.filter_by(name=name).first()
            if email_existed_user or name_existed_user:
                resp['status'] = FAILURE
                err_msg = email_existed_user and 'email address already exists' or 'name already exists'
                error = {'code': 100409, 'message': err_msg}
                resp['data'] = error
                http_code = 409
            else:
                user = User(name, email, password)
                db.session.add(user)
                db.session.commit()
        except Exception as err:
            print(f'UsersEndPoint error happened {err}')
            raise err
        return make_response(jsonify(resp), http_code)


class UserEndPoint(Resource):
    def get(self, email):
        resp = {'status': SUCCESS}
        http_code = 200
        try:
            password = request.headers.get('password')
            user = User.query.filter_by(email=email).filter_by(password=password).first()
            admin_key = None
            if user and user.admin and len(user.admin):
                admin_key = user.admin[0].admin_key
            if user is None:
                err_msg = 'wrong email address/wrong password'
                print(f' {err_msg}')
                resp['status'] = FAILURE
                error = {'code': 110401, 'message': 'wrong email address/wrong password'}
                resp['data'] = error
                http_code = 401
            else:
                resp['data'] = {'user_id': user.id, 'admin_key': admin_key}
        except Exception as err:
            print(f' UserEndPoint error happened {err}')
            raise err

        return make_response(jsonify(resp), http_code)


api.add_resource(UsersEndPoint, '/users')
api.add_resource(UserEndPoint, '/user/email/<email>')
