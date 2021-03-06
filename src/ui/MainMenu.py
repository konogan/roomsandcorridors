# encoding: utf-8
from src.Constants import MyColors
from src.ui.Button import Button


class MainMenu:
    def __init__(self, menu_surface, save_exist=False):
        """
        Args:
            menu_surface:
            save_exist:
        """
        self.buttons = []
        self.surface = menu_surface
        self.init_buttons(save_exist)

    def init_buttons(self, save_exist=False):
        """
        Args:
            save_exist:
        """
        if save_exist:
            play_button = Button("load", self.surface, "(l)oad world", -200)
            self.buttons.append(play_button)

        new_button = Button("new", self.surface, "(n)ew world", -140)
        self.buttons.append(new_button)

        quit_button = Button("quit", self.surface, "(q)uit", -80)
        self.buttons.append(quit_button)

    def render(self):
        self.surface.fill(MyColors.BACKGROUND.value)

        for button in self.buttons:
            button.render()

        return self.surface
