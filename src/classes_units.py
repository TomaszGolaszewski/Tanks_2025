import os
import pygame

from game_engine.entities import *


class Turret(Base_object):
    path = ["imgs", "units", "turret.bmp"]

    def __init__(self, coord: tuple[float, float], angle: float, team_color: tuple[int, int, int]):
        Base_object.__init__(self, coord, angle)
        self.team_color = team_color
        self.sprite = self.swap_color(self.sprite, LIME, team_color)

class TankBase(Base_animated_object):
    path = ["imgs", "units", "tank_body_8.bmp"]
    number_of_frames = 8
    number_of_states = 2

    def __init__(self, coord: tuple[float, float], angle: float, team_color: tuple[int, int, int]):
        Base_animated_object.__init__(self, coord, angle)
        self.team_color = team_color
        new_sprite_list = [self.swap_color(sprite, LIME, team_color) for sprite in self.sprite_list]
        self.sprite_list = new_sprite_list

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
        self.team_color = self.decide_team_color(team)

        # unit objects
        self.body = TankBase(coord, angle, self.team_color)
        self.turret = Turret(coord, angle, self.team_color)

    def draw(self, surface, offset_x: int, offset_y: int):
        """Draw unit on screen."""
        self.body.draw(surface, offset_x, offset_y)
        self.turret.draw(surface, offset_x, offset_y)
        pygame.draw.circle(surface, WHITE, world2screen(self.coord, offset_x, offset_y), 2)

    def run(self):
        """Run the basic functioning of the unit."""
        self.body.set_position(self.coord)
        self.turret.set_position(self.coord)

    def manually_move_body(self, direction_x: int, direction_y: int):
        """Move unit body manually, e.g. by keyboard.
        The direction of movement corresponds to the axes of the in-game coordinate system:
        * direction_x == 1 -> move right
        * direction_x == -1 -> move left
        * direction_y == 1 -> move down
        * direction_y == -1 -> move up
        """
        move_speed = 5 
        self.coord = (self.coord[0] + move_speed * direction_x, self.coord[1] + move_speed * direction_y)

        # TODO: move to different method
        if direction_x or direction_y:
            self.body.state = "move"
        else:
            self.body.state = "stop"

    def manually_move_turret(self, direction: int):
        """Move unit turret manually, e.g. by keyboard.
        The direction of rotation is clockwise:
        * direction == 1 -> move right
        * direction == -1 -> move left
        """
        move_speed = 0.03
        turret_angle = self.turret.get_angle()
        turret_angle += move_speed * direction
        if turret_angle > 2*math.pi:
            turret_angle -= 2*math.pi
        if turret_angle < 0:
            turret_angle += 2*math.pi
        self.turret.set_angle(turret_angle)

    def get_position(self) -> tuple[float, float]:
        """Return object's coordinates."""
        return self.coord
    
    def decide_team_color(self, team) -> tuple[int, int, int]:
        """Return team color base on team number."""
        if team == 1:
            return RED
        elif team == 2:
            return (0, 0, 250) # BLUE
        else:
            return WHITE