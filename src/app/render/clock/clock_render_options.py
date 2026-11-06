from dataclasses import dataclass, field

import pygame

from app.render import RenderOptions
from app.shared.colors import BLACK


@dataclass(frozen=True)
class ClockRenderOptions(RenderOptions):
    surface: pygame.Surface
    text_color: pygame.Color = field(default_factory=lambda: pygame.Color(BLACK))
    font_name: str = "dejavusans,liberationsans,arial"
    font_size: int = 28
    padding: int = 16
