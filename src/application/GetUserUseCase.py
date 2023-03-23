from src.application.input.GetUserUseCaseInput import GetUserUseCaseInput
from src.application.UseCase import UseCase
from src.domain.criteria.user.GetUserCriteria import GetUserCriteria
from src.domain.entities.User import User
from src.domain.repositories.UserRepository import UserRepository


class GetUserUseCase(UseCase):
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, input: GetUserUseCaseInput) -> User:
        return self.repository.get(GetUserCriteria(input.userId))