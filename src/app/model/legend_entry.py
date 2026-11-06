from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class LegendEntry:
    color: pygame.Color
    label: str
