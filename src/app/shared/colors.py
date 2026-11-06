import pygame

WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
BEEBAIT_COLOR = pygame.Color(255, 0, 255)
OCCUPIED_BEEBAIT_COLOR = pygame.Color(0, 0, 255)
SWARM_COLOR = pygame.Color(0, 0, 0)
BUTTON_COLOR = pygame.Color(220, 220, 220)

TEMPERATURE_PALETTE_MIN = 0.0
TEMPERATURE_PALETTE_MAX = 40.0
TEMPERATURE_PALETTE_STEP = 2.0

TEMPERATURE_PALETTE: tuple[pygame.Color, ...] = (
    pygame.Color(49, 0, 98),
    pygame.Color(72, 23, 183),
    pygame.Color(45, 75, 230),
    pygame.Color(20, 130, 250),
    pygame.Color(30, 175, 250),
    pygame.Color(50, 210, 230),
    pygame.Color(65, 228, 195),
    pygame.Color(80, 235, 150),
    pygame.Color(115, 240, 105),
    pygame.Color(160, 245, 70),
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
    pygame.Color(110, 0, 20),
)
