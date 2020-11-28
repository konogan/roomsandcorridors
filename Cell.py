# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from collections import namedtuple
import pygame

import mycolors

Coord = namedtuple('Coord', 'x y')

class Cell():

    def __init__(self, coord_x, coord_y):
        self.coord = Coord(coord_x, coord_y)
        self.is_free = True
        self.belongs_to = 0
        self.type = None

    def belong_to_room(self, room_id):
        self.is_free = False
        self.belongs_to = room_id
        self.type = "ROOM"

    def set_corridor(self):
        self.is_free = False
        self.belongs_to = 0
        self.type = "CORRIDOR"

    def set_door(self):
        self.is_free = False
        self.type = "DOOR"

    def set_wall(self):
        self.type = "WALL"
        
    def is_walkable(self):
        return self.type != "WALL"
       

    def toJson(self):
        export = {}
        export['x'] = self.coord.x
        export['y'] = self.coord.y
        export['f'] = self.is_free
        export['b'] = self.belongs_to
        export['t'] = self.type
        return export

    def fromJson(self, json_data):
        self.is_free = json_data['f']
        self.belongs_to = json_data['b']
        self.type = json_data['t']

    def render(self, surface, tile_size,offset=(0,0)):
        if self.type == "WALL":
            cell_color = mycolors.GREY
        elif self.type == "ROOM":
            cell_color = mycolors.WHITE
        elif self.type == "CORRIDOR":
            cell_color = mycolors.WHITE
        elif self.type == "DOOR":
            cell_color = mycolors.GREEN
        else:
            cell_color = mycolors.BLACK

        rect = pygame.Rect(
            (self.coord.x-offset[0])*tile_size,
            (self.coord.y-offset[1])*tile_size,
            tile_size,
            tile_size
        )
        pygame.draw.rect(surface, cell_color, rect)
