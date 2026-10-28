from dataclasses import dataclass

from app.render import RenderOptions


@dataclass(frozen=True)
class WorldRenderOptions(RenderOptions):
    pass
