# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pygame
from Constants import Direction


class Messages():
    def __init__(self, settings, surface):
        self.settings = settings
        self.messages = []
        self.surface = surface
        self.font_size = 15
        self.font = pygame.font.Font('assets/basis33.ttf', self.font_size)
        self.add_message("You arrive in a dark room")
        self.add_message("-------------------------")
        self.add_message("Move with the arrows")
        self.add_message("(o)pen door/chest")
        self.add_message("(c)lose door/chest")
        self.add_message("(p)ick item")
        self.add_message("-------------------------")

    def add_message(self, text):
        self.messages.append(text)

    def player_move(self, orientation):
        if orientation == Direction.NORTH:
            orientation_word = "North"
        if orientation == Direction.SOUTH:
            orientation_word = "South"
        if orientation == Direction.EAST:
            orientation_word = "East"
        if orientation == Direction.WEST:
            orientation_word = "West"

        self.add_message('You head '+orientation_word)

    def player_orient(self, orientation):
        if orientation == Direction.NORTH:
            orientation_word = "North"
        if orientation == Direction.SOUTH:
            orientation_word = "South"
        if orientation == Direction.EAST:
            orientation_word = "East"
        if orientation == Direction.WEST:
            orientation_word = "West"

        self.add_message('You face to the  '+orientation_word)

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
                500 + index * (self.font_size+3),
                self.settings.ui_width,
                self.settings.screen_height)

            self.surface.blit(message, rect)
