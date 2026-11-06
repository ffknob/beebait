import random

from world.model import GridPosition, WorldParameters


class Swarm:
    def __init__(self, id: int, position: GridPosition):
        self._id = id
        self._position = position
        self._settled = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def position(self) -> GridPosition:
        return self._position

    @property
    def settled(self) -> bool:
        return self._settled

    def is_adjacent_to(self, position: GridPosition) -> bool:
        return (
            abs(self._position.row - position.row) <= 1
            and abs(self._position.column - position.column) <= 1
        )

    def move(self, parameters: WorldParameters) -> None:
        if self._settled:
            return

        positions = [
            GridPosition(row, column)
            for d_row in (-1, 0, 1)
            for d_column in (-1, 0, 1)
            if (d_row, d_column) != (0, 0)
            and 0 <= (row := self._position.row + d_row) < parameters.rows
            and 0 <= (column := self._position.column + d_column) < parameters.columns
        ]

        self._position = random.choice(positions)

    def settle(self) -> None:
        self._settled = True

    def __repr__(self) -> str:
        return (
            f"Swarm(id={self._id}, position={self._position}, settled={self._settled})"
        )
