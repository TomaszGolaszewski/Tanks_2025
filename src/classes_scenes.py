import os
import pygame

from settings import *
from game_engine.scenes import *
from game_engine.scenes_features import *
from classes_map import *
# from classes_trains import *
from classes_scenes_game import *


class TitleScene(SceneBase):
    def __init__(self):
        """Initialization of the scene."""
        SceneBase.__init__(self)
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
                            self.switch_scene(BrowseMapsScene({"game_mode": button.option}))
                  
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


class LoadingScene(SceneBase):
    def __init__(self, kw):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        self.loading_text = FixText((WIN_WIDTH/2, WIN_HEIGHT/2), "Loading ...", 30)
        self.ticks = 0

    # def process_input(self, events, keys_pressed):
    #     """
    #     Receive all the events that happened since the last frame.
    #     Handle all received events.
    #     """
    #     pass

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


class BrowseMapsScene(SceneBase):
    def __init__(self, kw):
        """Initialization of the scene."""
        SceneBase.__init__(self, kw)
        self.map = Map(os.path.join("maps", "Testowa_v21.txt"))
        # self.loading_text = FixText((WIN_WIDTH/2, WIN_HEIGHT/2), "Loading ...", 30)
        # self.ticks = 0

    def process_input(self, events, keys_pressed):
        """
        Receive all the events that happened since the last frame.
        Handle all received events.
        """
        pass
        
    def update(self):
        """Game logic for the scene."""
        pass
        # self.ticks += 1
        # # automatically jump to the GameScene after the first cycle
        # if self.ticks > 1:
        #     self.switch_scene(GameScene(self.kw))
    
    def render(self, win):
        """Draw scene on the screen."""
        pass
        # clear screen
        win.fill(BLACK)
        # draw
        self.map.draw(win)
        self.map.draw_preview(win)


# ======================================================================


class TemplateScene(SceneBase):
    def __init__(self, kw):
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