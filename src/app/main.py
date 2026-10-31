import asyncio

import pygame

from app.render.grid import GridRenderer, GridRenderOptions
from app.render.world import WorldRenderer, WorldRenderOptions
from world.feature import RelativeHumidity, Temperature
from world.model import FeatureStatistics, WorldParameters
from world.world import World

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
BACKGROUND = "white"


def create_world() -> World:
    temperature = Temperature(FeatureStatistics(min=21, max=30, mean=25, median=26))
    relative_humidity = RelativeHumidity(
        FeatureStatistics(min=21, max=30, mean=25, median=26)
    )

    world_parameters: WorldParameters = WorldParameters(columns=100, rows=100)

    return World(parameters=world_parameters, features={temperature, relative_humidity})


def create_grid_renderer(surface: pygame.Surface) -> GridRenderer:
    grid_render_options: GridRenderOptions = GridRenderOptions(
        surface=surface, line_color="gray60"
    )

    return GridRenderer(options=grid_render_options)


def create_world_render(surface: pygame.Surface) -> WorldRenderer:
    world_render_options: WorldRenderOptions = WorldRenderOptions(surface=surface)

    return WorldRenderer(
        options=world_render_options,
        grid_renderer=create_grid_renderer(surface=surface),
    )


async def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    world: World = create_world()
    world_renderer: WorldRenderer = create_world_render(screen)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND)

        await world.refresh()
        world_renderer.render(world)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
