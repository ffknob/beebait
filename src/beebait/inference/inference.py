from dataclasses import dataclass


@dataclass(frozen=True)
class Inference:
    model_name: str
    occupied: bool
    confidence: float
