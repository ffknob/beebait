from abc import ABC, abstractmethod
import random

from world.model import FeatureStatistics
from world.enums import FeatureType


class Feature(ABC):
    def __init__(
        self, feature_type: FeatureType, statistics: FeatureStatistics
    ):
        self.feature_type = feature_type
        self.statistics = statistics

    @abstractmethod
    def sample(self) -> float:
        pass
