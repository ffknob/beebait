import random

from world.enums import FeatureType
from world.model import FeatureStatistics

from .feature import Feature


class Temperature(Feature):
    def __init__(self, statistics: FeatureStatistics):
        super().__init__(FeatureType.TEMPERATURE, statistics)

    def sample(self, concentration: float = 10.0) -> float:
        e = self.statistics
        amplitude = e.max - e.min
        if amplitude <= 0:
            return e.min

        m = (e.mean - e.min) / amplitude
        alpha = m * concentration
        beta = (1 - m) * concentration

        return e.min + random.betavariate(alpha, beta) * amplitude
