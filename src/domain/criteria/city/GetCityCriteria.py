class GetCityCriteria:
    def __init__(self, postalCode: str) -> None:
        self.postalCode = postalCode

    def __eq__(self, other):
        if isinstance(other, GetCityCriteria):
            return self.postalCode == other.postalCode
        return False