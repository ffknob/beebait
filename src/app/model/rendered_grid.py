from dataclasses import dataclass

from .grid_cell import GridCell


@dataclass(frozen=True)
class Grid:
    columns: int
    rows: int
    cells: list[GridCell] | None = None
