import pygame

from settings import *
from game_engine.scenes import *
from game_engine.scenes_features import *
from classes_map import *
from classes_units import *


class GameScene(SceneBase):
    def __init__(self, kw={}):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        self.map = Map(os.path.join("maps", self.kw.get("map_file")))
        # display variables
        self.player_x_pos, self.player_y_pos = 100, 100

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """                
        # keys that can be pressed multiple times
        # move
        move_speed = 5 
        # move left
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.player_x_pos -= move_speed
        # move right
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.player_x_pos += move_speed
        # move up
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.player_y_pos -= move_speed
        # move down
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.player_y_pos += move_speed

    def update(self):
        """Game logic for the scene."""
        pass
    
    def render(self, win):
        """Draw scene on the screen."""
        # clear screen
        win.fill(BLACK)
        # draw the map
        self.draw_game_area(win, WIN_WIDTH//2 - self.player_x_pos, WIN_HEIGHT//2 - self.player_y_pos, \
                            screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT)
        self.map.draw_preview_by_topright(win, (WIN_WIDTH, 0))
        
    def draw_game_area(self, win, offset_x: int, offset_y: int, screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT):
        """Draw game area on the screen.
        The Map, units and players.
        """
        # create buffer surface
        buffer_surface = pygame.Surface((screen_width, screen_height))

        # draw map
        self.map.draw_cropped_map(buffer_surface, offset_x, offset_y, \
                            screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT)
        # draw units
        pygame.draw.circle(buffer_surface, RED, world2screen((self.player_x_pos, self.player_y_pos), offset_x, offset_y), 10)

        # draw buffer on screen
        win.blit(buffer_surface, (screen_pos_x, screen_pos_y))

# ======================================================================


class Game2PlayersScene(GameScene):
    def __init__(self, kw={}):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        self.map = Map(os.path.join("maps", self.kw.get("map_file")))
        # display variables
        self.player_1_x_pos, self.player_1_y_pos = 100, 100
        self.player_2_x_pos, self.player_2_y_pos = 300, 100

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """
        # keys that can be pressed multiple times
        # move
        move_speed = 5 

        # Player 1
        # move left
        if keys_pressed[pygame.K_a]:
            self.player_1_x_pos -= move_speed
        # move right
        if keys_pressed[pygame.K_d]:
            self.player_1_x_pos += move_speed
        # move up
        if keys_pressed[pygame.K_w]:
            self.player_1_y_pos -= move_speed
        # move down
        if keys_pressed[pygame.K_s]:
            self.player_1_y_pos += move_speed

        # Player 2
        # move left
        if keys_pressed[pygame.K_LEFT]:
            self.player_2_x_pos -= move_speed
        # move right
        if keys_pressed[pygame.K_RIGHT]:
            self.player_2_x_pos += move_speed
        # move up
        if keys_pressed[pygame.K_UP]:
            self.player_2_y_pos -= move_speed
        # move down
        if keys_pressed[pygame.K_DOWN]:
            self.player_2_y_pos += move_speed

    def update(self):
        """Game logic for the scene."""
        pass
    
    def render(self, win):
        """Draw scene on the screen."""
        # clear screen
        win.fill(BLACK)
        # draw the map
        margin_between_players = 30
        self.draw_game_area(win, WIN_WIDTH//4 - self.player_1_x_pos, WIN_HEIGHT//2 - self.player_1_y_pos, \
                            screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH//2 - margin_between_players//2, screen_height=WIN_HEIGHT)
        self.draw_game_area(win, WIN_WIDTH//4 - self.player_2_x_pos, WIN_HEIGHT//2 - self.player_2_y_pos, \
                            screen_pos_x=WIN_WIDTH//2 + margin_between_players//2, screen_pos_y=0, \
                            screen_width=WIN_WIDTH//2 - margin_between_players//2, screen_height=WIN_HEIGHT)
        self.map.draw_preview_by_midtop(win, (WIN_WIDTH//2, 0))
    
    # TODO: to remove
    def draw_game_area(self, win, offset_x: int, offset_y: int, screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT):
        """Draw game area on the screen.
        The Map, units and players.
        """
        buffer_surface = pygame.Surface((screen_width, screen_height))

        # draw map
        self.map.draw_cropped_map(buffer_surface, offset_x, offset_y, \
                            screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT)
        # draw units
        pygame.draw.circle(buffer_surface, RED, world2screen((self.player_1_x_pos, self.player_1_y_pos), offset_x, offset_y), 10)
        pygame.draw.circle(buffer_surface, BLUE, world2screen((self.player_2_x_pos, self.player_2_y_pos), offset_x, offset_y), 10)

        # draw buffer on screen
        win.blit(buffer_surface, (screen_pos_x, screen_pos_y))

# ======================================================================
