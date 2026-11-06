from beebait.sensor import Sensor
from world.feature import FeatureValue
from world.model import GridPosition
from world.world import Cell

MAX_BEEBAIT_ID = 65535


class Beebait:
    def __init__(
        self,
        id: int,
        position: GridPosition,
        occupied: bool = False,
        sensors: list[Sensor] | None = None,
        features_values: list[FeatureValue] | None = None,
    ):
        if not 0 <= id <= MAX_BEEBAIT_ID:
            raise ValueError(f"Beebait id must be between 0 and {MAX_BEEBAIT_ID}")

        self._id = id
        self._position = position
        self._occupied = occupied
        self._sensors = sensors if sensors else []
        self._features_values: dict[str, FeatureValue] = {}

        for feature_value in features_values or []:
            self.set_feature_value(feature_value)

    @property
    def id(self) -> int:
        return self._id

    @property
    def position(self) -> GridPosition:
        return self._position

    @property
    def occupied(self) -> bool:
        return self._occupied

    @property
    def sensors(self) -> list[Sensor]:
        return self._sensors

    @property
    def features_values(self) -> dict[str, FeatureValue]:
        return self._features_values

    def occupy(self) -> None:
        self._occupied = True

    def vacate(self) -> None:
        self._occupied = False

    def set_feature_value(self, feature_value: FeatureValue) -> None:
        self._features_values[feature_value.feature_name] = feature_value

    def read_sensors(self, cell: Cell) -> None:
        for sensor in self._sensors:
            feature_value = sensor.read(cell, self._occupied)
            if feature_value is not None:
                self.set_feature_value(feature_value)

    def __repr__(self) -> str:
        return f"Beebait(id={self._id}, position={self._position}, occupied={self._occupied}, features_values={self._features_values})"
