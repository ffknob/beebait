from abc import ABC, abstractmethod

from world.enums import FeatureName
from world.feature import FeatureValue
from world.world import Cell


class Sensor(ABC):
    def __init__(self, feature_name: FeatureName):
        self.feature_name = feature_name

    @abstractmethod
    def read(self, cell: Cell, occupied: bool) -> FeatureValue | None:
        pass
