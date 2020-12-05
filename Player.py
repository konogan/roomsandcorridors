# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pygame

from Constants import Coord, My_colors, Direction


class Player():
    def __init__(self, coord_x, coord_y, room_id):
        self.coord = Coord(coord_x, coord_y)
        self.orientation = Direction.NORTH
        self.current_room = room_id
        self.view_distance = 3
        self.inventory = []

    def move(self, new_coord, room_id):
        self.current_room = room_id
        self.coord = new_coord

    def orient(self, direction):
        self.orientation = direction

    def pick_item(self, item):
        if item.type == "TORCH":
            self.view_distance = 8
        self.inventory.append(item)

    def drop_item(self, item):
        # TODO drop item on the world at current location
        pass

    def render(self, world_surface, tile_size, offset=(0, 0)):
        local_rect = pygame.Rect(0, 0, tile_size, tile_size)

        local_surface = pygame.Surface((tile_size, tile_size))

        world_rect = pygame.Rect(
            (self.coord.x-offset[0])*tile_size,
            (self.coord.y-offset[1])*tile_size,
            tile_size,
            tile_size
        )

        pygame.draw.rect(local_surface, My_colors.WHITE.value, local_rect)
        pygame.draw.polygon(local_surface, My_colors.PLAYER.value, (
            (int(tile_size//2), 0),
            (0, tile_size),
            (tile_size, tile_size))
        )

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
