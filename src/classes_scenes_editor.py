import pygame

from settings import *
from game_engine.scenes import *
from game_engine.scenes_features import *
from classes_map import *
# from classes_trains import *


class EditorScene(SceneBase):
    def __init__(self, kw={}):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        self.map = Map(os.path.join("maps", self.kw.get("map_file")))
        # display variables
        self.margin_top = 50
        self.scale = 0.5
        self.offset_horizontal, self.offset_vertical = 0, 0

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """
        for event in events:

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click
                if event.button == 1:
                    # TODO: for test, to remove
                    mouse_pos = pygame.mouse.get_pos()
                    world_test = screen2world((mouse_pos[0], mouse_pos[1]-self.margin_top), self.offset_horizontal, self.offset_vertical, self.scale)
                    print(self.scale, world_test[0] // TILE_EDGE_LENGTH, world_test[1] // TILE_EDGE_LENGTH)

                # 3 - right click
                if event.button == 3:
                    pass

            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                # 1 - left click
                if event.button == 1:
                    pass

                # 2 - middle click
                if event.button == 2:
                    # define new view center
                    mouse_pos = pygame.mouse.get_pos()
                    self.offset_horizontal -= (mouse_pos[0] - WIN_WIDTH/2) / self.scale
                    self.offset_vertical -= (mouse_pos[1]-self.margin_top - WIN_HEIGHT/2) / self.scale

                # 3 - right click
                if event.button == 3:
                    pass

                # 4 - scroll up
                if event.button == 4:
                    old_scale = self.scale
                    # mouse_pos = pygame.mouse.get_pos()

                    self.scale *= 2
                    if self.scale >= 1: self.scale = 1

                    if old_scale - self.scale:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        self.offset_horizontal -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / self.scale
                        self.offset_vertical -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / self.scale

                # 5 - scroll down
                if event.button == 5:
                    old_scale = self.scale
                    # mouse_pos = pygame.mouse.get_pos()

                    self.scale /= 2
                    if self.scale <= 0.125: self.scale = 0.125

                    if old_scale - self.scale:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        self.offset_horizontal -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / self.scale
                        self.offset_vertical -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / self.scale


            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # center
                if event.key == pygame.K_c:
                    self.scale = 1
                    self.offset_horizontal, self.offset_vertical = 0, 0
                
    # keys that can be pressed multiple times
        # move
        move_speed = 5 / self.scale
        # move left
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.offset_horizontal += move_speed
        # move right
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.offset_horizontal -= move_speed
        # move up
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.offset_vertical += move_speed
        # move down
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.offset_vertical -= move_speed

    def update(self):
        """Game logic for the scene."""
        pass
    
    def render(self, win):
        """Draw scene on the screen."""
        # clear screen
        win.fill(BLACK)
        # draw the map
        self.map.draw(win, self.offset_horizontal, self.offset_vertical, self.scale, \
                            screen_pos_x=0, screen_pos_y=self.margin_top, screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT)


# ======================================================================

