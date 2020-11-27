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
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("rooms & corridors")

        # render surfaces
        self.menu_surface = pygame.Surface(screen_size)
        self.world_surface = pygame.Surface(screen_size)
        
        # game stats
        self.stats = GameStats(self.settings)

        self.save_exist = os.path.isfile('world.save')

        # init
        self.world = World(self.settings, self.stats, self.world_surface)
        self.main_menu = MainMenu(self.menu_surface, self.save_exist)

    def new(self):
        print("Generate a new world")
        self.world.new()
        self.save()
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
                self.world.render()

                self.screen.blit(self.world_surface, (0, 0))
                # infos.fill((55,155,255))
            else:
                self.screen.blit(self.main_menu.render(), (0, 0))

            # flip display
            pygame.display.flip()
            # limit speed
            clock.tick(30)
