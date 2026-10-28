from dataclasses import dataclass


@dataclass(frozen=True)
class WorldParameters:
    columns: int
    rows: int
    refresh_rate: float
