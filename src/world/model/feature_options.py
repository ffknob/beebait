from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureOptions:
    max_oscillation: float | None = None
    concentration: float = 10.0
    max_neighbour_deviation: float | None = None
    max_base_deviation: float | None = None
    excursion_probability: float = 0.0
    max_excursion: float | None = None
    daily_amplitude: float | None = None
    daily_peak_hour: float = 15.0
