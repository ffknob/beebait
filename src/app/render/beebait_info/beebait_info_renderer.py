from typing import override

import pygame

from app.render import Renderer
from beebait.beebait import Beebait
from world.enums import FeatureName

from .beebait_info_render_options import BeebaitInfoRenderOptions


class BeebaitInfoRenderer(Renderer[list[Beebait]]):
    def __init__(self, options: BeebaitInfoRenderOptions) -> None:
        super().__init__(options)

        self.options = options

        self.font = pygame.font.SysFont(options.font_name, options.font_size)
        self.bold_font = pygame.font.SysFont(
            options.font_name, options.font_size, bold=True
        )

    def _format_temperature(self, beebait: Beebait, feature_name: FeatureName) -> str:
        feature_value = beebait.features_values.get(feature_name)

        return f"{feature_value.value:.0f}º" if feature_value else "--º"

    def _format_beebait(self, beebait: Beebait) -> str:
        external_temperature = self._format_temperature(
            beebait, FeatureName.TEMPERATURE
        )
        internal_temperature = self._format_temperature(
            beebait, FeatureName.INTERNAL_TEMPERATURE
        )
        status = "occupied" if beebait.occupied else "empty"

        return f"Beebait #{beebait.id}: {external_temperature} / {internal_temperature}; {status}"

    @override
    def render(self, object: list[Beebait]) -> None:
        beebaits: list[Beebait] = object

        surface = self.options.surface
        horizontal_margin = (
            surface.get_width() * self.options.horizontal_margin_percentage
        )
        line_height = self.font.get_linesize() + self.options.line_spacing
        lines_per_column = max(1, surface.get_height() // line_height)

        for i, beebait in enumerate(beebaits):
            font = self.bold_font if beebait.occupied else self.font
            color = (
                self.options.occupied_text_color
                if beebait.occupied
                else self.options.text_color
            )

            text = font.render(self._format_beebait(beebait), True, color)

            column, line = divmod(i, lines_per_column)
            surface.blit(
                text,
                (
                    horizontal_margin + column * self.options.column_width,
                    line * line_height,
                ),
            )
