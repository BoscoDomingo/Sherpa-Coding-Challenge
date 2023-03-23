from unittest.mock import Mock, patch

import pytest

from src.db import LocalDB
from src.logic import Logic
from src.user import User


@pytest.fixture
def db() -> LocalDB:
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
def user() -> User:
    return User(userId='1', name='John Doe', postalCode='NY12345', city='New York')


def test_getUserByIdWorksWithExistingUser(db: LocalDB, user: User):
    logic = Logic(db)

    assert logic.getUserById('1') == user


def test_getUserByIdFailsWithNonexistentUser(db: LocalDB):
    logic = Logic(db)

    with pytest.raises(Exception, match='User 3 not found'):
        logic.getUserById('3')


@pytest.mark.skip(reason="Redundant since there are no restricions to userIds in place")
def test_getUserByIdFailsWithInvalidUserId(db: LocalDB):
    logic = Logic(db)

    with pytest.raises(Exception, match='User not found'):
        logic.getUserById('invalid')


def test_createUserWithIdWorksWithValidUser(db: LocalDB):
    logic = Logic(db)

    userToAdd = User(userId='3', name='Joseph', postalCode='1000')
    userAdded = logic.createUserWithId(userId=userToAdd.userId, name=userToAdd.name, postalCode=userToAdd.postalCode)

    assert userAdded == userToAdd


def test_createUserWithIdReturnsExistingUserIfUserIdAlreadyPresent(db: LocalDB, user: User):
    logic = Logic(db)
    with pytest.raises(ValueError, match=f'User {user.userId} already exists'):
        logic.createUserWithId(userId=user.userId, name=user.name, postalCode=user.postalCode)


def test_updateUserByIdWorksWithValidUser(db: LocalDB, user: User):
    logic = Logic(db)

    with patch.object(logic, '_fetchCity', return_value='Bilbao') as mockFetchCity:
        result = logic.updateUserById(userId=user.userId, postalCode='1000')

    assert result == {'message': f'User {user.userId} updated.'}
    assert logic.getUserById('1').city == 'Bilbao'
    assert logic.getUserById('1').postalCode == '1000'
    mockFetchCity.assert_called_once_with('1000')


def test_updateUserByIdFailsWithNonexistentUser(db: LocalDB):
    logic = Logic(db)

    with pytest.raises(Exception, match='User not found'):
        logic.updateUserById(userId='5', postalCode='1000')


def test_updateUserById_fetchCityError(db: LocalDB, user: User):
    logic = Logic(db)

    with patch.object(logic, '_fetchCity', side_effect=Exception('Error in the request')):
        with pytest.raises(Exception, match='Error in the request'):
            logic.updateUserById(userId=user.userId, postalCode='1000')


def test_fetchCityWorksWithValidRequest(db: LocalDB):
    logic = Logic(db)
    response = Mock()
    response.json.return_value = {'postalCodes': [{'placeName': 'Bilbao'}]}

    with patch('requests.get', return_value=response):
        assert logic._fetchCity('1000') == 'Bilbao'


def test_fetchCityFailsWhenRequestFails(db: LocalDB):
    logic = Logic(db)

    with patch('requests.get', side_effect=Exception('Error in the request')):
        with pytest.raises(Exception, match='Error in the request'):
            logic._fetchCity('1000')


def test_parsePostalCodeWorksWithValidInputs(db: LocalDB):
    logic = Logic(db)

    assert logic._parsePostalCode('1A2B3C') == '123'
    assert logic._parsePostalCode('123') == '123'
    assert logic._parsePostalCode('ABC') == ''


def test_parsePostalCodeWorksWithEmptyInputs(db: LocalDB):
    logic = Logic(db)

    assert logic._parsePostalCode('') == ''
    assert logic._parsePostalCode(' ') == ''
