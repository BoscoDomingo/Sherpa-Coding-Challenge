import requests

from src.domain.criteria.user.GetUserCriteria import GetUserCriteria
from src.domain.criteria.user.UpdateUserCriteria import UpdateUserCriteria
from src.domain.entities.User import User
from src.domain.repositories.UserRepository import UserRepository


class Logic:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def getUserById(self, userId: str) -> User:
        return self._repository.get(GetUserCriteria(userId))

    def createUserWithId(self, userId: str, name: str, postalCode: str) -> User:
        user = User(userId=userId, name=name, postalCode=postalCode)
        self._repository.save(user)
        return user

    def updateUserById(self, userId: str, postalCode: str) -> dict[str, str]:
        city: str = self._fetchCity(postalCode)
        self._repository.update(UpdateUserCriteria(userId, postalCode, city))
        return {'message': f'User {userId} updated.'}

    def _fetchCity(self, postalCode: str) -> str:
        try:
            postalCode = self._parsePostalCode(postalCode)
            url: str = ("http://api.geonames.org/postalCodeSearchJSON?"
                        f"postalcode={postalCode}"
                        "&username=boscodomingo&maxRows=1")
            response = requests.get(url, timeout=10)
            city: str = response.json()['postalCodes'][0]['placeName']
            return city
        except:
            raise Exception('Error in the request')

    def _parsePostalCode(self, postalCode: str) -> str:
        return ''.join(char for char in postalCode if char.isdigit())


if __name__ == '__main__':
    pass
