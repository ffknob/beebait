from typing import override

import pygame

from app.model import Grid
from app.render import Renderer

from .grid_render_options import GridRenderOptions


class GridRenderer(Renderer[Grid]):
    def __init__(self, options: GridRenderOptions) -> None:
        self.options = options

        self.horizontal_margin: float | None = None
        self.vertical_margin: float | None = None

        self.cell_width: int | None = None
        self.cell_height: int | None = None

        self.horizontal_lines: list[tuple[pygame.Vector2, pygame.Vector2]] = []
        self.vertical_lines: list[tuple[pygame.Vector2, pygame.Vector2]] = []

        self.cells_coordinates: list[list[pygame.Rect]] = []

    def _recalculate_after_surface_resizing(self, grid: Grid) -> None:
        self.horizontal_margin = None
        self.vertical_margin = None

        self.cell_width = None
        self.cell_height = None

        self.horizontal_lines = []
        self.vertical_lines = []

        self.cells_coordinates = []

        self._calculate_margins(grid)
        self._calculate_cell_dimensions(grid)
        self._calculate_horizontal_lines(grid)
        self._calculate_vertical_lines(grid)
        self._calculate_cells_coordinates(grid)

    def _calculate_margins(self, grid: Grid) -> tuple[float, float]:
        if self.horizontal_margin is not None and self.vertical_margin is not None:
            return self.horizontal_margin, self.vertical_margin

        horizontal_margin = (
            self.options.surface.get_width() * self.options.horizontal_margin_percentage
        )
        vertical_margin = (
            self.options.surface.get_height() * self.options.vertical_margin_percentage
        )

        self.horizontal_margin = horizontal_margin
        self.vertical_margin = vertical_margin

        return horizontal_margin, vertical_margin

    def _calculate_cell_dimensions(self, grid: Grid) -> tuple[int, int]:
        if self.cell_width is not None and self.cell_height is not None:
            return self.cell_width, self.cell_height

        surface_width, surface_height = self.options.surface.get_size()
        horizontal_margin, vertical_margin = self._calculate_margins(grid)

        cell_width = int((surface_width - (2 * horizontal_margin)) // grid.columns)
        cell_height = int((surface_height - (2 * vertical_margin)) // grid.rows)

        return cell_width, cell_height

    def _calculate_horizontal_lines(
        self, grid: Grid
    ) -> list[tuple[pygame.Vector2, pygame.Vector2]]:
        cell_width, cell_height = self._calculate_cell_dimensions(grid)
        horizontal_margin, vertical_margin = self._calculate_margins(grid)

        for i in range(grid.rows + 1):
            start_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin,
                vertical_margin + (i * cell_height),
            )
            end_pos: pygame.Vector2 = pygame.Vector2(
                horizontal_margin + (cell_width * grid.columns),
                vertical_margin + (i * cell_height),
            )

            self.horizontal_lines.append((start_pos, end_pos))

        return self.horizontal_lines

    def _calculate_vertical_lines(
        self, grid: Grid
    ) -> list[tuple[pygame.Vector2, pygame.Vector2]]:
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

            self.vertical_lines.append((start_pos, end_pos))

        return self.vertical_lines

    def _calculate_cells_coordinates(self, grid: Grid) -> list[list[pygame.Rect]]:
        cell_width, cell_height = self._calculate_cell_dimensions(grid)
        horizontal_margin, vertical_margin = self._calculate_margins(grid)

        cells_coordinates: list[list[pygame.Rect]] = []

        for row in range(grid.rows):
            row_dimensions: list[pygame.Rect] = []
            for column in range(grid.columns):
                cell_rect: pygame.Rect = pygame.Rect(
                    horizontal_margin + (column * cell_width),
                    vertical_margin + (row * cell_height),
                    cell_width,
                    cell_height,
                )
                row_dimensions.append(cell_rect)
                cells_coordinates.append(row_dimensions)

        self.cells_coordinates = cells_coordinates

        return cells_coordinates

    def _render_horizontal_lines(self, grid: Grid) -> None:
        for horizontal_line in self.horizontal_lines:
            start_pos, end_pos = horizontal_line

            pygame.draw.line(
                self.options.surface,
                self.options.line_color,
                start_pos,
                end_pos,
                self.options.line_width,
            )

    def _render_vertical_lines(self, grid: Grid) -> None:
        for vertical_line in self.vertical_lines:
            start_pos, end_pos = vertical_line

            pygame.draw.line(
                self.options.surface,
                self.options.line_color,
                start_pos,
                end_pos,
                self.options.line_width,
            )

    def _render_cells(self, grid: Grid) -> None:
        for row in range(grid.rows):
            for column in range(grid.columns):
                cell_rect: pygame.Rect = self.cells_coordinates[row][column]

                pygame.draw.rect(
                    self.options.surface,
                    self.options.cell_color,
                    cell_rect,
                )

    @override
    def render(self, object: Grid) -> None:
        grid: Grid = object

        if not self.horizontal_lines:
            self._calculate_horizontal_lines(grid)

        if not self.vertical_lines:
            self._calculate_vertical_lines(grid)

        self._render_horizontal_lines(grid)
        self._render_vertical_lines(grid)
        self._render_cells(grid)
