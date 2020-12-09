# encoding: utf-8
import pygame

from src.Constants import MyColors


class Button:
    """Represent a button in the interface
    """    
    def __init__(self, button_id, surface, msg, offset_y):
        """
        Args:
            button_id:
            surface:
            msg:
            offset_y:
        """
        self.surface = surface
        self.button_id = button_id
        self.hover = False
        self.surface_rect = surface.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 500, 50
        self.button_color = MyColors.BLACK.value
        self.button_color_hover = MyColors.BACKGROUND_LIGHT.value
        self.text_color = MyColors.TEXT.value
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.surface_rect.center
        # self.rect.centery = self.rect.centery + offset_y
        # The button message needs to be prepped only once.
        self.__prep_msg(msg)

    def __prep_msg(self, msg):
        """
        Args:
            msg:
        """
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_hover = self.font.render(
            msg, True, MyColors.SELECTED.value, self.button_color_hover)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def render(self):
        if self.hover:
            self.surface.fill(self.button_color_hover, self.rect)
            self.surface.blit(self.msg_image_hover, self.msg_image_rect)
        else:
            self.surface.fill(self.button_color, self.rect)
            self.surface.blit(self.msg_image, self.msg_image_rect)
