# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from Button import Button
from Constants import My_colors

class MainMenu:
    def __init__(self, menu_surface, save_exist=False):
        self.surface = menu_surface
        self.init_buttons(save_exist)

    def init_buttons(self, save_exist=False):
        self.buttons = []
        if save_exist:
            play_button = Button("load", self.surface, "re(l)oad world", -200)
            self.buttons.append(play_button)

        new_button = Button("new", self.surface, "(n)ew world", -140)
        self.buttons.append(new_button)

        quit_button = Button("quit", self.surface, "(q)uit", -80)
        self.buttons.append(quit_button)

    def render(self):
        self.surface.fill(My_colors.BACKGROUND.value)

        for button in self.buttons:
            button.render()

        return self.surface
