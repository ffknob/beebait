from typing import override

import pygame

from app.render import Renderer
from app.render.grid import GridRenderer
from swarm.swarm import Swarm

from .swarm_render_options import SwarmRenderOptions


class SwarmRenderer(Renderer[list[Swarm]]):
    def __init__(
        self, options: SwarmRenderOptions, grid_renderer: GridRenderer
    ) -> None:
        super().__init__(options)

        self.options = options
        self.grid_renderer = grid_renderer

    @override
    def render(self, object: list[Swarm]) -> None:
        swarms: list[Swarm] = object

        if not self.grid_renderer.cells_coordinates:
            return

        for swarm in swarms:
            if swarm.settled:
                continue

            cell_rect: pygame.Rect = self.grid_renderer.cells_coordinates[
                swarm.position.row
            ][swarm.position.column]

            pygame.draw.rect(self.options.surface, self.options.color, cell_rect)
