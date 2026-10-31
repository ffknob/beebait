import pygame

from app.model.cell import Cell
from app.render import Renderer
from world.feature import FeatureValue

from .cell_render_options import CellRenderOptions


class CellRenderer(Renderer[Cell]):
    def __init__(self, options: CellRenderOptions) -> None:
        self.options = options

    def _get_temperature_color(self, cell: Cell) -> pygame.Color:
        temperature: FeatureValue | None = cell.features.get("temperature", None)
        temperature_measurement = temperature.value if temperature else None

        temperature_color_index = (
            (
                int(
                    (temperature_measurement - self.options.min_temperature)
                    // self.options.temperature_step
                )
            )
            if temperature_measurement is not None
            else None
        )
        temperature_color = (
            self.options.temperature_palette[
                max(
                    0,
                    min(
                        temperature_color_index,
                        len(self.options.temperature_palette) - 1,
                    ),
                )
            ]
            if temperature_color_index is not None
            else self.options.no_measurement_color
        )

        return temperature_color

    def render(self, object: Cell) -> None:
        cell: Cell = object

        temperature_color: pygame.Color = self._get_temperature_color(cell)

        pygame.draw.rect(self.options.surface, temperature_color, cell.dimensions)
