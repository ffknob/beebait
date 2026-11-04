from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class RenderedCell:
    coordinates: pygame.Rect | None = None
    color: pygame.Color | None = None
