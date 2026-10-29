from dataclasses import dataclass


@dataclass(frozen=True)
class Grid:
    columns: int
    rows: int
