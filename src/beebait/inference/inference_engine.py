from world.feature import FeatureValue

from .conclusion import Conclusion
from .conclusion_strategy import ConclusionStrategy
from .inference import Inference
from .inference_model import InferenceModel
from .weighted_average_strategy import WeightedAverageStrategy


class InferenceEngine:
    def __init__(
        self,
        models: list[tuple[InferenceModel, float]] | None = None,
        strategy: ConclusionStrategy | None = None,
    ):
        self._models = models if models else []
        self._strategy = strategy if strategy else WeightedAverageStrategy()

    @property
    def models(self) -> list[tuple[InferenceModel, float]]:
        return self._models

    def add_model(self, model: InferenceModel, weight: float = 1.0) -> None:
        self._models.append((model, weight))

    def submit(self, features: dict[str, FeatureValue]) -> Conclusion | None:
        weighted_inferences: list[tuple[Inference, float]] = [
            (inference, weight)
            for model, weight in self._models
            if (inference := model.infer(features)) is not None
        ]

        return self._strategy.conclude(weighted_inferences)
