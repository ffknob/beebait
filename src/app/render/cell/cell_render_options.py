from dataclasses import dataclass

import pygame

from app.render import RenderOptions

# 25 colors, one per 2 °C interval from -10 °C to +40 °C (cold → hot)
TEMPERATURE_PALETTE: tuple[pygame.Color, ...] = (
    pygame.Color(49, 0, 98),  # [-10, -8)
    pygame.Color(69, 0, 139),  # [-8, -6)
    pygame.Color(72, 23, 183),  # [-6, -4)
    pygame.Color(59, 57, 219),  # [-4, -2)
    pygame.Color(33, 94, 240),  # [-2, 0)
    pygame.Color(20, 130, 250),  # [0, 2)
    pygame.Color(25, 165, 250),  # [2, 4)
    pygame.Color(40, 195, 240),  # [4, 6)
    pygame.Color(60, 220, 220),  # [6, 8)
    pygame.Color(70, 230, 180),  # [8, 10)
    pygame.Color(90, 235, 140),  # [10, 12)
    pygame.Color(125, 240, 100),  # [12, 14)
    pygame.Color(165, 245, 70),  # [14, 16)
    pygame.Color(205, 245, 50),  # [16, 18)
    pygame.Color(240, 240, 45),  # [18, 20)
    pygame.Color(255, 220, 40),  # [20, 22)
    pygame.Color(255, 195, 35),  # [22, 24)
    pygame.Color(255, 170, 30),  # [24, 26)
    pygame.Color(255, 140, 25),  # [26, 28)
    pygame.Color(250, 110, 20),  # [28, 30)
    pygame.Color(240, 80, 15),  # [30, 32)
    pygame.Color(225, 50, 10),  # [32, 34)
    pygame.Color(200, 25, 10),  # [34, 36)
    pygame.Color(165, 10, 10),  # [36, 38)
    pygame.Color(125, 0, 15),  # [38, 40]
)
NO_TEMPERATURE_COLOR = pygame.Color(128, 128, 128)


@dataclass(frozen=True)
class CellRenderOptions(RenderOptions):
    temperature_palette: tuple[pygame.Color, ...] = TEMPERATURE_PALETTE
    no_measurement_color: pygame.Color = NO_TEMPERATURE_COLOR
    min_temperature: float = -10.0
    max_temperature: float = 40.0
    temperature_step: float = 2.0
