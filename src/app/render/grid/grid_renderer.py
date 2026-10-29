import pygame

from app.model.grid import Grid

from app.render import Renderer
from .grid_render_options import GridRenderOptions


class GridRenderer(Renderer[Grid]):
    def __init__(self, options: GridRenderOptions) -> None:
        self.options = options

    def _calculate_margins(self, grid: Grid) -> tuple[int, int]:
        horizontal_margin: int = int(
            (self.options.surface.get_width() - (self.options.cell_size * grid.columns))
            / 2
        )
        vertical_margin: int = int(
            (self.options.surface.get_height() - (self.options.cell_size * grid.rows))
            / 2
        )

        return horizontal_margin, vertical_margin

    def _render_horizontal_lines(self, grid: Grid) -> None:
        horizontal_margin, vertical_margin = self._calculate_margins(grid)

        for i in range(grid.rows + 1):
            start_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin,
                horizontal_margin + (i * self.options.cell_size),
            )
            end_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin + (self.options.cell_size * grid.columns),
                horizontal_margin + (i * self.options.cell_size),
            )

            pygame.draw.line(
                self.options.surface,
                self.options.line_color,
                start_pos,
                end_pos,
                self.options.line_width,
            )

    def _render_vertical_lines(self, grid: Grid) -> None:
        horizontal_margin, vertical_margin = self._calculate_margins(grid)

        for i in range(grid.columns + 1):
            start_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin + (i * self.options.cell_size), vertical_margin
            )
            end_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin + (i * self.options.cell_size),
                vertical_margin + (self.options.cell_size * grid.rows),
            )

            pygame.draw.line(
                self.options.surface,
                self.options.line_color,
                start_pos,
                end_pos,
                self.options.line_width,
            )

    def render(self, object: Grid) -> None:
        grid: Grid = object

        self._render_horizontal_lines(grid)
        self._render_vertical_lines(grid)
