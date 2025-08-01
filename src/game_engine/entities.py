import os
import pygame

from game_engine.definitions import *
from game_engine.functions_math import *


# ======================================================================


class Base_object:
    path = ["path_to_sprite", "example.png"]

    def __init__(self, coord: tuple[float, float], angle: float):
        """Initialization of the object.
        
        Args:
            coord (tuple[float, float]): Position as a tuple containing x and y coordinates.
            angle (float): Rotation angle in radians.
        """
        # basic variables
        self.coord = coord
        self.angle = angle

        # load and prepare sprite
        self.sprite = pygame.image.load(os.path.join(*self.path))
        self.sprite.convert()
        self.sprite.set_colorkey(BLACK)

        # calculate frame size
        sprite_rect = self.sprite.get_rect()
        self.frame_width = sprite_rect.width
        self.frame_height = sprite_rect.height

    def draw(self, win, offset_x: float, offset_y: float, scale: float = 1):
        """Draw the object on the screen."""
        scaled_image = pygame.transform.scale(self.sprite, (scale * self.frame_width, scale * self.frame_height))
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center = world2screen(self.coord, offset_x, offset_y, scale))
        win.blit(rotated_image, new_rect.topleft)

    def get_position(self) -> tuple[float, float]:
        """Return object's coordinates."""
        return self.coord

    def get_angle(self) -> float:
        """Return object's angle (in radians)."""
        return self.angle

    def set_position(self, coord: tuple[float, float]):
        """Set new position."""
        self.coord = coord

    def set_angle(self, angle: float):
        """Sets a new rotation angle for the object.

        Args:
            angle (float): The new angle in radians.
        """
        self.angle = angle


# ======================================================================


class Base_animated_object(Base_object):
    path = ["path_to_sprite_sheet", "example.png"]
    number_of_frames = 4
    number_of_states = 3

    def __init__(self, coord: tuple[float, float], angle: float):
        """Initialization of the object.
        
        Args:
            coord (tuple[float, float]): Position as a tuple containing x and y coordinates.
            angle (float): Rotation angle in radians.
        """
        # basic variables
        self.coord = coord
        self.angle = angle
        self.state = "stop"

        # load and prepare sprite sheet
        self.sprite_sheet = pygame.image.load(os.path.join(*self.path))
        self.sprite_sheet.convert()
        self.sprite_sheet.set_colorkey(BLACK)

        # calculate frame size
        sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.frame_width = sprite_sheet_rect.width // self.number_of_frames
        self.frame_height = sprite_sheet_rect.height // self.number_of_states

        # crop sprite sheet into frames - store frames in sprite list
        self.sprite_list = []
        for y in range(self.number_of_states):
            for x in range(self.number_of_frames):
                self.sprite_list.append(self.crop_sprite(self.sprite_sheet, x, y))

        # prepare clock
        self.last_time = 0
        self.frame = 0
        self.frame_interval = 1000 // self.number_of_frames

        # set first frame
        self.frame_sprite = self.sprite_list[0]   

    def draw(self, win, offset_x: float, offset_y: float, scale: float = 1):
        """Main method for preparing and drawing the object on the screen."""
        # count frames and load new sprite when the change will occur
        if self.frame_clock():
            self.frame_sprite = self.sprite_list[self.get_frame_index()] 
        # draw
        self.draw_sprite(win, offset_x, offset_y, scale)

    def draw_sprite(self, win, offset_x: float, offset_y: float, scale: float = 1):
        """Draw currently loaded sprite of the object on the screen."""
        scaled_image = pygame.transform.scale(self.frame_sprite, (scale * self.frame_width, scale * self.frame_height))
        rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center = world2screen(self.coord, offset_x, offset_y, scale))
        win.blit(rotated_image, new_rect.topleft)

    def frame_clock(self):
        """Updates the animation frame based on the passage of time.

        Returns:
            bool: True when the change will occur.
        """
        current_time = pygame.time.get_ticks()
        if current_time > self.last_time + self.frame_interval:
            self.last_time = current_time
            self.frame += 1
            if self.frame == self.number_of_frames: 
                self.frame = 0
            return True
        return False

    def crop_sprite(self, sprite_sheet, no_of_frame: int, no_of_state: int):
        """Function that crops and return one frame from sprite sheet."""
        image = pygame.Surface((self.frame_width, self.frame_height))
        image.blit(sprite_sheet, (0, 0), (no_of_frame * self.frame_width, no_of_state * self.frame_height, self.frame_width, self.frame_height))
        image.convert()
        image.set_colorkey(BLACK)
        return image

    def get_frame_index(self):
        """Count frame index to get sprite from sprite list."""
        if self.state == "stop":
            offset = 0
        elif self.state == "move":
            offset = 1
        elif self.state == "dead":
            offset = 2
        else:
            offset = 2       
        return self.number_of_frames * offset + self.frame


# ======================================================================

