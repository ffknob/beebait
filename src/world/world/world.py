import random
from datetime import UTC, datetime
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

        self._cells_with_neighbours: list[tuple[Cell, list[Cell]]] = [
            (self._grid[row][column], self._get_neighbours(row, column))
            for row in range(self._parameters.rows)
            for column in range(self._parameters.columns)
        ]
        self._initialized = False
        self._simulated_seconds = self._parameters.start_hour * 3600
        self._epoch = (
            datetime.now(UTC)
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .timestamp()
        )

    @property
    def parameters(self) -> WorldParameters:
        return self._parameters

    @property
    def grid(self) -> list[list[Cell]]:
        return self._grid

    @property
    def simulated_seconds(self) -> float:
        return self._simulated_seconds

    @property
    def simulated_timestamp(self) -> float:
        return self._epoch + self._simulated_seconds

    @property
    def hour(self) -> float:
        return (self._simulated_seconds / 3600) % 24

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

            neighbours_values = [
                value
                for neighbour in neighbours
                if (value := neighbour.features_values.get(feature.feature_name))
                is not None
            ]

            feature_value = feature.sample(
                previous_feature_value, neighbours_values, self.hour
            )
            cell.set_feature_value(feature_value)

    def init(self) -> Self:
        for cell, neighbours in self._cells_with_neighbours:
            self._update_cell_features(cell, neighbours)

        self._initialized = True

        return self

    async def refresh(self, elapsed_seconds: float) -> Self:
        if not self._initialized:
            return self.init()

        self._simulated_seconds += elapsed_seconds * self._parameters.time_scale

        random.shuffle(self._cells_with_neighbours)
        for cell, neighbours in self._cells_with_neighbours:
            self._update_cell_features(cell, neighbours)

        return self

    def __repr__(self) -> str:
        return f"World(parameters={self._parameters}, features={self._features})"
