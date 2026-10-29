from abc import ABC, abstractmethod

from world.enums import FeatureName
from world.model import FeatureStatistics

from .feature_value import FeatureValue


class Feature[T: (int, float, str)](ABC):
    def __init__(self, feature_name: FeatureName, statistics: FeatureStatistics):
        self.feature_name = feature_name
        self.statistics = statistics

    @abstractmethod
    def sample(self) -> FeatureValue[T]:
        pass
