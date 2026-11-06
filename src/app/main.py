import asyncio
import random

import pygame

from app.render.beebait import BeebaitRenderer, BeebaitRenderOptions
from app.render.beebait_info import BeebaitInfoRenderer, BeebaitInfoRenderOptions
from app.render.button import ButtonRenderer, ButtonRenderOptions
from app.render.clock import ClockRenderer, ClockRenderOptions
from app.render.legend import LegendRenderer, LegendRenderOptions
from app.render.swarm import SwarmRenderer, SwarmRenderOptions
from app.render.grid import GridRenderer, GridRenderOptions
from app.render.world import WorldRenderer, WorldRenderOptions
from beebait.beebait import Beebait
from beebait.sensor import ExternalTemperatureSensor, InternalTemperatureSensor, Sensor
from world.feature import RelativeHumidity, Temperature
from world.model import (
    FeatureOptions,
    FeatureStatistics,
    GridPosition,
    WorldParameters,
)
from swarm.swarm import Swarm
from world.world import World
from app.model import Button, LegendEntry
from app.shared.colors import (
    BEEBAIT_COLOR,
    BLACK,
    OCCUPIED_BEEBAIT_COLOR,
    SWARM_COLOR,
    TEMPERATURE_PALETTE,
    TEMPERATURE_PALETTE_MAX,
    TEMPERATURE_PALETTE_MIN,
    TEMPERATURE_PALETTE_STEP,
    WHITE,
)

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 900
INFO_PANEL_HEIGHT = 180
FPS = 60
TOTAL_BEEBAITS = 30
TOTAL_SWARMS = int(0.5 * TOTAL_BEEBAITS)
SWARM_MIN_START_DISTANCE = 3
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 32
BUTTON_MARGIN = 16
BUTTON_SPACING = 8
PAUSE_BUTTON_RECT = pygame.Rect(
    WINDOW_WIDTH - BUTTON_MARGIN - BUTTON_WIDTH,
    WINDOW_HEIGHT - INFO_PANEL_HEIGHT + BUTTON_MARGIN,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
STEP_BUTTON_RECT = PAUSE_BUTTON_RECT.move(0, BUTTON_HEIGHT + BUTTON_SPACING)
RESET_BUTTON_RECT = STEP_BUTTON_RECT.move(0, BUTTON_HEIGHT + BUTTON_SPACING)
STEP_ELAPSED_SECONDS = 1 / FPS


def create_world() -> World:
    temperature = Temperature(
        FeatureStatistics(min=5, max=40, mean=22, median=22),
        FeatureOptions(
            max_oscillation=0.05,
            concentration=2.0,
            max_neighbour_deviation=1.5,
            max_base_deviation=2.0,
            excursion_probability=0.02,
            max_excursion=7.0,
            daily_amplitude=6.0,
            daily_peak_hour=15.0,
        ),
    )
    relative_humidity = RelativeHumidity(
        FeatureStatistics(min=21, max=30, mean=25, median=26),
        FeatureOptions(
            max_oscillation=0.2,
            max_neighbour_deviation=2.0,
            max_base_deviation=3.0,
            daily_amplitude=2.0,
            daily_peak_hour=5.0,
        ),
    )

    world_parameters: WorldParameters = WorldParameters(columns=100, rows=100)

    return World(parameters=world_parameters, features={temperature, relative_humidity})


def get_grid_positions(world: World) -> list[GridPosition]:
    return [
        GridPosition(row, column)
        for row in range(world.parameters.rows)
        for column in range(world.parameters.columns)
    ]


def create_beebaits(world: World) -> list[Beebait]:
    sensors: list[Sensor] = [ExternalTemperatureSensor(), InternalTemperatureSensor()]
    positions = get_grid_positions(world)

    return [
        Beebait(id=id, position=position, sensors=sensors)
        for id, position in enumerate(
            random.sample(positions, min(TOTAL_BEEBAITS, len(positions))), start=1
        )
    ]


def create_swarms(world: World, beebaits: list[Beebait]) -> list[Swarm]:
    positions = [
        position
        for position in get_grid_positions(world)
        if all(
            max(
                abs(position.row - beebait.position.row),
                abs(position.column - beebait.position.column),
            )
            >= SWARM_MIN_START_DISTANCE
            for beebait in beebaits
        )
    ]

    return [
        Swarm(id=id, position=random.choice(positions))
        for id in range(1, TOTAL_SWARMS + 1)
    ]


def occupy_beebaits(swarms: list[Swarm], beebaits: list[Beebait]) -> None:
    for swarm in swarms:
        if swarm.settled:
            continue

        beebait = next(
            (
                beebait
                for beebait in beebaits
                if not beebait.occupied and swarm.is_adjacent_to(beebait.position)
            ),
            None,
        )
        if beebait is not None:
            beebait.occupy()
            swarm.settle()


async def cycle(
    world: World,
    beebaits: list[Beebait],
    swarms: list[Swarm],
    elapsed_seconds: float,
) -> None:
    await world.refresh(elapsed_seconds)

    for swarm in swarms:
        swarm.move(world.parameters)

    occupy_beebaits(swarms, beebaits)

    for beebait in beebaits:
        beebait.read_sensors(world.grid[beebait.position.row][beebait.position.column])


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
    beebait_render_options: BeebaitRenderOptions = BeebaitRenderOptions(surface=surface)

    return BeebaitRenderer(options=beebait_render_options, grid_renderer=grid_renderer)


def create_swarm_renderer(
    surface: pygame.Surface, grid_renderer: GridRenderer
) -> SwarmRenderer:
    swarm_render_options: SwarmRenderOptions = SwarmRenderOptions(surface=surface)

    return SwarmRenderer(options=swarm_render_options, grid_renderer=grid_renderer)


def create_beebait_info_renderer(surface: pygame.Surface) -> BeebaitInfoRenderer:
    beebait_info_render_options: BeebaitInfoRenderOptions = BeebaitInfoRenderOptions(
        surface=surface
    )

    return BeebaitInfoRenderer(options=beebait_info_render_options)


def create_clock_renderer(
    surface: pygame.Surface, grid_renderer: GridRenderer
) -> ClockRenderer:
    clock_render_options: ClockRenderOptions = ClockRenderOptions(surface=surface)

    return ClockRenderer(options=clock_render_options, grid_renderer=grid_renderer)


def create_legend_entries() -> list[list[LegendEntry]]:
    temperature_entries = [
        LegendEntry(TEMPERATURE_PALETTE[0], f"< {TEMPERATURE_PALETTE_MIN:.0f}º")
    ]
    for i, color in enumerate(TEMPERATURE_PALETTE[1:-1]):
        low = TEMPERATURE_PALETTE_MIN + i * TEMPERATURE_PALETTE_STEP
        high = low + TEMPERATURE_PALETTE_STEP
        temperature_entries.append(LegendEntry(color, f"{low:.0f}–{high:.0f}º"))
    temperature_entries.append(
        LegendEntry(TEMPERATURE_PALETTE[-1], f"> {TEMPERATURE_PALETTE_MAX:.0f}º")
    )

    marker_entries = [
        LegendEntry(BEEBAIT_COLOR, "Empty beebait"),
        LegendEntry(OCCUPIED_BEEBAIT_COLOR, "Occupied beebait"),
        LegendEntry(SWARM_COLOR, "Swarm"),
    ]

    return [list(reversed(temperature_entries)), marker_entries]


def create_legend_renderer(
    surface: pygame.Surface, clock_renderer: ClockRenderer
) -> LegendRenderer:
    legend_render_options: LegendRenderOptions = LegendRenderOptions(surface=surface)

    return LegendRenderer(options=legend_render_options, clock_renderer=clock_renderer)


def create_button_renderer(surface: pygame.Surface) -> ButtonRenderer:
    button_render_options: ButtonRenderOptions = ButtonRenderOptions(surface=surface)

    return ButtonRenderer(options=button_render_options)


async def create_simulation() -> tuple[World, list[Beebait], list[Swarm]]:
    world: World = create_world()
    beebaits: list[Beebait] = create_beebaits(world)
    swarms: list[Swarm] = create_swarms(world, beebaits)

    await cycle(world, beebaits, swarms, 0.0)

    return world, beebaits, swarms


async def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    paused = False
    elapsed_seconds = 0.0

    world, beebaits, swarms = await create_simulation()

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
    swarm_renderer: SwarmRenderer = create_swarm_renderer(world_surface, grid_renderer)
    clock_renderer: ClockRenderer = create_clock_renderer(world_surface, grid_renderer)
    legend_renderer: LegendRenderer = create_legend_renderer(
        world_surface, clock_renderer
    )
    legend_entries: list[list[LegendEntry]] = create_legend_entries()
    button_renderer: ButtonRenderer = create_button_renderer(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if PAUSE_BUTTON_RECT.collidepoint(event.pos):
                    paused = not paused
                elif STEP_BUTTON_RECT.collidepoint(event.pos):
                    paused = True
                    await cycle(world, beebaits, swarms, STEP_ELAPSED_SECONDS)
                elif RESET_BUTTON_RECT.collidepoint(event.pos):
                    world, beebaits, swarms = await create_simulation()

        screen.fill(WHITE)

        if not paused:
            await cycle(world, beebaits, swarms, elapsed_seconds)

        world_renderer.render(world)
        swarm_renderer.render(swarms)
        beebait_renderer.render(beebaits)
        beebait_info_renderer.render(beebaits)
        clock_renderer.render(world)
        legend_renderer.render(legend_entries)
        button_renderer.render(
            [
                Button(PAUSE_BUTTON_RECT, "Resume" if paused else "Pause"),
                Button(STEP_BUTTON_RECT, "Step"),
                Button(RESET_BUTTON_RECT, "Reset"),
            ]
        )

        pygame.display.flip()

        elapsed_seconds = clock.tick(FPS) / 1000

    pygame.quit()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
