class User:
    def __init__(self, userId: str, name: str, postalCode: str,  city: str | None = None):
        self.userId = userId
        self.name = name
        self.postalCode = postalCode
        self.city = city


if __name__ == '__main__':
    pass
