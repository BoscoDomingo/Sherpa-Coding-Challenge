class User:
    def __init__(self, userId: str, name: str, postalCode: str,  city: str | None = None):
        self.userId = userId
        self.name = name
        self.postalCode = postalCode
        self.city = city

    def __eq__(self, other):
        if isinstance(other, User):
            return self.userId == other.userId and self.name == other.name and self.postalCode == other.postalCode and self.city == other.city
        return False


if __name__ == '__main__':
    pass
