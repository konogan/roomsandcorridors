# encoding: utf-8

import pygame

from src.Constants import Direction, MyColors


class Messages:
    def __init__(self, settings, surface: pygame.Surface):
        """
        Args:
            settings:
            surface (pygame.Surface): targeted surface for rendering
        """
        self.settings = settings
        self.messages = []
        self.surface = surface
        self.font_size = 15
        self.font = pygame.font.Font("./src/assets/basis33.ttf", self.font_size)
        self.add_message("You arrive in a dark room")
        self.add_message("-------------------------")
        self.add_message("Move with the arrows")
        self.add_message("(o)pen door/chest")
        self.add_message("(c)lose door/chest")
        self.add_message("(p)ick item")
        self.add_message("-------------------------")

    def add_message(self, text: str):
        """
        Args:
            text (str): message to display
        """
        self.messages.append(text)

    def player_move(self, orientation: Direction):
        """
        Args:
            orientation (Direction):
        """
        orientation_word: str = ""
        if orientation == Direction.NORTH:
            orientation_word = "North"
        if orientation == Direction.SOUTH:
            orientation_word = "South"
        if orientation == Direction.EAST:
            orientation_word = "East"
        if orientation == Direction.WEST:
            orientation_word = "West"

        self.add_message('You head ' + orientation_word)

    def player_orient(self, orientation: Direction):
        """
        Args:
            orientation (Direction): cardinal orientation
        """
        orientation_word = ""
        if orientation == Direction.NORTH:
            orientation_word = "North"
        if orientation == Direction.SOUTH:
            orientation_word = "South"
        if orientation == Direction.EAST:
            orientation_word = "East"
        if orientation == Direction.WEST:
            orientation_word = "West"

        self.add_message('You face to the  ' + orientation_word)

    def render(self):
        # fill black
        self.surface.fill((0, 0, 0))

        # draw border
        pygame.draw.line(self.surface, MyColors.TEXT.value, (0, 1),
                         (0, self.settings.screen_height))

        # display last messages
        for index, msg in enumerate(self.messages[-10:]):
            message = self.font.render("{}".format(msg), True, MyColors.TEXT.value)
            rect = pygame.Rect(
                10,
                500 + index * (self.font_size + 3),
                self.settings.ui_width,
                self.settings.screen_height)

            self.surface.blit(message, rect)
