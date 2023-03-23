from abc import ABC, abstractmethod

from src.domain.criteria.user.GetUserCriteria import GetUserCriteria
from src.domain.criteria.user.UpdateUserCriteria import UpdateUserCriteria
from src.domain.entities.User import User


class UserRepository(ABC):
    @abstractmethod
    def get(self, criteria: GetUserCriteria) -> User: pass
    @abstractmethod
    def save(self, user: User): pass
    @abstractmethod
    def update(self, criteria: UpdateUserCriteria): pass
