class UpdateUserLocationUseCaseInput:
    def __init__(self, userId: str, postalCode: str, city: str) -> None:
        self.userId = userId
        self.postalCode = postalCode
        self.city = city
