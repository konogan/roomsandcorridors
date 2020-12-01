# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pygame


class GameStats():
    def __init__(self, settings, surface):
        self.settings = settings
        self.messages = []
        self.surface = surface
        self.font_size = 15
        self.font = pygame.font.SysFont('arial', self.font_size)

    def add_message(self, text):
        self.messages.append(text)

    def player_move(self, direction):
        if direction is None:
            self.add_message('You hit the wall')
        else:
            if direction[1] < 0:
                orientation = "North"
            if direction[1] > 0:
                orientation = "South"
            if direction[0] > 0:
                orientation = "East"
            if direction[0] < 0:
                orientation = "West"
            self.add_message('You head '+orientation)

    def render(self):
        # fill black
        self.surface.fill((0, 0, 0))

        # draw border
        pygame.draw.line(self.surface, (255, 255, 255), (0, 1),
                         (0, self.settings.screen_height))

        # display last messages
        for index, msg in enumerate(self.messages[-10:]):
            message = self.font.render("{}".format(msg), True, (255, 255, 255))
            rect = pygame.Rect(
                10,
                10 + index * (self.font_size+3),
                self.settings.ui_width,
                self.settings.screen_height)

            self.surface.blit(message, rect)
