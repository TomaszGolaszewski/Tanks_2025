import pygame

from settings import *
from game_engine.scenes import *
from game_engine.scenes_features import *
# from classes_map import *
# from classes_trains import *


# ======================================================================


class GameSceneOLD(SceneBase):
    def __init__(self):
        """Initialization of the scene."""
        SceneBase.__init__(self)

        # display variables
        self.scale = 0.5
        self.offset_horizontal, self.offset_vertical = 500, 500
        # self.show_extra_data = False
        # self.show_movement_target = False
        # self.pause = False
        self.current_frame = 0
        
        # mouse related variables
        self.left_mouse_button_down = False
        self.right_mouse_button_down = False
        self.last_used_tile = 0

        # initialize the map
        self.map = Map()
        self.current_selected_train_id = 0
        self.lowest_free_train_id = 1

        # create initial test trains
        self.dict_with_trains = {}

        # TODO: check and remove
        self.list_with_windows = []
    

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """

        # calculate values ​​for mouse and tile position
        mouse_pos = pygame.mouse.get_pos()
        coord_world = screen2world(mouse_pos, self.offset_horizontal, self.offset_vertical, self.scale)
        coord_id = self.map.world2id(coord_world)
        current_tile_id = self.map.get_tile_by_coord_id(coord_id)

        for event in events:

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click
                if event.button == 1:
                    button_was_pressed = False
                    # choose mode
                    if any([mode_button.is_inside(mouse_pos) for mode_button in self.list_with_mode_buttons]):
                        button_was_pressed = True
                        for mode_button in self.list_with_mode_buttons:
                            if mode_button.check_pressing(mouse_pos):
                                self.current_mode = mode_button.option
                    # choose terrain
                    if self.current_mode == "terrain" and \
                            any([terrain_button.is_inside(mouse_pos) for terrain_button in self.list_with_terrain_buttons]):
                        button_was_pressed += True
                        for terrain_button in self.list_with_terrain_buttons:
                            if terrain_button.check_pressing(mouse_pos):
                                self.current_terrain = terrain_button.option
                    
                    if not button_was_pressed:
                        self.left_mouse_button_down = True
                        self.right_mouse_button_down = False

                # 3 - right click
                if event.button == 3:
                    # semaphores
                    if self.current_mode == "semaphores" and current_tile_id:
                        self.map.remove_semaphore(current_tile_id)
                        self.map.calculate_trains_path(self.dict_with_trains)
                    # remove targets
                    if self.current_mode == "targets":
                        if self.current_selected_train_id in self.dict_with_trains and \
                                current_tile_id in self.dict_with_trains[self.current_selected_train_id].movement_target:
                            self.dict_with_trains[self.current_selected_train_id].movement_target.remove(current_tile_id)
                            # calculate trains paths
                            self.map.calculate_trains_path(self.dict_with_trains)
                    else:
                        self.right_mouse_button_down = True
                        self.left_mouse_button_down = False

            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                # 1 - left click
                if event.button == 1:
                    self.left_mouse_button_down = False
                    self.last_used_tile = 0
                    self.current_used_tile = 0

                # 2 - middle click
                if event.button == 2:
                    # define new view center
                    self.offset_horizontal -= (mouse_pos[0] - WIN_WIDTH/2) / self.scale
                    self.offset_vertical -= (mouse_pos[1] - WIN_HEIGHT/2) / self.scale

                # 3 - right click
                if event.button == 3:
                    self.right_mouse_button_down = False
                    self.last_used_tile = 0
                    self.current_used_tile = 0

                # 4 - scroll up
                if event.button == 4:
                    old_scale = self.scale

                    self.scale *= 2
                    if self.scale >= 4: self.scale = 4

                    if old_scale - self.scale:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        self.offset_horizontal -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / self.scale
                        self.offset_vertical -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / self.scale

                # 5 - scroll down
                if event.button == 5:
                    old_scale = self.scale

                    self.scale /= 2
                    # if SCALE <= 0.25: SCALE = 0.25
                    if self.scale <= 0.125: self.scale = 0.125

                    if old_scale - self.scale:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        self.offset_horizontal -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / self.scale
                        self.offset_vertical -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / self.scale


            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # pause
                if event.key == pygame.K_SPACE:
                    if self.pause: self.pause = False
                    else: self.pause = True
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


    # handle the remaining logic related to mouse operation
        
        # adding entities
        if self.left_mouse_button_down and (not current_tile_id or self.last_used_tile != current_tile_id):
            # add new tile
            if self.current_mode == "terrain" or (self.current_mode =="tracks" and not current_tile_id):
                current_tile_id = self.map.add_tile(coord_id, self.current_terrain)

            self.last_used_tile = current_tile_id
        # removing entities
        if self.right_mouse_button_down:
            # remove tile
            if self.current_mode == "terrain" and current_tile_id:
                # remove tile from train variables
                self.map.remove_tile(current_tile_id)
                self.map.calculate_trains_path(self.dict_with_trains)
        
    def update(self):
        """Game logic for the scene."""

        # count tics
        self.current_frame += 1
        if self.current_frame == FRAMERATE: # // 10:
            self.current_frame = 0

        # check hovering of the mouse
        mouse_coord = pygame.mouse.get_pos()
        for mode_button in self.list_with_mode_buttons:
            mode_button.check_hovering(mouse_coord)
        if self.current_mode == "terrain":
            for terrain_button in self.list_with_terrain_buttons:
                terrain_button.check_hovering(mouse_coord)

        # run the simulation
        if not self.current_frame:
            
            # calculate trains free paths
            self.map.calculate_trains_path(self.dict_with_trains)

        # run trains
        for train_id in self.dict_with_trains:
            self.dict_with_trains[train_id].run(self.map, self.dict_with_trains)


    def render(self, win):
        """Draw scene on the screen."""

        # clear screen
        win.fill(BLACK)

        # draw the map
        self.map.draw(win, self.offset_horizontal, self.offset_vertical, self.scale)


    # # draw UI

    #     # draw pause
    #     if self.pause:
    #         self.pause_text.draw(win)


# ======================================================================

