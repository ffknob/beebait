from abc import ABC, abstractmethod

from .conclusion import Conclusion
from .inference import Inference


class ConclusionStrategy(ABC):
    @abstractmethod
    def conclude(
        self, weighted_inferences: list[tuple[Inference, float]]
    ) -> Conclusion | None:
        pass
