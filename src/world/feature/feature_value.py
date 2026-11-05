from typing import TypeVar

T = TypeVar("T")


class FeatureValue[T: (int, float, str)]:
    def __init__(
        self,
        feature_name: str,
        value: T,
        target: T | None = None,
        base: T | None = None,
    ):
        self.feature_name = feature_name
        self.value = value
        # Value this feature is currently drifting towards (None = no drift in progress)
        self.target = target
        # Value set when the world was created, around which this cell oscillates
        self.base = base

    def __repr__(self):
        return f"FeatureValue(feature_name={self.feature_name}, value={self.value}, target={self.target}, base={self.base})"
