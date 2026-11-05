from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureOptions:
    # Maximum absolute change between two consecutive samples (None = unlimited)
    max_oscillation: float | None = None
    # Beta distribution concentration: higher values keep samples closer to the mean
    concentration: float = 10.0
    # Maximum absolute deviation from the neighbours' mean (None = independent cells)
    max_neighbour_deviation: float | None = None
    # Maximum absolute deviation from the cell's initial value over time; keeps
    # cold/hot zones from fading away (None = targets drawn from the statistics)
    max_base_deviation: float | None = None
