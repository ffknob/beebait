from dataclasses import dataclass

from .rendered_cell import RenderedCell


@dataclass(frozen=True)
class RenderedGrid:
    columns: int
    rows: int
    cells: list[list[RenderedCell]] | None = None
