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

    def _pull_towards_neighbours(
        self, value: float, neighbours_values: list[FeatureValue]
    ) -> float:
        """Brings value within max_neighbour_deviation of the neighbours' mean."""
        max_deviation = self.options.max_neighbour_deviation
        if max_deviation is None or not neighbours_values:
            return value

        center = sum(n.value for n in neighbours_values) / len(neighbours_values)
        deviation = max(-max_deviation, min(value - center, max_deviation))

        return max(self.statistics.min, min(center + deviation, self.statistics.max))

    def _sample_around_base(self, base: float | None) -> float:
        max_base_deviation = self.options.max_base_deviation
        if base is None or max_base_deviation is None:
            return self._sample_from_statistics()

        target = base + random.uniform(-max_base_deviation, max_base_deviation)

        return max(self.statistics.min, min(target, self.statistics.max))

    def _next_value(
        self,
        previous_feature_value: FeatureValue | None,
        neighbours_values: list[FeatureValue],
    ) -> tuple[float, float | None, float | None]:
        """Returns the next (value, target, base) triple for this feature.

        neighbours_values holds only the neighbours that already have a value, so
        it may be empty (e.g. the first cell set when the world is created).
        """
        max_oscillation = self.options.max_oscillation

        if previous_feature_value is None or max_oscillation is None:
            value = self._pull_towards_neighbours(
                self._sample_from_statistics(), neighbours_values
            )

            return value, None, value

        previous = previous_feature_value.value
        target = previous_feature_value.target
        base = previous_feature_value.base

        # Keep drifting towards the same target until it is reached, then pick a
        # new one. Drawing a new target every step would make the value just
        # jitter around the mean; keeping it makes the value sweep the whole
        # distribution without ever settling.
        if target is not None:
            # Neighbours move too, so the target is kept within their reach
            target = self._pull_towards_neighbours(target, neighbours_values)

        if target is None or abs(target - previous) <= max_oscillation:
            target = self._pull_towards_neighbours(
                self._sample_around_base(base), neighbours_values
            )

        # The value itself is never snapped to the neighbours, so it never jumps
        # more than max_oscillation; it just keeps chasing a target near them
        step = random.uniform(0, max_oscillation)
        delta = max(-step, min(target - previous, step))

        return previous + delta, target, base

    @abstractmethod
    def sample(
        self,
        previous_feature_value: FeatureValue | None,
        neighbours_values: list[FeatureValue],
    ) -> FeatureValue[T]:
        pass
