import asyncio
import random

import pygame

from app.render.beebait import BeebaitRenderer, BeebaitRenderOptions
from app.render.beebait_info import BeebaitInfoRenderer, BeebaitInfoRenderOptions
from app.render.grid import GridRenderer, GridRenderOptions
from app.render.world import WorldRenderer, WorldRenderOptions
from beebait.beebait import Beebait
from beebait.model import GridPosition
from world.enums import FeatureName
from world.feature import FeatureValue, RelativeHumidity, Temperature
from world.model import FeatureOptions, FeatureStatistics, WorldParameters
from world.world import World
from app.shared.colors import BLACK, WHITE

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 900
INFO_PANEL_HEIGHT = 180
FPS = 60
TOTAL_BEEBAITS = 30
OCCUPIED_BEEBAIT_PROBABILITY = 0.2


def create_world() -> World:
    temperature = Temperature(
        FeatureStatistics(min=5, max=40, mean=22, median=22),
        FeatureOptions(
            max_oscillation=0.05,
            concentration=2.0,
            max_neighbour_deviation=1.5,
            max_base_deviation=2.0,
        ),
    )
    relative_humidity = RelativeHumidity(
        FeatureStatistics(min=21, max=30, mean=25, median=26),
        FeatureOptions(
            max_oscillation=0.2, max_neighbour_deviation=2.0, max_base_deviation=3.0
        ),
    )

    world_parameters: WorldParameters = WorldParameters(columns=100, rows=100)

    return World(parameters=world_parameters, features={temperature, relative_humidity})


def create_beebaits(world: World) -> list[Beebait]:
    positions = [
        GridPosition(row, column)
        for row in range(world.parameters.rows)
        for column in range(world.parameters.columns)
    ]

    return [
        Beebait(
            id=id,
            position=position,
            occupied=random.random() < OCCUPIED_BEEBAIT_PROBABILITY,
        )
        for id, position in enumerate(
            random.sample(positions, min(TOTAL_BEEBAITS, len(positions))), start=1
        )
    ]


def update_beebaits_readings(world: World, beebaits: list[Beebait]) -> None:
    for beebait in beebaits:
        cell = world.grid[beebait.position.row][beebait.position.column]
        external_temperature = cell.features_values.get(FeatureName.TEMPERATURE)
        if external_temperature is None:
            continue

        internal_temperature = (
            random.gauss(34.5, 0.3)
            if beebait.occupied
            else external_temperature.value + random.gauss(0.5, 0.3)
        )

        beebait.set_feature_value(
            FeatureValue(FeatureName.TEMPERATURE, external_temperature.value)
        )
        beebait.set_feature_value(
            FeatureValue(FeatureName.INTERNAL_TEMPERATURE, internal_temperature)
        )


def create_grid_renderer(surface: pygame.Surface) -> GridRenderer:
    grid_render_options: GridRenderOptions = GridRenderOptions(
        surface=surface,
        background_color=WHITE,
        line_color=BLACK,
        vertical_margin_percentage=0.05,
    )

    return GridRenderer(options=grid_render_options)


def create_world_render(
    surface: pygame.Surface, grid_renderer: GridRenderer
) -> WorldRenderer:
    world_render_options: WorldRenderOptions = WorldRenderOptions(surface=surface)

    return WorldRenderer(options=world_render_options, grid_renderer=grid_renderer)


def create_beebait_renderer(
    surface: pygame.Surface, grid_renderer: GridRenderer
) -> BeebaitRenderer:
    beebait_render_options: BeebaitRenderOptions = BeebaitRenderOptions(
        surface=surface
    )

    return BeebaitRenderer(options=beebait_render_options, grid_renderer=grid_renderer)


def create_beebait_info_renderer(surface: pygame.Surface) -> BeebaitInfoRenderer:
    beebait_info_render_options: BeebaitInfoRenderOptions = BeebaitInfoRenderOptions(
        surface=surface
    )

    return BeebaitInfoRenderer(options=beebait_info_render_options)


async def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    world: World = create_world()
    beebaits: list[Beebait] = create_beebaits(world)

    world_surface = screen.subsurface(
        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT - INFO_PANEL_HEIGHT)
    )
    info_surface = screen.subsurface(
        (0, WINDOW_HEIGHT - INFO_PANEL_HEIGHT, WINDOW_WIDTH, INFO_PANEL_HEIGHT)
    )

    grid_renderer: GridRenderer = create_grid_renderer(world_surface)
    world_renderer: WorldRenderer = create_world_render(world_surface, grid_renderer)
    beebait_renderer: BeebaitRenderer = create_beebait_renderer(
        world_surface, grid_renderer
    )
    beebait_info_renderer: BeebaitInfoRenderer = create_beebait_info_renderer(
        info_surface
    )

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        await world.refresh()
        update_beebaits_readings(world, beebaits)

        world_renderer.render(world)
        beebait_renderer.render(beebaits)
        beebait_info_renderer.render(beebaits)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
