from eventapp.services.signature_util import generate_signature
from eventapp.models import db, Event, Admin, User, EventSignup

def test_signup_event(client, app):
    # test that signup will be created
    key = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    path = '/api/v1/event/1/users'
    signature = generate_signature(key, path)
    resp = client.post(path,
                       json={"user_id": 3},
                       headers={'signature': signature})
    assert resp.status_code == 201
    assert resp.json['status'] == 'success'

    # test that the signup was inserted into the database
    with app.app_context():
        signup = EventSignup.query.filter_by(user_id=3).filter_by(event_id=1).first()
        assert signup

    # test that signup will be created by admin
    admin_key = '4e7fe767-bd2b-4a34-acdf-17985d65830c'
    admin_id = 1
    admin_signature = generate_signature(admin_key, path)
    resp = client.post(path,
                       json={"user_id": 4},
                       headers={'admin_signature': admin_signature, 'admin_id': admin_id})
    assert resp.status_code == 201
    assert resp.json['status'] == 'success'

    # test that the signup was inserted into the database
    with app.app_context():
        signup = EventSignup.query.filter_by(user_id=4).filter_by(event_id=1).first()
        assert signup


def test_signup_event_fail(client, app):
    # test that signature check will fail
    key = '123'
    path = '/api/v1/event/1/users'
    signature = generate_signature(key, path)
    resp = client.post(path,
                       json={"user_id": 3},
                       headers={'signature': signature})
    assert resp.status_code == 401
    assert resp.json['status'] == 'failure'

    # test that user will not be found
    signature = generate_signature(key, path)
    resp = client.post(path,
                       json={"user_id": 5},
                       headers={'signature': signature})
    assert resp.status_code == 404
    assert resp.json['status'] == 'failure'

    # test that event will not be found
    path = '/api/v1/event/3/users'
    key = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    signature = generate_signature(key, path)
    resp = client.post(path,
                       json={"user_id": 3},
                       headers={'signature': signature})
    assert resp.status_code == 404
    assert resp.json['status'] == 'failure'

    # test that signup already exists
    path = '/api/v1/event/1/users'
    signature = generate_signature(key, path)
    resp = client.post(path,
                       json={"user_id": 1},
                       headers={'signature': signature})
    assert resp.status_code == 409
    assert resp.json['status'] == 'failure'

    # test that admin_signature check will fail
    path = '/api/v1/event/1/users'
    admin_key = '123'
    admin_id = 1
    admin_signature = generate_signature(admin_key, path)
    resp = client.post(path,
                       json={"user_id": 4},
                       headers={'admin_signature': admin_signature, 'admin_id': admin_id})
    assert resp.status_code == 401
    assert resp.json['status'] == 'failure'


def test_get_signups_of_event(client, app):
    # test that signups of the event will be got by admin
    path = '/api/v1/event/1/users'
    admin_key = '4e7fe767-bd2b-4a34-acdf-17985d65830c'
    admin_id = 1
    admin_signature = generate_signature(admin_key, path)
    resp = client.get(path, headers={'admin_signature': admin_signature, 'admin_id': admin_id})
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'


def test_quit_event(client, app):
    # test that signup will be remove
    key = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    path = '/api/v1/event/1/user/1'
    signature = generate_signature(key, path)
    resp = client.delete(path,
                         headers={'signature': signature})
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'

    # test that the signup was inserted into the database
    with app.app_context():
        signup = EventSignup.query.filter_by(user_id=1).filter_by(event_id=1).first()
        assert not signup

    # test that signup will be removed by admin
    path = '/api/v1/event/2/user/2'
    admin_key = '4e7fe767-bd2b-4a34-acdf-17985d65830c'
    admin_id = 1
    admin_signature = generate_signature(admin_key, path)
    resp = client.delete(path,
                         headers={'admin_signature': admin_signature, 'admin_id': admin_id})
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'

    # test that the signup was inserted into the database
    with app.app_context():
        signup = EventSignup.query.filter_by(user_id=2).filter_by(event_id=1).first()
        assert not signup


def test_quit_event_fail(client, app):
    # test that signature check will fail
    key = '123'
    path = '/api/v1/event/1/user/3'
    signature = generate_signature(key, path)
    resp = client.delete(path,
                       headers={'signature': signature})
    assert resp.status_code == 401
    assert resp.json['status'] == 'failure'

    # test that user will not be found
    path = '/api/v1/event/1/user/5'
    signature = generate_signature(key, path)
    resp = client.delete(path,
                       headers={'signature': signature})
    assert resp.status_code == 404
    assert resp.json['status'] == 'failure'

    # test that event will not be found
    path = '/api/v1/event/3/user/3'
    key = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    signature = generate_signature(key, path)
    resp = client.delete(path,
                       headers={'signature': signature})
    assert resp.status_code == 404
    assert resp.json['status'] == 'failure'

    # test that signup does not exists
    path = '/api/v1/event/1/user/4'
    signature = generate_signature(key, path)
    resp = client.delete(path,
                       headers={'signature': signature})
    assert resp.status_code == 404
    assert resp.json['status'] == 'failure'

    # test that admin_signature check will fail
    path = '/api/v1/event/1/user/1'
    admin_key = '123'
    admin_id = 1
    admin_signature = generate_signature(admin_key, path)
    resp = client.delete(path,
                       headers={'admin_signature': admin_signature, 'admin_id': admin_id})
    assert resp.status_code == 401
    assert resp.json['status'] == 'failure'