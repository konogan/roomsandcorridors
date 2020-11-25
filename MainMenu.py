# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from Button import Button

class MainMenu :
    def __init__(self,menu_surface):
        self.surface = menu_surface
        self.surface.fill((55,155,255))
        self.buttons = []
        self.__init_buttons()
        
    def __init_buttons(self):    
        play_button = Button("play", self.surface, "(P)lay current world",-200)
        self.buttons.append(play_button)

        new_button = Button("new", self.surface, "(N)ew world",-140)
        self.buttons.append(new_button)
    
        quit_button = Button("quit", self.surface, "(Q)uit",-80)
        self.buttons.append(quit_button)
    
    def render(self):
        self.surface.fill((55,155,255))
        
        for button in self.buttons:
            button.render()
        
        return self.surface