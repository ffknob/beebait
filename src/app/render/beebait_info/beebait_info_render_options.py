from dataclasses import dataclass, field

import pygame

from app.render import RenderOptions
from app.shared.colors import BLACK, OCCUPIED_BEEBAIT_COLOR


@dataclass(frozen=True)
class BeebaitInfoRenderOptions(RenderOptions):
    surface: pygame.Surface
    text_color: pygame.Color = field(default_factory=lambda: pygame.Color(BLACK))
    occupied_text_color: pygame.Color = field(
        default_factory=lambda: pygame.Color(OCCUPIED_BEEBAIT_COLOR)
    )
    font_name: str = "dejavusans,liberationsans,arial"
    font_size: int = 14
    line_spacing: int = 2
    column_width: int = 250
    horizontal_margin_percentage: float = 0.1
