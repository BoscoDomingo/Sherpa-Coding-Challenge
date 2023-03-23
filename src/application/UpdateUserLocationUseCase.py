from src.application.input.UpdateUserLocationUseCaseInput import \
    UpdateUserLocationUseCaseInput
from src.application.UseCase import UseCase
from src.domain.criteria.user.UpdateUserCriteria import UpdateUserCriteria
from src.domain.repositories.UserRepository import UserRepository


class UpdateUserLocationUseCase(UseCase):
    def __init__(self, userRepository: UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self, input: UpdateUserLocationUseCaseInput):
        if not input.userId or not input.postalCode or not input.city:
            raise Exception('Incorrect data')
        self.userRepository.update(UpdateUserCriteria(input.userId, input.postalCode, input.city))
