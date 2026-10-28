from abc import ABC, abstractmethod

from world.enums import FeatureName
from world.feature import FeatureValue
from world.model import FeatureStatistics


class Feature[T: (int, float, str)](ABC):
    def __init__(self, feature_name: FeatureName, statistics: FeatureStatistics):
        self.feature_name = feature_name
        self.statistics = statistics

    @abstractmethod
    def sample(self) -> FeatureValue[T]:
        pass
