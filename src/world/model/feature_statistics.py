from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureStatistics:
    min: float
    max: float
    mean: float
    median: float
