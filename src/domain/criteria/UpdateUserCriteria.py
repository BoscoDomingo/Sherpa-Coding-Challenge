class UpdateUserCriteria:
    def __init__(self, userId: str, postalCode: str, city: str) -> None:
        self.userId = userId
        self.postalCode = postalCode
        self.city = city

    def __eq__(self, other):
        if isinstance(other, UpdateUserCriteria):
            return self.userId == other.userId and self.postalCode == other.postalCode and self.city == other.city
        return False
