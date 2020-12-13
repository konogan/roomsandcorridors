# encoding: utf-8


import pygame

from src.Constants import Coord, MyColors


class Room():
    """Represent a room in the game"""

    def __init__(self, coord_x, coord_y, width, height, room_id):
        self.coord = Coord(coord_x, coord_y)
        self.width = width
        self.height = height
        self.room_id = room_id

    def get_center(self):
        return self.coord.x + int(self.width/2), self.coord.y + int(self.height/2)

    def render(self, world_surface, tile_size, offset=(0, 0)):
        cell_font = pygame.font.SysFont('arial', 18)
        number = cell_font.render("{}".format(
            self.room_id), True, MyColors.RED.value)
        room_rect = pygame.Rect(
            self.coord.x*tile_size,
            self.coord.y*tile_size,
            tile_size,
            tile_size)
        world_surface.blit(number, room_rect)
