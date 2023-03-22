import pytest

from src.user import User
from src.db import LocalDB


@pytest.fixture
def db():
    db = LocalDB()
    user1 = User('1', 'John Doe', 'NY12345', 'New York')
    user2 = User('2', 'Alexa Siri', 'CA12345', 'Los Angeles')
    # If these were to fail, the whole suite would fail.
    # Due to time constraints we'll keep it as is,
    # but a proper mock should be used in the future.
    db.addUserToDB(user1)
    db.addUserToDB(user2)
    return db


@pytest.fixture
def user():
    return User(userId='1', name='John Doe', postalCode='NY12345', city='New York')


def test_getUserByIdWorksWithExistingUser(db, user):
    assert db.getUserById('1').name == user.name
    assert db.getUserById('1').postalCode == user.postalCode
    assert db.getUserById('1').city == user.city


def test_getUserByIdFailsWithNonExistingUser(db):
    with pytest.raises(Exception):
        db.getUserById('3')


def test_getUserByIdFailsWithInvalidInput(db):
    with pytest.raises(KeyError):
        db.getUserById('invalid')


def test_addUserToDBWorksWithValidUser(db):
    userToAdd = User(userId='3', name='Samuel L. Jackson', postalCode='CA20031', city='Los Angeles')

    db.addUserToDB(userToAdd)

    assert db.master['3'] == userToAdd.name
    assert db.detalle['3'] == (userToAdd.postalCode, userToAdd.city)


def test_addUserToDBFailsWithInvalidUser(db):
    with pytest.raises(ValueError):
        db.addUserToDB(None)


def test_addUserToDBFailsWithInvalidInput(db):
    with pytest.raises(AttributeError):
        db.addUserToDB('user')


def test_updateUserLocationWorksWithExistingUser(db):
    db.updateUserLocation('1', '28001', 'Madrid')

    assert db.detalle['1'] == ('28001', 'Madrid')


def test_updateUserLocationFailsIfUserDoesNotExist(db):
    with pytest.raises(KeyError):
        db.updateUserLocation('3', '28001', 'Madrid')


def test_updateUserLocationFailsWithInvalidInput(db):
    with pytest.raises(KeyError):
        db.updateUserLocation('invalid', '28001', 'Madrid')
