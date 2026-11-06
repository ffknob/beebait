from dataclasses import dataclass, field

import pygame

from app.render import RenderOptions
from app.shared.colors import SWARM_COLOR


@dataclass(frozen=True)
class SwarmRenderOptions(RenderOptions):
    surface: pygame.Surface
    color: pygame.Color = field(default_factory=lambda: pygame.Color(SWARM_COLOR))
