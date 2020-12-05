# encoding: utf-8
import pygame.ftfont


class Button():

    def __init__(self, ident, surface, msg, decy):
        """This is a button yo"""
        self.surface = surface
        self.ident = ident
        self.hover = False
        self.surface_rect = surface.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 500, 50
        self.button_color = (0, 0, 0)
        self.button_color_hover = (125, 125, 125)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.surface_rect.center
        self.rect.centery = self.rect.centery + decy
        # The button message needs to be prepped only once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_hover = self.font.render(
            msg, True, self.text_color, self.button_color_hover)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def render(self):
        if self.hover:
            self.surface.fill(self.button_color_hover, self.rect)
            self.surface.blit(self.msg_image_hover, self.msg_image_rect)
        else:
            self.surface.fill(self.button_color, self.rect)
            self.surface.blit(self.msg_image, self.msg_image_rect)
