from typing import TypeVar

T = TypeVar("T")


class FeatureValue[T: (int, float, str)]:
    def __init__(self, feature_name: str, value: T):
        self.feature_name = feature_name
        self.value = value

    def __repr__(self):
        return f"FeatureValue(feature_name={self.feature_name}, value={self.value})"
