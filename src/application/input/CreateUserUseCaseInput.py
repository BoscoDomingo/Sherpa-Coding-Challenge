class CreateUserUseCaseInput:
    def __init__(self, userId: str, name: str, postalCode: str) -> None:
        self.userId = userId
        self.name = name
        self.postalCode = postalCode
