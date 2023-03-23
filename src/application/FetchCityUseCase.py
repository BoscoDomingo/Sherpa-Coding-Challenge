import requests

from src.application.input.FetchCityUseCaseInput import FetchCityUseCaseInput
from src.application.UseCase import UseCase
from src.domain.repositories.UserRepository import UserRepository


class FetchCityUseCase(UseCase):
    def __init__(self, userRepository: UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self, input: FetchCityUseCaseInput) -> str:
        try:
            postalCode = self._parsePostalCode(input.postalCode)
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