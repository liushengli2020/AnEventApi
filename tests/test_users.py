from eventapp.services.signature_util import generate_signature
from eventapp.models import db, Event, Admin, User, EventSignup


def test_create_user(client, app):
    # test that user will be created
    path = '/api/v1/users'
    user_password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    user_name = 'testuser3'
    user_email = 'testuser3@sample.invalid'
    resp = client.post(path,
                       json={'name': user_name, 'email': user_email,'password': user_password})
    assert resp.status_code == 201
    assert resp.json['status'] == 'success'

    # test that the user was inserted into the database
    with app.app_context():
        user = User.query.filter_by(name=user_name).first()
        assert user

def test_create_user_fail(client, app):
    # test that name already exists
    path = '/api/v1/users'
    user_password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    user_name = 'testuser2'
    user_email = 'testuser3@sample.invalid'
    resp = client.post(path,
                       json={'name': user_name, 'email': user_email, 'password': user_password})
    assert resp.status_code == 409
    assert resp.json['status'] == 'failure'

    # test that email address already exists
    path = '/api/v1/users'
    user_password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    user_name = 'testuser3'
    user_email = 'testuser2@sample.invalid'
    resp = client.post(path,
                       json={'name': user_name, 'email': user_email, 'password': user_password})
    assert resp.status_code == 409
    assert resp.json['status'] == 'failure'

def test_get_user(client, app):
    # test that user will be got by email
    user_password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    user_email = 'testuser2@sample.invalid'
    path = '/api/v1/user/email/'+user_email
    resp = client.get(path, headers={'password': user_password})
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'

def test_get_user_fail(client, app):
    # test that user will not be got by wrong email
    user_password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    user_email = 'testuser3@sample.invalid'
    path = '/api/v1/user/email/'+user_email
    resp = client.get(path, headers={'password': user_password})
    assert resp.status_code == 401
    assert resp.json['status'] == 'failure'

    # test that user will not be got by wrong email
    user_password = '123'
    user_email = 'testuser2@sample.invalid'
    path = '/api/v1/user/email/' + user_email
    resp = client.get(path, headers={'password': user_password})
    assert resp.status_code == 401
    assert resp.json['status'] == 'failure'