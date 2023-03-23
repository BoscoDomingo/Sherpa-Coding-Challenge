class GetUserCriteria:
    def __init__(self, userId: str) -> None:
        self.userId = userId

    def __eq__(self, other):
        if isinstance(other, GetUserCriteria):
            return self.userId == other.userId
        return False