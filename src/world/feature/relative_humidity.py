import random

from world.enums import FeatureName
from world.feature import Feature, FeatureValue
from world.model import FeatureStatistics


class RelativeHumidity(Feature[float]):
    def __init__(self, statistics: FeatureStatistics):
        super().__init__(FeatureName.RELATIVE_HUMIDITY, statistics)

    def sample(self, concentration: float = 10.0) -> FeatureValue[float]:
        e = self.statistics
        amplitude = e.max - e.min
        if amplitude <= 0:
            return FeatureValue(self.feature_name, e.min)

        m = (e.mean - e.min) / amplitude
        alpha = m * concentration
        beta = (1 - m) * concentration

        sample = e.min + random.betavariate(alpha, beta) * amplitude

        return FeatureValue(self.feature_name, sample)
