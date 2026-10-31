import pygame

from app.model import Grid, GridCell
from app.render import Renderer
from app.render.grid import GridRenderer
from world.world import World

from .world_render_options import WorldRenderOptions


class WorldRenderer(Renderer[World]):
    def __init__(
        self, options: WorldRenderOptions, grid_renderer: GridRenderer
    ) -> None:
        super().__init__(options)

        self.grid_renderer = grid_renderer
        self.grid: Grid | None = None

    def _create_grid(self, columns: int, rows: int) -> Grid:
        self.grid = Grid(columns=columns, rows=rows, grid_cells=grid_cells)

        return self.grid

    def render(self, object: World) -> None:
        world: World = object

        grid: Grid = self._create_grid(world.parameters.columns, world.parameters.rows)

        self.grid_renderer.render(grid)
