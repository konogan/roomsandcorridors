# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


import pygame


from Constants import My_colors


class PickableItem():
    def __init__(self, name=None):
        self.name = name
        self.color = My_colors.ITEM.value

    def __repr__(self):
        return '{}'.format(self.name.lower().capitalize())

    def __print__(self):
        return '{}'.format(self.name.lower().capitalize())

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return NotImplemented

    def render_surface(self, tile_size):
        local_surface = pygame.Surface((tile_size, tile_size))
        local_rect = pygame.Rect(0, 0, tile_size, tile_size)
        pygame.draw.rect(local_surface, self.color, local_rect)
        return local_surface


class Torch(PickableItem):
    def __init__(self):
        PickableItem.__init__(self, __class__.__name__)
        self.color = My_colors.ITEM.value


class Sword(PickableItem):
    def __init__(self):
        PickableItem.__init__(self, __class__.__name__)
        self.color = My_colors.ITEM.value


class SilverCoin(PickableItem):
    def __init__(self):
        PickableItem.__init__(self, __class__.__name__)
        self.color = My_colors.ITEM.value


class CopperCoin(PickableItem):
    def __init__(self):
        PickableItem.__init__(self, __class__.__name__)
        self.color = My_colors.ITEM.value
