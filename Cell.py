# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from collections import namedtuple
import mycolors

import pygame

Coord = namedtuple('Coord', 'x y')

class Cell():
    def __init__(self,coord_x,coord_y):
        self.coord = Coord(coord_x,coord_y)
        self.is_free = True
        self.belongs_to = None
        self.type = None
 
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def belong_to_room(self,room_id):
        self.is_free = False
        self.belongs_to = room_id
        self.type = "ROOM"
    
    def set_corridor(self):
        self.is_free = False
        self.type = "CORRIDOR"
        
    def set_door(self):
        self.is_free = False
        self.type = "DOOR"
    
    def set_wall(self):
        self.type = "WALL"
        
    def render(self,screen,tile_size):
        if self.type=="WALL":
            cell_color = mycolors.GREY
        elif self.type=="ROOM":
            cell_color =  mycolors.WHITE
        elif self.type=="CORRIDOR":
            cell_color =  mycolors.WHITE
        elif self.type=="DOOR":
            cell_color =  mycolors.GREEN
        else:
            cell_color = mycolors.BLACK
        
        rect = pygame.Rect(
            self.coord.x*tile_size,
            self.coord.y*tile_size,
            tile_size,
            tile_size
        )
        pygame.draw.rect(screen, cell_color,rect)