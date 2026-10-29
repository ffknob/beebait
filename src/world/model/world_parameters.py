from dataclasses import dataclass


@dataclass(frozen=True)
class WorldParameters:
    columns: int = 20
    rows: int = 20
    refresh_rate: float = 1.0
