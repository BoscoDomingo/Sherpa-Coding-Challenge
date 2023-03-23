from src.domain.entities.User import User


class LocalDB:
    def __init__(self) -> None:
        self.master: dict[str, str] = {}
        self.detalle: dict[str, tuple[str, str | None]] = {}

    def getUserById(self, userId: str) -> User:
        if not userId in self.master or not userId in self.detalle:
            raise KeyError(f'User {userId} not found')

        name: str = self.master[userId]
        postalCode, city = self.detalle[userId]
        return User(userId, name, postalCode, city)

    def addUserToDB(self, user: User):
        if not user:
            raise ValueError('User is None')
        if user.userId in self.master:
            raise ValueError(f'User {user.userId} already exists')

        self.detalle[user.userId] = (user.postalCode, user.city)
        self.master[user.userId] = user.name

    def updateUserLocation(self, userId: str, postalCode: str, city: str | None):
        if not userId in self.master or not userId in self.detalle:
            raise KeyError(f'User {userId} not found')
        self.detalle[userId] = (postalCode, city)