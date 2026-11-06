from typing import TypeVar

T = TypeVar("T")


class FeatureValue[T: (int, float, str)]:
    def __init__(
        self,
        feature_name: str,
        value: T,
        target: T | None = None,
        base: T | None = None,
        offset: float = 0.0,
        excursion: bool = False,
    ):
        self.feature_name = feature_name
        self.value = value
        self.target = target
        self.base = base
        self.offset = offset
        self.excursion = excursion

    def __repr__(self):
        return f"FeatureValue(feature_name={self.feature_name}, value={self.value}, target={self.target}, base={self.base}, offset={self.offset}, excursion={self.excursion})"
