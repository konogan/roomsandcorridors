# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from collections import namedtuple
import pygame

Coord = namedtuple('Coord', 'x y')


class Player():
    def __init__(self, coord_x, coord_y,room_id):
        self.coord = Coord(coord_x, coord_y)
        self.orientation = "N"
        self.current_room = room_id

    def move(self, direction,room_id):
        if direction[1] < 0:
            self.orientation = "N"
        if direction[1] > 0:
            self.orientation = "S"
        if direction[0] > 0:
            self.orientation = "E"
        if direction[0] < 0:
            self.orientation = "W"

        self.current_room = room_id
        
        self.coord = Coord(
            self.coord.x + direction[0],
            self.coord.y + direction[1])

    def render(self, surface, tile_size):
        rect = pygame.Rect(
            self.coord.x*tile_size,
            self.coord.y*tile_size,
            tile_size,
            tile_size
        )
        pygame.draw.rect(surface, (160, 32, 240), rect)
