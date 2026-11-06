from dataclasses import dataclass, field

import pygame

from app.render import RenderOptions
from app.shared.colors import BLACK


@dataclass(frozen=True)
class LegendRenderOptions(RenderOptions):
    surface: pygame.Surface
    text_color: pygame.Color = field(default_factory=lambda: pygame.Color(BLACK))
    border_color: pygame.Color = field(default_factory=lambda: pygame.Color(BLACK))
    font_name: str = "dejavusans,liberationsans,arial"
    font_size: int = 12
    swatch_size: int = 12
    swatch_spacing: int = 6
    line_spacing: int = 4
    group_spacing: int = 12
    top_spacing: int = 16
