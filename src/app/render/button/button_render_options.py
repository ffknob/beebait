from dataclasses import dataclass, field

import pygame

from app.render import RenderOptions
from app.shared.colors import BLACK, BUTTON_COLOR


@dataclass(frozen=True)
class ButtonRenderOptions(RenderOptions):
    surface: pygame.Surface
    color: pygame.Color = field(default_factory=lambda: pygame.Color(BUTTON_COLOR))
    border_color: pygame.Color = field(default_factory=lambda: pygame.Color(BLACK))
    text_color: pygame.Color = field(default_factory=lambda: pygame.Color(BLACK))
    font_name: str = "dejavusans,liberationsans,arial"
    font_size: int = 14
    border_width: int = 1
    border_radius: int = 4
