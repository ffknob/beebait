from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class RenderOptions:
    surface: pygame.Surface
