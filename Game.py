# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import json
import os.path
import pygame

from Settings import Settings
from Game_Stats import GameStats
from World import World
from MainMenu import MainMenu
import Events_Listener as el

pygame.init()


class Game:
    def __init__(self):
        self.settings = Settings()
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

        # render surfaces
        self.menu_surface = pygame.Surface(screen_size)     # loading screen
        self.world_surface = pygame.Surface(world_size)     # gamescreen
        self.ui_surface = pygame.Surface(ui_size)           # ui bar

        # game stats
        self.stats = GameStats(self.settings, self.ui_surface)

        self.save_exist = os.path.isfile('world.save')

        # init
        self.world = World(self.settings, self.stats, self.world_surface)
        self.main_menu = MainMenu(self.menu_surface, self.save_exist)
        self.turns = 0
        self.need_redraw = True

    def new_turn(self):
        self.need_redraw = True
        self.turns +=1
    
    def new(self):
        print("Generate a new world")
        self.world.new()
        self.save()
        self.need_redraw = True
        self.stats.game_active = True

    def load(self):
        with open('world.save') as json_file:
            worldjson = json.load(json_file)
            self.world.fromJson(worldjson)

    def save(self):
        worldjson = self.world.toJson()
        with open('world.save', 'w') as outfile:
            json.dump(worldjson, outfile)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            # Watch for keyboard and mouse
            el.check_events(self)

            self.world.update()

            if self.stats.game_active:
                # world.update()

                if self.need_redraw:
                    # render
                    self.world.render()
                    self.stats.render()

                    # display
                    self.screen.blit(self.world_surface, (0, 0))
                    self.screen.blit(self.ui_surface, (self.settings.screen_width -
                                                    self.settings.ui_width, 0))
                    self.need_redraw = False
                    
            else:
                self.screen.blit(self.main_menu.render(), (0, 0))
                self.need_redraw = True

            # flip display
            pygame.display.flip()
            # limit speed
            clock.tick(30)
