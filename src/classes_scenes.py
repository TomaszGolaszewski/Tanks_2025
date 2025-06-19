import os
import pygame

from settings import *
from game_engine.scenes import *
from game_engine.scenes_features import *
from classes_map import *
# from classes_trains import *
from classes_scenes_game import *


class TitleScene(SceneBase):
    def __init__(self, kw={}):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        offset = 30
        self.title = FixText((WIN_WIDTH/2, WIN_HEIGHT/2 - 30 - offset), "TANKS 2025", 70)
        self.subtitle = FixText((WIN_WIDTH/2, WIN_HEIGHT/2 + 20 - offset), "New beginning", 40)
        self.list_with_mode_buttons = [
            AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 100 - offset), "[Quick Start]", 30, color=GRAY, option="quick"),
            AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 150 - offset), "[Classic One-person]", 30, color=GRAY, option="one"),
            AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 200 - offset), "[Classic Cooperation]", 30, color=GRAY, option="coop"),
            AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 250 - offset), "[Zombie Mode]", 30, color=GRAY, option="zombie"),
            AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 300 - offset), "[RTS Mode]", 30, color=GRAY, option="rts"),
            AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 350 - offset), "[Settings]", 30, color=GRAY, option="settings"),
            AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT/2 + 400 - offset), "[Exit]", 30, color=GRAY, option="exit"),
        ]
        self.seconds_since_start = 0
        self.current_frame = 0
        self.buttons_delay = 0 #1
    
    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """
        for event in events:
            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # move to the next scene
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.switch_scene(LoadingScene())
                # quick start
                if event.key == pygame.K_q:
                    self.switch_scene(LoadingScene())

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN \
                        and self.seconds_since_start > self.buttons_delay \
                        and event.button in [1,2,3]: # 1 - left; 2 - middle; 3 - right click
                mouse_coord = pygame.mouse.get_pos()
                # check buttons
                for button in self.list_with_mode_buttons:
                    if button.is_inside(mouse_coord):
                        if button.option == "exit":
                            self.terminate()
                        else:
                            self.kw.update({"game_mode": button.option})
                            self.switch_scene(BrowseMapsScene(self.kw))
                  
    def update(self):
        """Game logic for the scene."""

        # check hovering of the mouse
        mouse_coord = pygame.mouse.get_pos()
        for button in self.list_with_mode_buttons:
            button.check_hovering(mouse_coord)

        # clock
        self.current_frame += 1
        if self.current_frame == FRAMERATE:
            self.current_frame = 0
            self.seconds_since_start += 1

    def render(self, win):
        """Draw scene on the screen."""

        # clear screen
        win.fill(BLACK)

        # print titles and buttons
        self.title.draw(win)
        self.subtitle.draw(win)
        if self.seconds_since_start > self.buttons_delay:
            for button in self.list_with_mode_buttons:
                button.draw(win)


# ======================================================================


# class LoadingScene(SceneBase):
#     def __init__(self, kw):
#         """Initialization of the scene."""
#         SceneBase.__init__(self, kw)
#         self.loading_text = FixText((WIN_WIDTH/2, WIN_HEIGHT/2), "Loading ...", 30)
#         self.ticks = 0

#     # def process_input(self, events, keys_pressed):
#     #     """
#     #     Receive all the events that happened since the last frame.
#     #     Handle all received events.
#     #     """
#     #     pass

#     def update(self):
#         """Game logic for the scene."""
#         self.ticks += 1
#         # automatically jump to the GameScene after the first cycle
#         if self.ticks > 1:
#             self.switch_scene(GameScene(self.kw))
    
#     def render(self, win):
#         """Draw scene on the screen."""
#         # clear screen
#         win.fill(BLACK)
#         # print loading text
#         self.loading_text.draw(win)


# ======================================================================


class BrowseMapsScene(SceneBase):
    def __init__(self, kw={}):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        self.title = FixText((WIN_WIDTH/2, 60), "Choose map", 50)
        self.start_button = AdvancedButton((WIN_WIDTH/2, WIN_HEIGHT - 75), "[ Next >> ]", 30, color=LIME, color_hover=LIME)
        self.prev_map = AdvancedButton((250, WIN_HEIGHT - 75), "[ < Prev Map ]", 30, color=GRAY)
        self.next_map = AdvancedButton((WIN_WIDTH - 250, WIN_HEIGHT - 75), "[ Next Map > ]", 30, color=GRAY)

        try:
            self.list_with_files = os.listdir("maps")
        except FileNotFoundError:
            self.list_with_files = []
        self.current_map_file = self.list_with_files[0]
        self.current_map_no = 0
        self.kw.update({"map_file": self.current_map_file})
        self.map = Map(os.path.join("maps", self.current_map_file), preview_only=True)

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """
        for event in events:
            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # move to the next scene
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.switch_scene(LoadingScene(self.kw))

                # TODO: add keyboard operation

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in [1,2,3]: # 1 - left; 2 - middle; 3 - right click
                mouse_coord = pygame.mouse.get_pos()
                # move to the next scene
                if self.start_button.is_inside(mouse_coord):
                    self.switch_scene(LoadingScene(self.kw))
                # choose map
                if self.prev_map.is_inside(mouse_coord) or self.next_map.is_inside(mouse_coord):
                    if self.prev_map.is_inside(mouse_coord):
                        self.current_map_no -= 1
                        if self.current_map_no < 0:
                            self.current_map_no = len(self.list_with_files)-1
                    elif self.next_map.is_inside(mouse_coord):
                        self.current_map_no += 1
                        if self.current_map_no >= len(self.list_with_files):
                            self.current_map_no = 0
                    self.current_map_file = self.list_with_files[self.current_map_no]
                    self.kw.update({"map_file": self.current_map_file})
                    self.map = Map(os.path.join("maps", self.current_map_file), preview_only=True)

    def update(self):
        """Game logic for the scene."""
        # check hovering of the mouse
        mouse_coord = pygame.mouse.get_pos()
        self.start_button.check_hovering(mouse_coord)
        self.prev_map.check_hovering(mouse_coord)
        self.next_map.check_hovering(mouse_coord)
    
    def render(self, win):
        """Draw scene on the screen."""
        # clear screen
        win.fill(BLACK)
        # print titles and buttons
        self.title.draw(win)
        self.start_button.draw(win)
        self.prev_map.draw(win)
        self.next_map.draw(win)
        # draw the map
        self.map.draw_preview_by_center(win, (WIN_WIDTH/2, WIN_HEIGHT/2))


# ======================================================================


class LoadingScene(SceneBase):
    def __init__(self, kw={}):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        self.loading_text = FixText((WIN_WIDTH/2, WIN_HEIGHT/2), "Loading ...", 30)
        self.ticks = 0

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """
        pass

    def update(self):
        """Game logic for the scene."""
        self.ticks += 1
        # automatically jump to the GameScene after the first cycle
        if self.ticks > 1:
            self.switch_scene(GameScene(self.kw))
    
    def render(self, win):
        """Draw scene on the screen."""
        # clear screen
        win.fill(BLACK)
        # print loading text
        self.loading_text.draw(win)


# ======================================================================


class TemplateScene(SceneBase):
    def __init__(self, kw={}):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
    
    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # move to the next scene when the user pressed Enter
                self.switch_scene(GameScene(self.kw))
        
    def update(self):
        """Game logic for the scene."""
        pass
    
    def render(self, win):
        """Draw scene on the screen."""
        win.fill(HOTPINK)