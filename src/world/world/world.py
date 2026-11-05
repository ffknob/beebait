import random
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

        # Each cell paired with its (up to 8) neighbours, in row-major order
        self._cells_with_neighbours: list[tuple[Cell, list[Cell]]] = [
            (self._grid[row][column], self._get_neighbours(row, column))
            for row in range(self._parameters.rows)
            for column in range(self._parameters.columns)
        ]
        self._initialized = False

    @property
    def parameters(self) -> WorldParameters:
        return self._parameters

    @property
    def grid(self) -> list[list[Cell]]:
        return self._grid

    def _get_neighbours(self, row: int, column: int) -> list[Cell]:
        neighbours: list[Cell] = []

        for d_row in (-1, 0, 1):
            for d_column in (-1, 0, 1):
                if d_row == 0 and d_column == 0:
                    continue

                r, c = row + d_row, column + d_column
                if 0 <= r < self._parameters.rows and 0 <= c < self._parameters.columns:
                    neighbours.append(self._grid[r][c])

        return neighbours

    def _update_cell_features(self, cell: Cell, neighbours: list[Cell]) -> None:
        for feature in self._features:
            previous_feature_value = cell.features_values.get(feature.feature_name)

            # Neighbours not set yet (only possible during init) are skipped
            neighbours_values = [
                value
                for neighbour in neighbours
                if (value := neighbour.features_values.get(feature.feature_name))
                is not None
            ]

            feature_value = feature.sample(previous_feature_value, neighbours_values)
            cell.set_feature_value(feature_value)

    def init(self) -> Self:
        # Row-major order: every cell (but the first) already has its left and
        # upper neighbours set, so the field grows coherently from the corner
        for cell, neighbours in self._cells_with_neighbours:
            self._update_cell_features(cell, neighbours)

        self._initialized = True

        return self

    async def refresh(self) -> Self:
        if not self._initialized:
            return self.init()

        # Random order, so updates don't drift in the row-major direction
        random.shuffle(self._cells_with_neighbours)
        for cell, neighbours in self._cells_with_neighbours:
            self._update_cell_features(cell, neighbours)

        return self

    def __repr__(self) -> str:
        return f"World(parameters={self._parameters}, features={self._features})"
