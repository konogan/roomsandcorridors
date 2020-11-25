# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from collections import namedtuple

import pygame

Coord = namedtuple('Coord', 'x y')

class Room():
    def __init__(self,coord_x,coord_y,width,height,room_id):
        self.coord          = Coord(coord_x,coord_y)
        self.width          = width
        self.height         = height
        self.room_id        = room_id
        self.is_reachable   = False
    
    def render(self,screen,tile_size):
        cell_font = pygame.font.SysFont('arial', 15)
        number = cell_font.render( "{}".format(self.room_id), True, (0,0,255))
        rect = pygame.Rect(
            self.coord.x*tile_size,
            self.coord.y*tile_size,
            tile_size,
            tile_size)
        screen.blit(number,rect)
  