import pygame

from app.model import RenderedCell, RenderedGrid
from app.render import Renderer
from app.render.grid import GridRenderer
from world.world import Cell, World

from .world_render_options import WorldRenderOptions


class WorldRenderer(Renderer[World]):
    def __init__(
        self, options: WorldRenderOptions, grid_renderer: GridRenderer
    ) -> None:
        super().__init__(options)

        self.grid_renderer = grid_renderer
        self.rendered_grid: RenderedGrid | None = None

    def _map_temperature_to_color(self, cell) -> tuple[int, int, int]:
        return pygame.Color(0, 0, 0)

    def _map_cell_to_rendered_cell(self, cell: Cell) -> RenderedCell:
        return RenderedCell(
            coordinates=None, color=self._map_temperature_to_color(cell)
        )

    def _create_grid(
        self, columns: int, rows: int, grid: list[list[Cell]]
    ) -> RenderedGrid:
        rendered_cells: list[list[RenderedCell]] = []
        for r, row in enumerate(grid):
            rendered_cells.append([])
            for c, cell in enumerate(row):
                rendered_cell: RenderedCell = self._map_cell_to_rendered_cell(cell=cell)
                rendered_cells[r].append(rendered_cell)

        self.rendered_grid = RenderedGrid(
            rows=rows, columns=columns, cells=rendered_cells
        )

        return self.rendered_grid

    def render(self, object: World) -> None:
        world: World = object

        rendered_grid: RenderedGrid = self._create_grid(
            world.parameters.columns, world.parameters.rows, world.grid
        )

        self.grid_renderer.render(rendered_grid)
