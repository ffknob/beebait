from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class GridCell:
    coordinates: pygame.Rect
    color: tuple[int, int, int]
