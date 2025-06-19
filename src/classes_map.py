import os
import pygame
import math
import random

from settings import *
from global_variables import *
from game_engine.definitions import *
from game_engine.functions_math import *


# TILE_DICT = {
#     0: SILVER,
#     1: SILVER,
#     2: SILVER,
#     3: WHITE, # snow
#     4: GREEN,
#     5: SILVER,
#     6: BLUE,
#     7: RED,
#     8: GREEN,
#     9: YELLOW,

#     10: GRAY,
#     11: GRAY,
#     12: GRAY,
#     13: WHITE, # snow
#     14: GREEN,
#     15: SILVER,
#     16: BLUE,
#     17: RED,
#     18: GREEN,
#     19: YELLOW,

#     25: SILVER,
#     26: BLUE,
#     27: RED,
#     28: GREEN,
#     29: YELLOW,

#     30: DARKSTEELGRAY,
#     31: SILVER,
#     32: GRAY,
#     33: WHITE, # snow
#     34: GREEN,
#     35: ORANGE, # lava
#     36: BLUE,
#     37: RED,
#     38: GREEN,
#     39: YELLOW,

#     42: BLUE, # water
#     43: WHITE, # snow tree
#     44: GREEN,
#     45: GRAY,
#     46: BLUE,
#     47: RED,
#     48: GREEN,
#     49: YELLOW,

#     110: RED, # old map border 
# }


class Tile:
    minimap_color = HOTPINK
    sprite_coord = (0, 0)

    def __init__(self, coord_id):
        """Initialization of the tile."""
        self.coord_id = coord_id
        self.sprite_base = self.load_and_cut_sprite(os.path.join(*MAP_SPRITES_BASE_PATH))

    def load_and_cut_sprite(self, path, use_alpha=False):
        """Load and crop sprite from sprite table.
        Change use_alpha to True for transparent sprites.
        """
        # load and prepare sprite sheet
        sprite_sheet = pygame.image.load(path)
        # sprite_sheet.convert()

        # crop image
        image = pygame.Surface((TILE_EDGE_LENGTH, TILE_EDGE_LENGTH))
        image.blit(sprite_sheet, (0, 0), (self.sprite_coord[0] * TILE_EDGE_LENGTH, self.sprite_coord[1] * TILE_EDGE_LENGTH, TILE_EDGE_LENGTH, TILE_EDGE_LENGTH))

        # if use_alpha:
        #     image_alpha = pygame.Surface.convert_alpha(image)
		#     image_alpha.set_colorkey(HOTPINK)
        #     return image_alpha
        # else:
        #     return image 
        # # image.convert()
        # image.set_colorkey(HOTPINK) # for transparency
        return image

    def draw_base(self, surface):
        """Draw base of the Tile on the surface."""
        surface.blit(self.sprite_base, (self.coord_id[0] * TILE_EDGE_LENGTH, self.coord_id[1] * TILE_EDGE_LENGTH))


class Grass(Tile):
    minimap_color = GRASS
    sprite_coord = (0, 4)

class Snow(Grass):
    minimap_color = WHITE
    sprite_coord = (0, 3)


class Wall(Tile):
    minimap_color = DARKSTEELGRAY
    sprite_coord = (3, 0)

class Tree(Wall):
    minimap_color = GREEN
    sprite_coord = (4, 4)

class SnowTree(Tree):
    minimap_color = HOTPINK
    sprite_coord = (4, 3)


class Water(Tile):
    minimap_color = BLUE
    sprite_coord = (4, 2)


class Void(Tile):
    minimap_color = RED
    sprite_coord = (11, 0)

TILE_DICT = {
    0: Tile,
    1: Tile,
    2: Tile,
    3: Snow,
    4: Grass,
    5: Tile,
    6: Tile,
    7: Tile,
    8: Tile,
    9: Tile,

    10: Tile,
    11: Tile,
    12: Tile,
    13: Tile,
    14: Tile,
    15: Tile,
    16: Tile,
    17: Tile,
    18: Tile,
    19: Tile,

    20: Tile,
    21: Tile,
    22: Tile,
    23: Tile,
    24: Tile,
    25: Tile,
    26: Tile,
    27: Tile,
    28: Tile,
    29: Tile,

    30: Wall,
    31: Tile,
    32: Tile,
    33: Tile,
    34: Tile,
    35: Tile,
    36: Tile,
    37: Tile,
    38: Tile,
    39: Tile,

    40: Tile,
    41: Tile,
    42: Water,
    43: SnowTree,
    44: Tree,
    45: Tile,
    46: Tile,
    47: Tile,
    48: Tile,
    49: Tile,

    110: Void,
}

# ======================================================================


class Map:
    def __init__(self, path_to_file, preview_only=False):
        """Initialization of the map."""
        self.path_to_file = path_to_file
        self.map_tile_ids_array = []
        try:
            with open(path_to_file) as file:
                # print(file.read()) 
                a, b, c = file.readline().split('\t')
                read_map_structure = file.readlines()
        except FileNotFoundError:
            raise FileNotFoundError("NO FILE!")
        
        # print(a)
        # print(b)
        # print(c)
        self.row_length = 0
        for line in read_map_structure:
            row = line.replace("\t\n", "").split('\t')
            if not self.row_length:
                self.row_length = len(row)
            if self.row_length != len(row):
                raise ValueError("FILE LINES ARE OF DIFFERENT LENGTH!")
            self.map_tile_ids_array.append(row)
        self.column_length = len(self.map_tile_ids_array)

        self.preview_map = self.create_preview_map(self.map_tile_ids_array, 5)

        if not preview_only: # do not create a whole map if we only need a preview
            self.map_tile_obj_array = self.create_tiles_array(self.map_tile_ids_array)
            self.base_surface = self.create_sprites_map(self.map_tile_obj_array)

    def draw_preview(self, win, coord):
        """Draw the preview Map on the screen.
        The anchor point is the upper left corner."""
        win.blit(self.preview_map, coord)

    def draw_preview_by_center(self, win, center_coord):
        """Draw the preview Map on the screen.
        The anchor point is the map center point."""
        new_rect = self.preview_map.get_rect(center = center_coord)
        win.blit(self.preview_map, new_rect.topleft)

    def draw(self, win):#, offset_x: int, offset_y: int, scale):
        """Draw the Map on the screen."""
        win.blit(self.base_surface, (100, 50))

    def create_preview_map(self, map_str_array: list[list], pixel_size: int):
        """Create canvas with preview map."""
        canvas = pygame.Surface((self.row_length * pixel_size, self.column_length * pixel_size))
        canvas.fill(HOTPINK)
        for y, row in enumerate(map_str_array):
            for x, tile in enumerate(row):
                pygame.draw.rect(canvas, TILE_DICT[int(tile)].minimap_color, [x*pixel_size, y*pixel_size, pixel_size, pixel_size])
        return canvas
    
    def create_tiles_array(self, map_str_array: list[list]):
        """Create array with map tiles objects."""
        map_tiles_array = []
        for y, str_row in enumerate(map_str_array):
            tile_row = []
            for x, tile in enumerate(str_row):
                tile_row.append(TILE_DICT[int(tile)]((x, y)))
            map_tiles_array.append(tile_row)
        return map_tiles_array

    def create_sprites_map(self, map_tiles_array: list[list]):
        """Create canvas with map built with sprites."""
        canvas = pygame.Surface((self.row_length * TILE_EDGE_LENGTH, self.column_length * TILE_EDGE_LENGTH))
        canvas.fill(HOTPINK)
        for row in map_tiles_array:
            for tile in row:
                tile.draw_base(canvas)
        return canvas


    # def draw(self, win, offset_x: int, offset_y: int, scale):
    #     """Draw the Map on the screen."""
    #     pass
        # for tile_id in self.dict_with_tiles:
        #     tile = self.dict_with_tiles[tile_id]
        #     tile.draw(win, offset_x, offset_y, scale)

    # def draw_grid(self, win, offset_x: int, offset_y: int, scale):
    #     """Draw grid of the Map on the screen."""
    #     pass
        # tile_top_left_coord_id = self.world2id(screen2world((0, 0), offset_x, offset_y, scale))
        # tile_bottom_right_coord_id = self.world2id(screen2world((WIN_WIDTH, WIN_HEIGHT), offset_x, offset_y, scale))
        # for x_id in range(tile_top_left_coord_id[0], tile_bottom_right_coord_id[0] + 1):
        #     for y_id in range(tile_top_left_coord_id[1], tile_bottom_right_coord_id[1] + 1):
        #         coord_screen = world2screen(self.id2world((x_id, y_id)), offset_x, offset_y, scale) 
        #         pygame.draw.circle(win, WHITE, coord_screen, 10*scale, 1)

    # def id2world(self, coord_id: tuple[int, int]) -> tuple[float, float]:
    #     """Calculate coordinates from tile's id to world coordinate system.
    #     Return coordinates in the world coordinate system."""
    #     x_id, y_id = coord_id
    #     if y_id % 2:
    #         x_world = (2 * x_id + 1) * self.inner_tile_radius
    #     else:
    #         x_world = 2 * x_id * self.inner_tile_radius
    #     y_world = 3 / 2 * self.outer_tile_radius * y_id
    #     return (x_world, y_world)

    # def world2id(self, coord_world: tuple[float, float]) -> tuple[int, int]:
    #     """Calculate coordinates from world coordinate system to tile's id.
    #     Return tile's id coordinates."""
    #     x_world, y_world = coord_world
    #     y_id = math.floor(2 / 3 * y_world / self.outer_tile_radius + 0.5)
    #     if y_id % 2:
    #         x_id = math.floor(x_world / self.inner_tile_radius / 2)
    #     else:
    #         x_id = math.floor(x_world / self.inner_tile_radius / 2 + 0.5)
    #     return (x_id, y_id)
    
