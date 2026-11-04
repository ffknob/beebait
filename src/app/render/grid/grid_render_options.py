from dataclasses import dataclass, field

import pygame

from app.render import RenderOptions
from app.shared.colors import BLACK, WHITE


@dataclass(frozen=True)
class GridRenderOptions(RenderOptions):
    surface: pygame.Surface
    background_color: pygame.Color = field(default_factory=lambda: pygame.Color(WHITE))
    line_color: pygame.Color = field(default_factory=lambda: pygame.Color(BLACK))
    line_width: int = 1
    horizontal_margin_percentage: float = 0.1
    vertical_margin_percentage: float = 0.1
