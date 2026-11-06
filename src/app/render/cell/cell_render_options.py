from dataclasses import dataclass

import pygame

from app.render import RenderOptions

TEMPERATURE_PALETTE: tuple[pygame.Color, ...] = (
    pygame.Color(49, 0, 98),
    pygame.Color(69, 0, 139),
    pygame.Color(72, 23, 183),
    pygame.Color(59, 57, 219),
    pygame.Color(33, 94, 240),
    pygame.Color(20, 130, 250),
    pygame.Color(25, 165, 250),
    pygame.Color(40, 195, 240),
    pygame.Color(60, 220, 220),
    pygame.Color(70, 230, 180),
    pygame.Color(90, 235, 140),
    pygame.Color(125, 240, 100),
    pygame.Color(165, 245, 70),
    pygame.Color(205, 245, 50),
    pygame.Color(240, 240, 45),
    pygame.Color(255, 220, 40),
    pygame.Color(255, 195, 35),
    pygame.Color(255, 170, 30),
    pygame.Color(255, 140, 25),
    pygame.Color(250, 110, 20),
    pygame.Color(240, 80, 15),
    pygame.Color(225, 50, 10),
    pygame.Color(200, 25, 10),
    pygame.Color(165, 10, 10),
    pygame.Color(125, 0, 15),
)
NO_TEMPERATURE_COLOR = pygame.Color(128, 128, 128)


@dataclass(frozen=True)
class CellRenderOptions(RenderOptions):
    temperature_palette: tuple[pygame.Color, ...] = TEMPERATURE_PALETTE
    no_measurement_color: pygame.Color = NO_TEMPERATURE_COLOR
    min_temperature: float = -10.0
    max_temperature: float = 40.0
    temperature_step: float = 2.0
