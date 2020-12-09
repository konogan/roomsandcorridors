# encoding: utf-8

import pygame

from src.Constants import MyColors


class PickableItem():
    def __init__(self, name=""):
        """
        Args:
            name (str): Name of the item
        """
        self.name = name
        self.color = MyColors.ITEM.value
        self.is_selected = False

    def __repr__(self):
        return '{}'.format(self.name.lower().capitalize())

    def __print__(self):
        return '{}'.format(self.name.lower().capitalize())

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return NotImplemented

    def render_surface(self, tile_size: int):
        """
        Args:
            tile_size (int):
        """
        local_surface = pygame.Surface((tile_size, tile_size))
        local_rect = pygame.Rect(0, 0, tile_size, tile_size)
        pygame.draw.rect(local_surface, self.color, local_rect)
        return local_surface


class Torch(PickableItem):
    def __init__(self):
        PickableItem.__init__(self, __class__.__name__)
        self.color = MyColors.ITEM.value


class Sword(PickableItem):
    def __init__(self):
        PickableItem.__init__(self, __class__.__name__)
        self.color = MyColors.ITEM.value


class SilverCoin(PickableItem):
    def __init__(self):
        PickableItem.__init__(self, __class__.__name__)
        self.color = MyColors.ITEM.value


class CopperCoin(PickableItem):
    def __init__(self):
        PickableItem.__init__(self, __class__.__name__)
        self.color = MyColors.ITEM.value
