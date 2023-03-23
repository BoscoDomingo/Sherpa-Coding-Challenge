from abc import ABC, abstractmethod

from src.domain.criteria.city.GetCityCriteria import GetCityCriteria


class CityRepository(ABC):
    @abstractmethod
    def get(self, criteria: GetCityCriteria) -> str: pass
