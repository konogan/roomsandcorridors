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
        self.visibility = False
        self.was_discovered = False
        self.last_time_was_seen = 0
        self.distance = 0

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

    def block_fov(self):
        return self.type == "WALL" or self.type == "DOOR"

    def set_visibility(self, visibility, current_turn, distance_from_player=0):
        self.visibility = visibility
        self.distance = distance_from_player
        if visibility:
            self.last_time_was_seen = current_turn
            self.was_discovered = True
        else:
            # number of turn of memory
            if current_turn - self.last_time_was_seen > 100:
                self.was_discovered = False

    def toJson(self):
        export = {}
        export['x'] = self.coord.x
        export['y'] = self.coord.y
        export['f'] = self.is_free
        export['b'] = self.belongs_to
        export['t'] = self.type
        export['v'] = self.visibility
        export['d'] = self.was_discovered
        export['s'] = self.last_time_was_seen
        return export

    def fromJson(self, json_data):
        self.is_free = json_data['f']
        self.belongs_to = json_data['b']
        self.type = json_data['t']
        self.visibility = json_data['v']
        self.was_discovered = json_data['d']
        self.last_time_was_seen = json_data['s']

    def render(self, surface, tile_size, offset=(0, 0), debug=False):

        if self.type == "WALL":
            cell_color = mycolors.GREY
            cell_color_in_memory = mycolors.GREY
        elif self.type == "ROOM":
            cell_color = mycolors.WHITE
            cell_color_in_memory = mycolors.GREY
        elif self.type == "CORRIDOR":
            cell_color = mycolors.WHITE
            cell_color_in_memory = mycolors.GREY
        elif self.type == "DOOR":
            cell_color = mycolors.GREEN
            cell_color_in_memory = mycolors.GREY
        else:
            cell_color = mycolors.BLACK

        rect = pygame.Rect(
            (self.coord.x-offset[0])*tile_size,
            (self.coord.y-offset[1])*tile_size,
            tile_size,
            tile_size
        )

        if self.visibility:
            pygame.draw.rect(surface, cell_color, rect)
        else:
            if self.was_discovered:
                # TODO change opacity based on time since discovering
                pygame.draw.rect(surface, cell_color_in_memory, rect)

        if debug and self.visibility:
            cell_font = pygame.font.SysFont('arial', 15)
            number = cell_font.render("{}".format(
                self.distance), True, (0, 0, 255))

            rect = pygame.Rect(
                (self.coord.x-offset[0])*tile_size,
                (self.coord.y-offset[1])*tile_size,
                tile_size,
                tile_size)
            surface.blit(number, rect)
