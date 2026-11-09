from abc import ABC, abstractmethod

from .uplink import Uplink


class Transmitter(ABC):
    @abstractmethod
    def transmit(self, uplink: Uplink) -> None:
        pass

    def close(self) -> None:
        pass
