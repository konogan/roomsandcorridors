# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pygame

from Settings import Settings
from Game_Stats import GameStats
from World import World
from MainMenu import MainMenu
import Events_Listener  as el

pygame.init()

class Game:
    def __init__(self):
        self.settings = Settings()
        screen_size = (self.settings.screen_width, self.settings.screen_height)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("rooms & corridors")
        
        #render surfaces
        self.menu_surface = pygame.Surface(screen_size)
        self.world_surface = pygame.Surface(screen_size)

        #game stats
        self.stats = GameStats(self.settings)
        
        self.world = None
        self.main_menu = MainMenu(self.menu_surface)
        
        
    def new(self):
        print("Generate a new world")
        self.world = World(self.settings, self.world_surface)
    
    def load(self):
        print('load')
    
    def save(self):
        print("save")
    
    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Watch for keyboard and mouse
            el.check_events(self)

            if self.stats.game_active:
                #world.update()
                self.world.render()

                self.screen.blit(self.world_surface, (0, 0))
                #infos.fill((55,155,255))
            else :
                self.screen.blit(self.main_menu.render(), (0, 0))

            #flip display
            pygame.display.flip()
            # limit speed
            clock.tick(30)
