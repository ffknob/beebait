from app.render import Renderer
from app.render.world import WorldRenderOptions
from world.world import World


class WorldRenderer[World](Renderer):
    def __init__(self, options: WorldRenderOptions):
        super().__init__(options)

        self.world = world

    def render(self, object: World) -> None:
        grid_render_options: GridRenderOptions = GridRenderOptions()

        GridRenderer(grid_render_options).render()
