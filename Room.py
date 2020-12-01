# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


import pygame

from Constants import Coord, My_colors


class Room():
    def __init__(self, coord_x, coord_y, width, height, room_id):
        self.coord = Coord(coord_x, coord_y)
        self.width = width
        self.height = height
        self.room_id = room_id
        self.is_reachable = False

    def get_center(self):
        return self.coord.x + int(self.width/2), self.coord.y + int(self.height/2)

    def to_json(self):
        export = {}
        export['x'] = self.coord.x
        export['y'] = self.coord.y
        export['w'] = self.width
        export['h'] = self.height
        export['i'] = self.room_id
        return export

    def render(self, screen, tile_size, offset=(0, 0)):
        cell_font = pygame.font.SysFont('arial', 18)
        number = cell_font.render("{}".format(
            self.room_id), True, My_colors.RED.value)
        rect = pygame.Rect(
            (self.coord.x-offset[0])*tile_size,
            (self.coord.y-offset[1])*tile_size,
            tile_size,
            tile_size)
        screen.blit(number, rect)
