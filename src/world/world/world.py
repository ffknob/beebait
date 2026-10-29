from typing import Self

from world.feature import Feature
from world.model import WorldParameters

from .cell import Cell

DEFAULT_WORLD_COLUMNS = 20
DEFAULT_WORLD_ROWS = 20
DEFAULT_WORLD_REFRESH_RATE = 1.0


class World:
    def __init__(
        self,
        parameters: WorldParameters | None = None,
        features: set[Feature] | None = None,
    ):
        self._parameters = (
            parameters
            if parameters
            else WorldParameters(
                columns=DEFAULT_WORLD_COLUMNS,
                rows=DEFAULT_WORLD_ROWS,
                refresh_rate=DEFAULT_WORLD_REFRESH_RATE,
            )
        )
        self._grid: list[list[Cell]] = [
            [Cell() for _ in range(self._parameters.columns)]
            for _ in range(self._parameters.rows)
        ]
        self._features = features if features else set()

    @property
    def parameters(self) -> WorldParameters:
        return self._parameters

    @property
    def grid(self) -> list[list[Cell]]:
        return self._grid

    def _update_cell_features(self, cell: Cell) -> None:
        for feature in self._features:
            feature_value = feature.sample()
            cell.set_feature_value(feature_value)

    def _update_cells(self) -> None:
        for row in range(self._parameters.rows):
            for column in range(self._parameters.columns):
                cell: Cell = self._grid[row][column]
                self._update_cell_features(cell)

    def init(self) -> Self:
        self._update_cells()

        return self

    async def refresh(self) -> Self:
        self._update_cells()

        return self

    def __repr__(self) -> str:
        return f"World(parameters={self._parameters}, features={self._features})"
