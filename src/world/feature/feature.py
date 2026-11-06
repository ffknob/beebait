import math
import random
from abc import ABC, abstractmethod

from world.enums import FeatureName
from world.model import FeatureOptions, FeatureStatistics

from .feature_value import FeatureValue


class Feature[T: (int, float, str)](ABC):
    def __init__(
        self,
        feature_name: FeatureName,
        statistics: FeatureStatistics,
        options: FeatureOptions | None = None,
    ):
        self.feature_name = feature_name
        self.statistics = statistics
        self.options = options if options else FeatureOptions()

    def _sample_from_statistics(self) -> float:
        e = self.statistics
        amplitude = e.max - e.min
        if amplitude <= 0:
            return e.min

        m = (e.mean - e.min) / amplitude
        alpha = m * self.options.concentration
        beta = (1 - m) * self.options.concentration

        return e.min + random.betavariate(alpha, beta) * amplitude

    def _daily_offset(self, hour: float) -> float:
        amplitude = self.options.daily_amplitude
        if amplitude is None:
            return 0.0

        return amplitude * math.cos(
            2 * math.pi * (hour - self.options.daily_peak_hour) / 24
        )

    def _pull_towards_neighbours(
        self, value: float, neighbours_values: list[float]
    ) -> float:
        max_deviation = self.options.max_neighbour_deviation
        if max_deviation is None or not neighbours_values:
            return value

        center = sum(neighbours_values) / len(neighbours_values)
        deviation = max(-max_deviation, min(value - center, max_deviation))

        return max(self.statistics.min, min(center + deviation, self.statistics.max))

    def _sample_around_base(self, base: float | None) -> float:
        max_base_deviation = self.options.max_base_deviation
        if base is None or max_base_deviation is None:
            return self._sample_from_statistics()

        target = base + random.uniform(-max_base_deviation, max_base_deviation)

        return max(self.statistics.min, min(target, self.statistics.max))

    def _sample_excursion(self, base: float | None) -> float | None:
        max_excursion = self.options.max_excursion
        if (
            base is None
            or max_excursion is None
            or random.random() >= self.options.excursion_probability
        ):
            return None

        min_excursion = min(self.options.max_base_deviation or 0.0, max_excursion)
        target = base + random.choice((-1, 1)) * random.uniform(
            min_excursion, max_excursion
        )

        return max(self.statistics.min, min(target, self.statistics.max))

    def _next_value(
        self,
        previous_feature_value: FeatureValue | None,
        neighbours_feature_values: list[FeatureValue],
        hour: float,
    ) -> tuple[float, float | None, float | None, float, bool]:
        max_oscillation = self.options.max_oscillation
        offset = self._daily_offset(hour)
        neighbours_values = [n.value - n.offset for n in neighbours_feature_values]

        if previous_feature_value is None or max_oscillation is None:
            value = self._pull_towards_neighbours(
                self._sample_from_statistics(), neighbours_values
            )

            return value + offset, None, value, offset, False

        previous = previous_feature_value.value - previous_feature_value.offset
        target = previous_feature_value.target
        base = previous_feature_value.base
        excursion = previous_feature_value.excursion

        if target is not None and not excursion:
            target = self._pull_towards_neighbours(target, neighbours_values)

        if target is None or abs(target - previous) <= max_oscillation:
            excursion_target = self._sample_excursion(base)
            excursion = excursion_target is not None
            target = (
                excursion_target
                if excursion_target is not None
                else self._pull_towards_neighbours(
                    self._sample_around_base(base), neighbours_values
                )
            )

        step = random.uniform(0, max_oscillation)
        delta = max(-step, min(target - previous, step))

        return previous + delta + offset, target, base, offset, excursion

    @abstractmethod
    def sample(
        self,
        previous_feature_value: FeatureValue | None,
        neighbours_values: list[FeatureValue],
        hour: float,
    ) -> FeatureValue[T]:
        pass
