# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


import pygame


from Constants import My_colors


class Item():
    def __init__(self, item_type=None, pickable=True):
        self.type = item_type
        self.pickable = pickable

    def __repr__(self):
        return '<Item type='+str(self.type)+'>'

    def __str__(self):
        return str(self.type)

    def render_surface(self, tile_size):
        local_surface = pygame.Surface((tile_size, tile_size))
        local_rect = pygame.Rect(0, 0, tile_size, tile_size)
        cell_color = My_colors.ITEM
        pygame.draw.rect(local_surface, cell_color.value, local_rect)
        return local_surface


class Chest(Item):
    def __init__(self):
        Item.__init__(self, 'CHEST')
        self.content = []

    def add_item(self, item_to_add):
        self.content.append(item_to_add)

    def pick_item(self, item_to_pick):
        self.content.remove(item_to_pick)
        return item_to_pick


class Torch(Item):
    def __init__(self):
        Item.__init__(self, 'TORCH')
        self.duraction = 20
