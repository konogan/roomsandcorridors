# encoding: utf-8


import pygame

from src.Constants import MyColors
from src.items.Inventory import Inventory


class PlayerInventory(Inventory):
    def __init__(self):
        Inventory.__init__(self)
        self.selected_item_index = 0
        self.font_size = 15
        self.item_font = pygame.font.Font('./src/assets/basis33.ttf', self.font_size)
        self.title_font = pygame.font.Font('./src/assets/basis33.ttf', 30)

    def select(self, selected_item_index):
        """
        Args:
            selected_item_index:
        """
        self.selected_item_index = selected_item_index

    def render(self, inventory_surface):
        """
        Args:
            inventory_surface:
        """
        index = 0
        item_width = 64
        item_height = 64
        item_size = (item_width, item_height)

        margin = 10
        nb_item_per_line = 5

        # clean
        inventory_surface.fill(MyColors.BACKGROUND.value)

        # display command and title
        title = self.title_font.render("Inventory", True, MyColors.TEXT.value)
        title_rect = pygame.Rect((margin, margin), (500, 40))
        inventory_surface.blit(title, title_rect)

        title = self.item_font.render(
            "Use [arrows] to select an item, [e]quip it or [d]rop it", True, MyColors.TEXT.value)
        title_rect = pygame.Rect((margin, margin+50), (500, self.font_size))
        inventory_surface.blit(title, title_rect)

        # display items
        while index < len(self.items):
            # compute coordinates and local surfaces
            item_x = (index % nb_item_per_line) * item_width + margin
            item_y = int(index/nb_item_per_line) * item_height + margin + 100
            item_rect = pygame.Rect((item_x, item_y), item_size)
            item_surface = pygame.Surface(item_size)
            item_local_rect = pygame.Rect((0, 0), item_size)

            # background
            pygame.draw.rect(item_surface, MyColors.BACKGROUND_LIGHT.value, item_local_rect)

            # frame
            # highlight selected Index
            if index == self.selected_item_index:
                pygame.draw.rect(
                    item_surface, MyColors.SELECTED.value, item_local_rect, 2)
            else:
                pygame.draw.rect(
                    item_surface, MyColors.WHITE.value, item_local_rect, 2)

            # legend
            item_label = "{}".format(
                str(self.items[index]) + "->" + str(self.quantities[index]))
            item_legend = self.item_font.render(
                item_label, True, MyColors.TEXT.value)

            # item_legend_size = item_legend.get_size()
            # TODO place legend bottom right
            item_surface.blit(item_legend, item_local_rect)

            # push item on inventory surface
            inventory_surface.blit(item_surface, item_rect)
            index += 1
