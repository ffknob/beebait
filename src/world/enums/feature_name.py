from enum import StrEnum


class FeatureName(StrEnum):
    TEMPERATURE = "temperature"
    RELATIVE_HUMIDITY = "relative_humidity"
    INTERNAL_TEMPERATURE = "internal_temperature"
    INTERNAL_RELATIVE_HUMIDITY = "internal_relative_humidity"
    ACOUSTIC_ENERGY = "acoustic_energy"
    DOMINANT_FREQUENCY = "dominant_frequency"
