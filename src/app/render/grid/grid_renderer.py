import pygame

from app.model.grid import Grid

from app.render import Renderer
from .grid_render_options import GridRenderOptions


class GridRenderer(Renderer[Grid]):
    def __init__(self, options: GridRenderOptions) -> None:
        self.options = options

    def _calculate_cell_dimensions(self, grid: Grid) -> tuple[int, int]:
        cell_width: int = self.options.surface.get_width() // grid.columns
        cell_height: int = self.options.surface.get_height() // grid.rows

        return cell_width, cell_height

    def _calculate_margins(self, grid: Grid) -> tuple[float, float]:
        horizontal_margin = (
            self.options.surface.get_width() * self.options.horizontal_margin_percentage
        )
        vertical_margin = (
            self.options.surface.get_height() * self.options.vertical_margin_percentage
        )

        return horizontal_margin, vertical_margin

    def _render_horizontal_lines(self, grid: Grid) -> None:
        cell_width, cell_height = self._calculate_cell_dimensions(grid)
        horizontal_margin, vertical_margin = self._calculate_margins(grid)

        for i in range(grid.rows + 1):
            start_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin,
                horizontal_margin + (i * cell_height),
            )
            end_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin + (cell_width * grid.columns),
                horizontal_margin + (i * cell_height),
            )

            pygame.draw.line(
                self.options.surface,
                self.options.line_color,
                start_pos,
                end_pos,
                self.options.line_width,
            )

    def _render_vertical_lines(self, grid: Grid) -> None:
        cell_width, cell_height = self._calculate_cell_dimensions(grid)
        horizontal_margin, vertical_margin = self._calculate_margins(grid)

        for i in range(grid.columns + 1):
            start_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin + (i * cell_width), vertical_margin
            )
            end_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin + (i * cell_width),
                vertical_margin + (cell_height * grid.rows),
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
        # self._render_vertical_lines(grid)
