import json

import pytest

from src.app import app
from src.domain.entities.User import User


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def user() -> User:
    return User(userId='1', name='John Doe', postalCode='CA98765', city='Los Angeles')


def test_getUserWorksWithExistentUser(client, user: User):
    client.post(f'/user/{user.userId}', data=json.dumps(user.__dict__), content_type='application/json')

    response = client.get(f'/user/{user.userId}')

    assert response.status_code == 200
    assert json.loads(response.data) == {
        "city": None,
        "name": user.name,
        "postalCode": user.postalCode,
        "userId": user.userId
    }


def test_getUserFailsWithNonexistentUser(client):
    response = client.get('/user/nonexistent-user-id')

    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'User not found'}


def test_createUserWorksWithValidUser(client, user: User):
    data = {'name': user.name, 'postalCode': user.postalCode}
    userId = '2'

    response = client.post(f'/user/{userId}', json=data, content_type='application/json')

    assert response.status_code == 200
    assert json.loads(response.data) == {
        'userId': userId,
        'name': user.name,
        'postalCode': user.postalCode,
        'city': None
    }


def test_createUserFailsIfUserExisted(client, user: User):
    data = {'name': user.name, 'postalCode': user.postalCode}
    userId = '2'

    response = client.post(f'/user/{userId}', json=data, content_type='application/json')

    assert response.status_code == 400
    assert json.loads(response.data) == {'message': f'User {userId} already exists'}


def test_createUserFailsIfDataMissingPostalCode(client):
    data = {'name': 'Jimmy Johnson'}
    userId = '3'

    response = client.post(f'/user/{userId}', json=data, content_type='application/json')

    assert response.status_code == 400
    assert json.loads(response.data) == {'message': 'Error in the request body'}


def test_createUserFailsIfDataMissingName(client):
    data = {'postalCode': 'NY10000'}
    userId = '3'

    response = client.post(f'/user/{userId}', json=data, content_type='application/json')

    assert response.status_code == 400
    assert json.loads(response.data) == {'message': 'Error in the request body'}


def test_createUserFailsIfDataIsEmpty(client):
    data = {}
    userId = '3'

    response = client.post(f'/user/{userId}', json=data, content_type='application/json')

    assert response.status_code == 400
    assert json.loads(response.data) == {'message': 'Error in the request body'}


def test_updateUserWorksWithValidUserIdAndPostalCode(client, user: User):
    data = {'postalCode': 'GA30250', 'name': user.name}

    response = client.put(f'/user/{user.userId}', json=data, content_type='application/json')

    assert response.status_code == 200
    assert json.loads(response.data) == {'message': f'User {user.userId} updated.'}


def test_updateUserFailsWithNonexistentUserId(client, user: User):
    data = {'postalCode': 'GA30250', 'name': user.name}
    userId = 'nonexistent-user-id'

    response = client.put(f'/user/{userId}', json=data, content_type='application/json')

    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'User not found'}


def test_updateUserFailsWithInvalidPostalCode(client, user: User):
    data = {'postalCode': 'invalid-postal-code', 'name': user.name}

    response = client.put(f'/user/{user.userId}', json=data, content_type='application/json')

    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'Error in the request'}


def test_updateUserFailsIfDataMissingName(client):
    data = {'postalCode': 'NY10000'}
    userId = '3'

    response = client.put(f'/user/{userId}', json=data, content_type='application/json')

    assert response.status_code == 400
    assert json.loads(response.data) == {'message': 'Error in the request body'}


def test_updateUserFailsIfDataIsEmpty(client):
    data = {}
    userId = '3'

    response = client.put(f'/user/{userId}', json=data, content_type='application/json')

    assert response.status_code == 400
    assert json.loads(response.data) == {'message': 'Error in the request body'}
