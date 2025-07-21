import os
import pygame
import math
import random

from settings import *
from global_variables import *
from game_engine.definitions import *
from game_engine.functions_math import *


class Tile:
    minimap_color = HOTPINK
    sprite_coord = (15, 5) # coord of tile on texture pack

    def __init__(self, coord_id, sprite_sheet_base=None):
        """Initialization of the tile."""
        self.sprite_id = 10 * self.sprite_coord[1] + self.sprite_coord[0]
        self.coord_id = coord_id
        self.sprite_base = self.load_and_cut_sprite(sprite_sheet_base)

    def load_and_cut_sprite(self, sprite_sheet, use_alpha=False):
        """Load and crop sprite from sprite table.
        Change use_alpha to True for transparent sprites.
        """
        # crop image
        image = pygame.Surface((TILE_EDGE_LENGTH, TILE_EDGE_LENGTH))
        image.blit(sprite_sheet, (0, 0), (self.sprite_coord[0] * TILE_EDGE_LENGTH, self.sprite_coord[1] * TILE_EDGE_LENGTH, TILE_EDGE_LENGTH, TILE_EDGE_LENGTH))

        # TODO: solve alpha

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
    sprite_coord = (0, 3)

class Snow(Grass):
    minimap_color = WHITE
    sprite_coord = (0, 2)


class Pavement(Grass):
    minimap_color = SILVER
    sprite_coord = (0, 0)

class TGPavement(Pavement):
    minimap_color = SILVER
    sprite_coord = (2, 0)

class Asphalt(Pavement):
    minimap_color = GRAY
    sprite_coord = (0, 1)

class AsphaltLineV(Pavement):
    minimap_color = GRAY
    sprite_coord = (2, 1)

class AsphaltLineH(Pavement):
    minimap_color = GRAY
    sprite_coord = (3, 1)

class AsphaltCrossingV(Pavement):
    minimap_color = GRAY
    sprite_coord = (4, 1)

class AsphaltCrossingH(Pavement):
    minimap_color = GRAY
    sprite_coord = (5, 1)


class Wall(Tile):
    minimap_color = DARKSTEELGRAY
    sprite_coord = (5, 0)

class Tree(Wall):
    minimap_color = GREEN
    sprite_coord = (2, 3)

class SnowTree(Tree):
    minimap_color = HOTPINK
    sprite_coord = (2, 2)


class BarrelPavement(Wall):
    minimap_color = BROWN
    sprite_coord = (1, 0)

class BarrelAsphalt(BarrelPavement):
    minimap_color = BROWN
    sprite_coord = (1, 1)

class BarrelSnow(BarrelPavement):
    minimap_color = BROWN
    sprite_coord = (1, 2)

class BarrelGrass(BarrelPavement):
    minimap_color = BROWN
    sprite_coord = (1, 3)

class Lava(BarrelPavement):
    minimap_color = ORANGE
    sprite_coord = (1, 5)


class Water(Tile):
    minimap_color = BLUE
    sprite_coord = (0, 5)


class Void(Tile):
    minimap_color = RED
    sprite_coord = (12, 5)


TILE_DICT = {
    0: Pavement,
    1: TGPavement,
    2: Tile,
    3: Snow,
    4: Grass,
    5: Tile,
    6: Tile,
    7: Tile,
    8: Tile,
    9: Tile,

    10: Asphalt,
    11: AsphaltLineV,
    12: AsphaltLineH,
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
    31: BarrelPavement,
    32: BarrelAsphalt,
    33: BarrelSnow,
    34: BarrelGrass,
    35: Lava,
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
            raise FileNotFoundError("NO MAP FILE!")
        
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
            self.base_surface_width = self.base_surface.get_width()
            self.base_surface_height = self.base_surface.get_height()

    def draw_preview(self, win, coord):
        """Draw the preview Map on the screen.
        The anchor point is the upper left corner."""
        win.blit(self.preview_map, coord)

    # get_rect() anchor points:
    # topleft, bottomleft, topright, bottomright
    # midtop, midleft, midbottom, midright
    # center, centerx, centery

    def draw_preview_by_center(self, win, center_coord):
        """Draw the preview Map on the screen.
        The anchor point is the map center point."""
        new_rect = self.preview_map.get_rect(center = center_coord)
        win.blit(self.preview_map, new_rect.topleft)

    def draw_preview_by_midtop(self, win, midtop_coord):
        """Draw the preview Map on the screen.
        The anchor point is the map midtop point."""
        new_rect = self.preview_map.get_rect(midtop = midtop_coord)
        win.blit(self.preview_map, new_rect.topleft)

    def draw_preview_by_topright(self, win, topright_coord):
        """Draw the preview Map on the screen.
        The anchor point is the map topright point."""
        new_rect = self.preview_map.get_rect(topright = topright_coord)
        win.blit(self.preview_map, new_rect.topleft)

    def draw(self, win, offset_x: int, offset_y: int, scale, screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT):
        """Draw the Map on the screen."""
        if scale >= 0.5:
            cropped_original_image = pygame.Surface((screen_width // scale, screen_height // scale))
            cropped_original_image.blit(self.base_surface, (offset_x, offset_y))
            scaled_image = pygame.transform.scale(cropped_original_image, (screen_width, screen_height))
            win.blit(scaled_image, (screen_pos_x, screen_pos_y))
        else:
            buffer_surface = pygame.Surface((screen_width, screen_height))
            scaled_image = pygame.transform.scale(self.base_surface, (int(scale * self.base_surface_width), int(scale * self.base_surface_height)))
            buffer_surface.blit(scaled_image, (offset_x*scale, offset_y*scale))
            win.blit(buffer_surface, (screen_pos_x, screen_pos_y))

    def draw_cropped_map(self, win, offset_x: int, offset_y: int, screen_pos_x=0, screen_pos_y=0, screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT):
        """Draw cropped Map on the screen."""
        win.blit(self.base_surface, (screen_pos_x, screen_pos_y), (- offset_x, - offset_y, screen_width, screen_height))

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
        sprite_sheet_base = self.load_sprite_sheet(os.path.join(*MAP_SPRITES_BASE_PATH))
        for y, str_row in enumerate(map_str_array):
            tile_row = []
            for x, tile in enumerate(str_row):
                tile_row.append(TILE_DICT[int(tile)]((x, y), sprite_sheet_base))
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

    def load_sprite_sheet(self, path, use_alpha=False):
        """Load sprite sheet from sprite table.
        Change use_alpha to True for transparent sprites.
        """
        try:
            sprite_sheet = pygame.image.load(path)
        except FileNotFoundError:
            raise FileNotFoundError("NO TEXTURE PACK FILE!")
        # sprite_sheet.convert()

        # TODO: solve alpha
        
        # if use_alpha:
        #     image_alpha = pygame.Surface.convert_alpha(image)
		#     image_alpha.set_colorkey(HOTPINK)
        #     return image_alpha
        # else:
        #     return image 
        # # image.convert()
        # image.set_colorkey(HOTPINK) # for transparency

        return sprite_sheet


    # def draw_grid(self, win, offset_x: int, offset_y: int, scale):
    #     """Draw grid of the Map on the screen."""
    #     pass

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
    
