import pygame

WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
BEEBAIT_COLOR = pygame.Color(255, 0, 255)
OCCUPIED_BEEBAIT_COLOR = pygame.Color(0, 0, 255)

TEMPERATURE_PALETTE_MIN = 0.0
TEMPERATURE_PALETTE_MAX = 40.0
TEMPERATURE_PALETTE_STEP = 2.0

# Cold → hot: one color below the minimum, one per step in between and one above the maximum
TEMPERATURE_PALETTE: tuple[pygame.Color, ...] = (
    pygame.Color(49, 0, 98),  # < 0
    pygame.Color(72, 23, 183),  # [0, 2)
    pygame.Color(45, 75, 230),  # [2, 4)
    pygame.Color(20, 130, 250),  # [4, 6)
    pygame.Color(30, 175, 250),  # [6, 8)
    pygame.Color(50, 210, 230),  # [8, 10)
    pygame.Color(65, 228, 195),  # [10, 12)
    pygame.Color(80, 235, 150),  # [12, 14)
    pygame.Color(115, 240, 105),  # [14, 16)
    pygame.Color(160, 245, 70),  # [16, 18)
    pygame.Color(205, 245, 50),  # [18, 20)
    pygame.Color(240, 240, 45),  # [20, 22)
    pygame.Color(255, 220, 40),  # [22, 24)
    pygame.Color(255, 195, 35),  # [24, 26)
    pygame.Color(255, 170, 30),  # [26, 28)
    pygame.Color(255, 140, 25),  # [28, 30)
    pygame.Color(250, 110, 20),  # [30, 32)
    pygame.Color(240, 80, 15),  # [32, 34)
    pygame.Color(225, 50, 10),  # [34, 36)
    pygame.Color(200, 25, 10),  # [36, 38)
    pygame.Color(165, 10, 10),  # [38, 40]
    pygame.Color(110, 0, 20),  # > 40
)
