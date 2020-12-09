# encoding: utf-8


import pygame

from src.Constants import Coord, MyColors


class Room():
    """Represent a room in the game"""

    def __init__(self, coord_x, coord_y, width, height, room_id):
        """Constructor

        Args:
            coord_x (int): X coordinate
            coord_y (int): Y coordinate
            width (int): Width
            height (int): Heigh
            room_id (int): id of the room
        """
        self.coord = Coord(coord_x, coord_y)
        self.width = width
        self.height = height
        self.room_id = room_id

    def get_center(self):
        """Return coordinates of the center of the room

        Returns:
            tuple: center of the room
        """
        return self.coord.x + int(self.width/2), self.coord.y + int(self.height/2)

    def render(self, screen, tile_size, offset=(0, 0)):
        """render

        Args:
            screen (pygame.Surface): Destination Surface
            tile_size (int): size of each tile
            offset (tuple, optional): camera offset. Defaults to (0, 0).
        """
        cell_font = pygame.font.SysFont('arial', 18)
        number = cell_font.render("{}".format(
            self.room_id), True, MyColors.RED.value)
        rect = pygame.Rect(
            (self.coord.x-offset[0])*tile_size,
            (self.coord.y-offset[1])*tile_size,
            tile_size,
            tile_size)
        screen.blit(number, rect)
