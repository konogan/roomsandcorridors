# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pygame

from src.Constants import Coord, MyColors, Direction
from src.actors.PlayerInventory import PlayerInventory


class Player:
    def __init__(self, coord_x: int, coord_y: int, room_id=1):
        """
        Args:
            coord_x:
            coord_y:
            room_id:
        """
        self.coord = Coord(coord_x, coord_y)
        self.orientation = Direction.NORTH
        self.current_room = room_id
        self.view_distance = 3
        self.inventory = PlayerInventory()
        self.font_size = 15
        self.font = pygame.font.SysFont('arial', self.font_size)

    def move(self, new_coord, room_id):
        """
        Args:
            new_coord:
            room_id:
        """
        self.current_room = room_id
        self.coord = new_coord

    def orient(self, direction):
        """
        Args:
            direction:
        """
        self.orientation = direction

    def pick_item(self, item):
        # TODO picked item that can be equipped ?
        # available slot in player ?
        # auto equip sword ? torch ? shield ?

        # if item.type == "TORCH":
        #     self.view_distance = 8

        """
        Args:
            item:
        """
        self.inventory.add(item)

    def drop_item(self, item):
        # TODO drop item on the world at current location
        # for the moment remove the item from the inventory
        """
        Args:
            item:
        """
        self.inventory.remove(item)

    def render(self, world_surface: pygame.Surface, tile_size):
        angle = 0

        # local_rect = pygame.Rect((0, 0), tile_size)
        local_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)

        world_rect = pygame.Rect((self.coord.x * tile_size, self.coord.y * tile_size), (tile_size,tile_size))

        pygame.draw.polygon(local_surface, MyColors.PLAYER.value, (
            (int(tile_size // 2), 0),
            (0, tile_size),
            (tile_size, tile_size)))

        if self.orientation == Direction.NORTH:
            angle = 0
        if self.orientation == Direction.EAST:
            angle = -90
        if self.orientation == Direction.SOUTH:
            angle = 180
        if self.orientation == Direction.WEST:
            angle = 90

        rotated_surface = pygame.transform.rotate(local_surface, angle)

        world_surface.blit(rotated_surface, world_rect)
