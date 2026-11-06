from world.enums import FeatureName
from world.model import FeatureOptions, FeatureStatistics

from .feature import Feature
from .feature_value import FeatureValue


class RelativeHumidity(Feature[float]):
    def __init__(
        self, statistics: FeatureStatistics, options: FeatureOptions | None = None
    ):
        super().__init__(FeatureName.RELATIVE_HUMIDITY, statistics, options)

    def sample(
        self,
        previous_feature_value: FeatureValue | None,
        neighbours_values: list[FeatureValue],
        hour: float,
    ) -> FeatureValue[float]:
        value, target, base, offset, excursion = self._next_value(
            previous_feature_value, neighbours_values, hour
        )

        return FeatureValue(self.feature_name, value, target, base, offset, excursion)
