from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class Button:
    rect: pygame.Rect
    label: str
