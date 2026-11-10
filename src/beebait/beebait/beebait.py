import time

from beebait.communication import Transmitter, Uplink
from beebait.inference import Conclusion, InferenceEngine
from beebait.sensor import Sensor
from world.enums import FeatureName
from world.feature import FeatureValue
from world.model import GridPosition
from world.world import Cell

MAX_BEEBAIT_ID = 65535
DEFAULT_TRANSMISSION_INTERVAL = 600.0


class Beebait:
    def __init__(
        self,
        id: int,
        position: GridPosition,
        occupied: bool = False,
        sensors: list[Sensor] | None = None,
        features_values: list[FeatureValue] | None = None,
        inference_engine: InferenceEngine | None = None,
        transmission_interval: float = DEFAULT_TRANSMISSION_INTERVAL,
    ):
        if not 0 <= id <= MAX_BEEBAIT_ID:
            raise ValueError(f"Beebait id must be between 0 and {MAX_BEEBAIT_ID}")

        self._id = id
        self._position = position
        self._occupied = occupied
        self._sensors = sensors if sensors else []
        self._features_values: dict[str, FeatureValue] = {}
        self._inference_engine = (
            inference_engine if inference_engine else InferenceEngine()
        )
        self._conclusion: Conclusion | None = None
        self._transmission_interval = transmission_interval
        self._last_transmission: float | None = None

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

    @property
    def conclusion(self) -> Conclusion | None:
        return self._conclusion

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

    def infer(self) -> Conclusion | None:
        self._conclusion = self._inference_engine.submit(self._features_values)

        return self._conclusion

    def _feature_value(self, feature_name: FeatureName) -> float | None:
        feature_value = self._features_values.get(feature_name)

        return float(feature_value.value) if feature_value else None

    def _create_uplink(
        self, conclusion: Conclusion, simulated_hour: float
    ) -> Uplink:
        return Uplink(
            timestamp=int(time.time() * 1000),
            beebait_id=self._id,
            occupied=conclusion.occupied,
            confidence=conclusion.confidence,
            internal_temperature=self._feature_value(
                FeatureName.INTERNAL_TEMPERATURE
            ),
            external_temperature=self._feature_value(FeatureName.TEMPERATURE),
            row=self._position.row,
            column=self._position.column,
            simulated_hour=simulated_hour,
            ground_truth_occupied=self._occupied,
        )

    def transmit(
        self,
        transmitter: Transmitter,
        simulated_seconds: float,
        simulated_hour: float,
    ) -> Uplink | None:
        if self._conclusion is None:
            return None

        if (
            self._last_transmission is not None
            and simulated_seconds - self._last_transmission
            < self._transmission_interval
        ):
            return None

        uplink = self._create_uplink(self._conclusion, simulated_hour)
        transmitter.transmit(uplink)
        self._last_transmission = simulated_seconds

        return uplink

    def __repr__(self) -> str:
        return f"Beebait(id={self._id}, position={self._position}, occupied={self._occupied}, conclusion={self._conclusion}, features_values={self._features_values})"
