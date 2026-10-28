import pygame


class GridRenderer:
    def __init__(self, grid):
        self.grid = grid

    def render(self):
        for row in self.grid:
