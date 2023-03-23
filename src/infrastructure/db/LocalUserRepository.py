from src.domain.criteria.user.GetUserCriteria import GetUserCriteria
from src.domain.criteria.user.UpdateUserCriteria import UpdateUserCriteria
from src.domain.entities.User import User
from src.domain.repositories.UserRepository import UserRepository

# This would be a DB, accessed via a wrapper of the DB driver


class LocalDB(UserRepository):
    def __init__(self) -> None:
        self.master: dict[str, str] = {}
        self.detalle: dict[str, tuple[str, str | None]] = {}

    def get(self, criteria: GetUserCriteria) -> User:
        userId = criteria.userId
        if not userId in self.master or not userId in self.detalle:
            raise KeyError(f'User {userId} not found')

        name: str = self.master[userId]
        postalCode, city = self.detalle[userId]
        return User(userId, name, postalCode, city)

    def save(self, user: User):
        if not user or not user.userId or not user.name or not user.postalCode:
            raise ValueError('User is invalid')
        if user.userId in self.master:
            raise ValueError(f'User {user.userId} already exists')

        self.detalle[user.userId] = (user.postalCode, None)
        self.master[user.userId] = user.name

    def update(self, criteria: UpdateUserCriteria):
        userId = criteria.userId
        if not userId in self.master or not userId in self.detalle:
            raise KeyError(f'User {userId} not found')
        if not criteria.postalCode or not criteria.city:
            raise ValueError('User is invalid')

        self.detalle[userId] = (criteria.postalCode, criteria.city)


# These are an implementation detail that could be nice to use to better define the expected tables.
# Python lacks a true custom types system and these would therefore have to be value objects.
# In a real-life scenario they would be defined in the actual DB schema.
class MasterRow:
    def __init__(self, userId: str, name: str):
        self.userId = userId
        self.name = name


class DetalleRow:
    def __init__(self, userId: str, postalCode: str, city: str):
        self.userId = userId
        self.postalCode = postalCode
        self.city = city
