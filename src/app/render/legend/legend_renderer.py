from typing import override

import pygame

from app.model import LegendEntry
from app.render import Renderer
from app.render.clock import ClockRenderer

from .legend_render_options import LegendRenderOptions


class LegendRenderer(Renderer[list[list[LegendEntry]]]):
    def __init__(
        self, options: LegendRenderOptions, clock_renderer: ClockRenderer
    ) -> None:
        super().__init__(options)

        self.options = options
        self.clock_renderer = clock_renderer

        self.font = pygame.font.SysFont(options.font_name, options.font_size)

    @override
    def render(self, object: list[list[LegendEntry]]) -> None:
        groups: list[list[LegendEntry]] = object

        if self.clock_renderer.rect is None:
            return

        x = self.clock_renderer.rect.left
        y = self.clock_renderer.rect.bottom + self.options.top_spacing
        line_height = (
            max(self.font.get_linesize(), self.options.swatch_size)
            + self.options.line_spacing
        )

        for group in groups:
            for entry in group:
                swatch = pygame.Rect(
                    x, y, self.options.swatch_size, self.options.swatch_size
                )
                pygame.draw.rect(self.options.surface, entry.color, swatch)
                pygame.draw.rect(
                    self.options.surface, self.options.border_color, swatch, 1
                )

                text = self.font.render(entry.label, True, self.options.text_color)
                self.options.surface.blit(
                    text,
                    (
                        swatch.right + self.options.swatch_spacing,
                        swatch.centery - text.get_height() // 2,
                    ),
                )

                y += line_height

            y += self.options.group_spacing
