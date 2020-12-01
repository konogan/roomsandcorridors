# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import json
import os.path
import pygame

from Messages import Messages
import Events_listeners

from Settings import Settings
from Constants import States
from Camera import Camera
from World import World
from MainMenu import MainMenu

pygame.init()


class Game:
    def __init__(self):
        self.settings = Settings()
        self.state = States.LOAD
        screen_size = (self.settings.screen_width, self.settings.screen_height)
        world_size = (self.settings.screen_width -
                      self.settings.ui_width, self.settings.screen_height)
        ui_size = (self.settings.ui_width, self.settings.screen_height)
        self.screen = pygame.display.set_mode(screen_size)

        self.center = (int((self.settings.screen_width-self.settings.ui_width) //
                           2), int(self.settings.screen_height // 2))

        pygame.display.set_caption("rooms & corridors")
        game_icon = pygame.image.load('assets/logo.png')
        pygame.display.set_icon(game_icon)

        # camera
        self.camera = Camera(self)

        # render surfaces
        self.menu_surface = pygame.Surface(screen_size)     # loading screen
        self.world_surface = pygame.Surface(world_size)     # gamescreen
        self.ui_surface = pygame.Surface(ui_size)           # ui bar

        # game stats
        self.stats = Messages(self.settings, self.ui_surface)

        self.save_exist = os.path.isfile('world.save')
        self.state = States.INIT
        # init
        self.world = World(self.settings, self.stats,
                           self.world_surface, self.camera)
        self.main_menu = MainMenu(self.menu_surface, self.save_exist)
        self.turns = 0
        self.need_redraw = True
        self.state = States.MENU

    def new_turn(self):
        self.need_redraw = True
        self.turns += 1

    def switch_debug(self):
        self.need_redraw = True
        if self.world.debug:
            self.world.debug = False
        else:
            self.world.debug = True

    def new(self):
        print("Generate a new world")
        self.world.new()
        self.save()
        self.need_redraw = True

    def load(self):
        with open('world.save') as json_file:
            worldjson = json.load(json_file)
            self.world.from_json(worldjson)
        

    def save(self):
        worldjson = self.world.to_json()
        with open('world.save', 'w') as outfile:
            json.dump(worldjson, outfile)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Watch for keyboard and mouse
            Events_listeners.check_events(self)

            if self.state == States.PLAY:

                self.world.update()

                if self.need_redraw:

                    self.world.update_fov(self.turns)

                    # render
                    self.world.render()
                    self.stats.render()

                    # display
                    self.screen.blit(self.world_surface, (0, 0))
                    self.screen.blit(self.ui_surface, (self.settings.screen_width -
                                                       self.settings.ui_width, 0))
                    self.need_redraw = False

            if self.state == States.ITEM:
                print("Inventory management")

            if self.state == States.MENU:
                self.screen.blit(self.main_menu.render(), (0, 0))
                self.need_redraw = True

            # flip display
            pygame.display.flip()
            # limit speed
            clock.tick(30)
