import random

from world.enums import FeatureName
from world.feature import FeatureValue
from world.world import Cell

from .sensor import Sensor


class ExternalTemperatureSensor(Sensor):
    def __init__(self, noise: float = 0.1):
        super().__init__(FeatureName.TEMPERATURE)

        self.noise = noise

    def read(self, cell: Cell, occupied: bool) -> FeatureValue[float] | None:
        temperature = cell.features_values.get(FeatureName.TEMPERATURE)
        if temperature is None:
            return None

        return FeatureValue(
            self.feature_name, temperature.value + random.gauss(0, self.noise)
        )
