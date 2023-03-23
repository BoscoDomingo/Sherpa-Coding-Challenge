from src.application.input.CreateUserUseCaseInput import CreateUserUseCaseInput
from src.application.UseCase import UseCase
from src.domain.entities.User import User
from src.domain.repositories.UserRepository import UserRepository


class CreateUserUseCase(UseCase):
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, input: CreateUserUseCaseInput) -> User:
        user = User(userId=input.userId, name=input.name, postalCode=input.postalCode)
        self.repository.save(user)
        return user
