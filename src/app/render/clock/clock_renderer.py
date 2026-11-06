from typing import override

from app.render import Renderer
from app.render.grid import GridRenderer
from world.world import World

import pygame

from .clock_render_options import ClockRenderOptions


class ClockRenderer(Renderer[World]):
    def __init__(
        self, options: ClockRenderOptions, grid_renderer: GridRenderer
    ) -> None:
        super().__init__(options)

        self.options = options
        self.grid_renderer = grid_renderer

        self.font = pygame.font.SysFont(options.font_name, options.font_size)
        self.rect: pygame.Rect | None = None

    @override
    def render(self, object: World) -> None:
        world: World = object

        if not self.grid_renderer.vertical_lines:
            return

        grid_top_right, _ = self.grid_renderer.vertical_lines[-1]

        hours, minutes = divmod(int(world.hour * 60), 60)
        text = self.font.render(
            f"{hours:02d}:{minutes:02d}", True, self.options.text_color
        )

        self.rect = self.options.surface.blit(
            text, (grid_top_right.x + self.options.padding, grid_top_right.y)
        )
