from dataclasses import dataclass, field

from .inference import Inference


@dataclass(frozen=True)
class Conclusion:
    occupied: bool
    confidence: float
    inferences: tuple[Inference, ...] = field(default_factory=tuple)
