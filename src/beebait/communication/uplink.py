import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Uplink:
    timestamp: int
    beebait_id: int
    occupied: bool
    confidence: float
    internal_temperature: float | None
    external_temperature: float | None
    row: int
    column: int
    simulated_hour: float
    ground_truth_occupied: bool

    def to_json(self) -> str:
        payload = asdict(self)
        payload["beebait_id"] = str(self.beebait_id)
        payload["occupied"] = int(self.occupied)
        payload["ground_truth_occupied"] = int(self.ground_truth_occupied)

        return json.dumps(
            {key: value for key, value in payload.items() if value is not None}
        )
