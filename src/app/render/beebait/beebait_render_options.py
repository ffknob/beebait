from dataclasses import dataclass, field

import pygame

from app.render import RenderOptions
from app.shared.colors import BEEBAIT_COLOR, OCCUPIED_BEEBAIT_COLOR


@dataclass(frozen=True)
class BeebaitRenderOptions(RenderOptions):
    surface: pygame.Surface
    color: pygame.Color = field(default_factory=lambda: pygame.Color(BEEBAIT_COLOR))
    occupied_color: pygame.Color = field(
        default_factory=lambda: pygame.Color(OCCUPIED_BEEBAIT_COLOR)
    )
