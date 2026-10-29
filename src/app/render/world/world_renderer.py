from app.render import Renderer
from app.render.grid import GridRenderer
from world.world import World
from app.model import Grid

from .world_render_options import WorldRenderOptions


class WorldRenderer(Renderer[World]):
    def __init__(
        self, options: WorldRenderOptions, grid_renderer: GridRenderer
    ) -> None:
        super().__init__(options)

        self.grid_renderer = grid_renderer

    def render(self, object: World) -> None:
        world: World = object
        grid: Grid = Grid(columns=world.parameters.columns, rows=world.parameters.rows)
        self.grid_renderer.render(grid)
