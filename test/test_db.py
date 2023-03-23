import pytest

from src.domain.criteria.GetUserCriteria import GetUserCriteria
from src.domain.criteria.UpdateUserCriteria import UpdateUserCriteria
from src.domain.entities.User import User
from src.infrastructure.db.LocalUserRepository import LocalDB


@pytest.fixture
def db():
    db = LocalDB()
    user1 = User('1', 'John Doe', 'NY12345', 'New York')
    user2 = User('2', 'Alexa Siri', 'CA12345', 'Los Angeles')
    # If these were to fail, the whole suite would fail.
    # Due to time constraints we'll keep it as is,
    # but a proper mock should be used in the future.
    db.save(user1)
    db.save(user2)
    return db


@pytest.fixture
def user():
    return User(userId='1', name='John Doe', postalCode='NY12345')


def test_getWorksWithExistingUser(db: LocalDB, user: User):
    assert db.get(GetUserCriteria(user.userId)) == user


def test_getFailsWithNonExistingUser(db: LocalDB):
    with pytest.raises(Exception):
        db.get(GetUserCriteria('3'))


def test_getFailsWithInvalidInput(db: LocalDB):
    with pytest.raises(KeyError):
        db.get(GetUserCriteria('invalid'))


def test_saveWorksWithValidUser(db: LocalDB):
    userToAdd = User(userId='3', name='Samuel L. Jackson', postalCode='CA20031', city='Los Angeles')

    db.save(userToAdd)

    assert db.master['3'] == userToAdd.name
    assert db.detalle['3'] == (userToAdd.postalCode, None)


def test_saveFailsWithInvalidUser(db: LocalDB):
    with pytest.raises(ValueError):
        db.save(None)  # type: ignore


def test_saveFailsWithInvalidInput(db: LocalDB):
    with pytest.raises(AttributeError):
        db.save('user')  # type: ignore


def test_updateWorksWithExistingUser(db: LocalDB):
    userId = '1'

    db.update(UpdateUserCriteria(userId, '28001', 'Madrid'))

    assert db.detalle[userId] == ('28001', 'Madrid')


def test_updateFailsIfUserDoesNotExist(db: LocalDB):
    with pytest.raises(KeyError):
        db.update(UpdateUserCriteria('3', '28001', 'Madrid'))


def test_updateFailsWithInvalidInput(db: LocalDB):
    with pytest.raises(KeyError):
        db.update(UpdateUserCriteria(8, '28001', 'Madrid')) # type: ignore
