import os
import pygame

from game_engine.entities import *


class Turret(Base_object):
    pass

class TankBase(Base_animated_object):
    pass

class Unit:
    def __init__(self, coord):
        self.coord = coord

    def draw_game_area(self, surface, offset_x: int, offset_y: int):
        """Draw unit on screen."""

        pygame.draw.circle(surface, LIME, world2screen(self.coord, offset_x, offset_y), 20, 3)