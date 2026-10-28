from world.feature import FeatureValue


class Cell:
    def __init__(self):
        self._features_values: dict[str, FeatureValue] = {}

    @property
    def features_values(self) -> dict[str, FeatureValue]:
        return self._features_values

    def set_feature_value(self, feature_value: FeatureValue) -> None:
        self._features_values[feature_value.feature_name] = feature_value
