from abc import ABC, abstractmethod

from world.enums import FeatureName
from world.feature import FeatureValue

from .inference import Inference


class InferenceModel(ABC):
    def __init__(self, name: str, required_features: tuple[FeatureName, ...]):
        self.name = name
        self.required_features = required_features

    def _extract_input(self, features: dict[str, FeatureValue]) -> list[float]:
        return [float(features[name].value) for name in self.required_features]

    @abstractmethod
    def _predict(self, input: list[float]) -> Inference:
        pass

    def infer(self, features: dict[str, FeatureValue]) -> Inference | None:
        if any(name not in features for name in self.required_features):
            return None

        return self._predict(self._extract_input(features))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, required_features={self.required_features})"
