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
        self.unit_dict = {
            1: Unit((100, 100), 0, 1)
        }
        self.player_id = 1

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """                
        # keys that can be pressed multiple times
        # move
        player_move_x = 0
        player_move_y = 0
        player_move_turret = 0
        # move left
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            player_move_x -= 1
        # move right
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            player_move_x += 1
        # move up
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            player_move_y -= 1
        # move down
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            player_move_y += 1
        # move turret left
        if keys_pressed[pygame.K_f] or keys_pressed[pygame.K_COMMA]:
            player_move_turret -= 1
        # move turret right
        if keys_pressed[pygame.K_h] or keys_pressed[pygame.K_PERIOD]:
            player_move_turret += 1
        # move player
        self.unit_dict[self.player_id].manually_move_body(player_move_x, player_move_y)
        self.unit_dict[self.player_id].manually_move_turret(player_move_turret)

    def update(self):
        """Game logic for the scene."""
        for unit_id in self.unit_dict:
            self.unit_dict[unit_id].run()
    
    def render(self, win):
        """Draw scene on the screen."""
        # clear screen
        win.fill(BLACK)
        # draw the map
        player_pos = self.unit_dict[self.player_id].get_position()
        self.draw_game_area(win, WIN_WIDTH//2 - player_pos[0], WIN_HEIGHT//2 - player_pos[1], \
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
        for unit_id in self.unit_dict:
            self.unit_dict[unit_id].draw(buffer_surface, offset_x, offset_y)
        # pygame.draw.circle(buffer_surface, RED, world2screen((self.player_x_pos, self.player_y_pos), offset_x, offset_y), 10)

        # draw buffer on screen
        win.blit(buffer_surface, (screen_pos_x, screen_pos_y))

# ======================================================================


class Game2PlayersScene(GameScene):
    def __init__(self, kw={}):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        self.map = Map(os.path.join("maps", self.kw.get("map_file")))
        self.unit_dict = {
            1: Unit((100, 100), 0, 1),
            2: Unit((300, 100), 0, 2)
        }
        self.player_1_id = 1
        self.player_2_id = 2

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """
        # keys that can be pressed multiple times
        # move

        # Player 1
        player_1_move_x = 0
        player_1_move_y = 0
        player_1_move_turret = 0
        # move left
        if keys_pressed[pygame.K_a]:
            player_1_move_x -= 1
        # move right
        if keys_pressed[pygame.K_d]:
            player_1_move_x += 1
        # move up
        if keys_pressed[pygame.K_w]:
            player_1_move_y -= 1
        # move down
        if keys_pressed[pygame.K_s]:
            player_1_move_y += 1
        # move turret left
        if keys_pressed[pygame.K_f]:
            player_1_move_turret -= 1
        # move turret right
        if keys_pressed[pygame.K_h]:
            player_1_move_turret += 1
        # move player 1
        self.unit_dict[self.player_1_id].manually_move_body(player_1_move_x, player_1_move_y)
        self.unit_dict[self.player_1_id].manually_move_turret(player_1_move_turret)

        # Player 2
        player_2_move_x = 0
        player_2_move_y = 0
        player_2_move_turret = 0
        # move left
        if keys_pressed[pygame.K_LEFT]:
            player_2_move_x -= 1
        # move right
        if keys_pressed[pygame.K_RIGHT]:
            player_2_move_x += 1
        # move up
        if keys_pressed[pygame.K_UP]:
            player_2_move_y -= 1
        # move down
        if keys_pressed[pygame.K_DOWN]:
            player_2_move_y += 1
        # move turret left
        if keys_pressed[pygame.K_COMMA]:
            player_2_move_turret -= 1
        # move turret right
        if keys_pressed[pygame.K_PERIOD]:
            player_2_move_turret += 1
        # move player 2
        self.unit_dict[self.player_2_id].manually_move_body(player_2_move_x, player_2_move_y)
        self.unit_dict[self.player_2_id].manually_move_turret(player_2_move_turret)

    # def update(self):
    #     """Game logic for the scene."""
    #     pass
    
    def render(self, win):
        """Draw scene on the screen."""
        # clear screen
        win.fill(BLACK)
        # draw the map
        margin_between_players = 30
        player_1_pos = self.unit_dict[self.player_1_id].get_position()
        player_2_pos = self.unit_dict[self.player_2_id].get_position()
        self.draw_game_area(win, WIN_WIDTH//4 - player_1_pos[0], WIN_HEIGHT//2 - player_1_pos[1], \
                            screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH//2 - margin_between_players//2, screen_height=WIN_HEIGHT)
        self.draw_game_area(win, WIN_WIDTH//4 - player_2_pos[0], WIN_HEIGHT//2 - player_2_pos[1], \
                            screen_pos_x=WIN_WIDTH//2 + margin_between_players//2, screen_pos_y=0, \
                            screen_width=WIN_WIDTH//2 - margin_between_players//2, screen_height=WIN_HEIGHT)
        self.map.draw_preview_by_midtop(win, (WIN_WIDTH//2, 0))
    

# ======================================================================
