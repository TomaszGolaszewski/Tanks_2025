import os
import pygame

from game_engine.entities import *


class Turret(Base_object):
    pass

class TankBase(Base_animated_object):
    pass

class Unit:
    def __init__(self, coord: tuple[float, float], angle: float, team: int):
        """Initialization of the unit.
        
        Args:
            coord (tuple[float, float]): Position as a tuple containing x and y coordinates.
            angle (float): Rotation angle in radians.
            team (int): ID of unit team - 0 for no team.
        """
        # basic variables
        self.coord = coord
        self.angle = angle
        self.team = team

    def draw(self, surface, offset_x: int, offset_y: int):
        """Draw unit on screen."""
        if self.team == 1:
            color = RED
        elif self.team == 2:
            color = BLUE
        else:
            color = WHITE
        pygame.draw.circle(surface, color, world2screen(self.coord, offset_x, offset_y), 10)

    def move_manually(self, direction_x: int, direction_y: int):
        """Move unit manually, e.g. by keyboard.
        The direction of movement corresponds to the axes of the in-game coordinate system:
        * direction_x == 1 -> move right
        * direction_x == -1 -> move left
        * direction_y == 1 -> move down
        * direction_y == -1 -> move up
        """
        move_speed = 5 
        self.coord = (self.coord[0] + move_speed * direction_x, self.coord[1] + move_speed * direction_y)

    def get_position(self) -> tuple[float, float]:
        """Return object's coordinates."""
        return self.coord