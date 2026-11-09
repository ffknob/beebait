from typing import override

from world.enums import FeatureName

from .inference import Inference
from .inference_model import InferenceModel


class InternalTemperatureRuleModel(InferenceModel):
    def __init__(
        self,
        min_colony_temperature: float = 33.0,
        max_colony_temperature: float = 36.0,
        confidence: float = 0.8,
    ):
        super().__init__(
            "internal_temperature_rule", (FeatureName.INTERNAL_TEMPERATURE,)
        )

        self.min_colony_temperature = min_colony_temperature
        self.max_colony_temperature = max_colony_temperature
        self.confidence = confidence

    @override
    def _predict(self, input: list[float]) -> Inference:
        # TODO: este modelo é apenas um mock baseado em uma regra fixa sobre a
        # temperatura interna. Deve ser substituído por um modelo de inferência
        # real, treinado com PyTorch (ou similar) e exportado para rodar na isca.
        (internal_temperature,) = input

        occupied = (
            self.min_colony_temperature
            <= internal_temperature
            <= self.max_colony_temperature
        )

        return Inference(self.name, occupied, self.confidence)
