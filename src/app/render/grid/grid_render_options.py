from dataclasses import dataclass

from app.render import RenderOptions


@dataclass(frozen=True)
class GridRenderOptions(RenderOptions):
    line_color: str = "black"
    line_width: int = 1
    horizontal_margin_percentage: float = 0.1
    vertical_margin_percentage: float = 0.1
