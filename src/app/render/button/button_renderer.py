from typing import override

import pygame

from app.model import Button
from app.render import Renderer

from .button_render_options import ButtonRenderOptions


class ButtonRenderer(Renderer[list[Button]]):
    def __init__(self, options: ButtonRenderOptions) -> None:
        super().__init__(options)

        self.options = options

        self.font = pygame.font.SysFont(options.font_name, options.font_size)

    @override
    def render(self, object: list[Button]) -> None:
        buttons: list[Button] = object

        for button in buttons:
            pygame.draw.rect(
                self.options.surface,
                self.options.color,
                button.rect,
                border_radius=self.options.border_radius,
            )
            pygame.draw.rect(
                self.options.surface,
                self.options.border_color,
                button.rect,
                self.options.border_width,
                border_radius=self.options.border_radius,
            )

            text = self.font.render(button.label, True, self.options.text_color)
            self.options.surface.blit(text, text.get_rect(center=button.rect.center))
