from abc import ABC, abstractmethod
from typing import TypeVar

from app.render import RenderOptions

T = TypeVar("T")


class Renderer[T](ABC):
    def __init__(self, options: RenderOptions) -> None:
        super().__init__()

        self.options = options

    @abstractmethod
    def render(self, object: T) -> None:
        pass
