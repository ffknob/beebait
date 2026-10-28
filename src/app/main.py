import asyncio

import pygame

from world.feature import RelativeHumidity, Temperature
from world.model import FeatureStatistics
from world.world import World
from app.render.world import WorldRenderer, WorldRenderOptions

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
BACKGROUND = "white"


def create_world() -> World:
    temperature = Temperature(FeatureStatistics(min=21, max=30, mean=25, median=26))
    relative_humidity = RelativeHumidity(
        FeatureStatistics(min=21, max=30, mean=25, median=26)
    )

    return World(features={temperature, relative_humidity})


def create_world_render() -> WorldRenderer:
    world_render_options: WorldRenderOptions = WorldRenderOptions()

    return WorldRenderer(options=world_render_options)


async def run():
    world: World = create_world()
    world_renderer: WorldRenderer = create_world_render()

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(BACKGROUND)

        await world.refresh()
        world_renderer.render(screen, world)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
