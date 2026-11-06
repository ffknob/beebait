from dataclasses import dataclass


@dataclass(frozen=True)
class GridPosition:
    row: int
    column: int
