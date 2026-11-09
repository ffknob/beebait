from typing import override

from .conclusion import Conclusion
from .conclusion_strategy import ConclusionStrategy
from .inference import Inference


class WeightedAverageStrategy(ConclusionStrategy):
    def __init__(self, occupied_threshold: float = 0.5):
        self.occupied_threshold = occupied_threshold

    @override
    def conclude(
        self, weighted_inferences: list[tuple[Inference, float]]
    ) -> Conclusion | None:
        total_weight = sum(weight for _, weight in weighted_inferences)
        if total_weight <= 0:
            return None

        probability = (
            sum(
                weight
                * (
                    inference.confidence
                    if inference.occupied
                    else 1 - inference.confidence
                )
                for inference, weight in weighted_inferences
            )
            / total_weight
        )

        occupied = probability >= self.occupied_threshold

        return Conclusion(
            occupied=occupied,
            confidence=probability if occupied else 1 - probability,
            inferences=tuple(inference for inference, _ in weighted_inferences),
        )
