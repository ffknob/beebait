import random

from world.enums import FeatureName
from world.feature import FeatureValue
from world.world import Cell

from .sensor import Sensor


class InternalTemperatureSensor(Sensor):
    def __init__(
        self,
        colony_temperature: float = 34.5,
        colony_deviation: float = 0.3,
        empty_offset: float = 0.5,
        empty_deviation: float = 0.3,
    ):
        super().__init__(FeatureName.INTERNAL_TEMPERATURE)

        self.colony_temperature = colony_temperature
        self.colony_deviation = colony_deviation
        self.empty_offset = empty_offset
        self.empty_deviation = empty_deviation

    def read(self, cell: Cell, occupied: bool) -> FeatureValue[float] | None:
        if occupied:
            return FeatureValue(
                self.feature_name,
                random.gauss(self.colony_temperature, self.colony_deviation),
            )

        temperature = cell.features_values.get(FeatureName.TEMPERATURE)
        if temperature is None:
            return None

        return FeatureValue(
            self.feature_name,
            temperature.value + random.gauss(self.empty_offset, self.empty_deviation),
        )
