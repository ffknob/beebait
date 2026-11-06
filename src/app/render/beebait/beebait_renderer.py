from typing import override

import pygame

from app.render import Renderer
from app.render.grid import GridRenderer
from beebait.beebait import Beebait

from .beebait_render_options import BeebaitRenderOptions


class BeebaitRenderer(Renderer[list[Beebait]]):
    def __init__(
        self, options: BeebaitRenderOptions, grid_renderer: GridRenderer
    ) -> None:
        super().__init__(options)

        self.options = options
        self.grid_renderer = grid_renderer

    @override
    def render(self, object: list[Beebait]) -> None:
        beebaits: list[Beebait] = object

        if not self.grid_renderer.cells_coordinates:
            return

        for beebait in beebaits:
            cell_rect: pygame.Rect = self.grid_renderer.cells_coordinates[
                beebait.position.row
            ][beebait.position.column]

            color: pygame.Color = (
                self.options.occupied_color if beebait.occupied else self.options.color
            )

            pygame.draw.rect(self.options.surface, color, cell_rect)
