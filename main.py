# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from Settings import Settings
from Game_Stats import GameStats
from World import World
from MainMenu import MainMenu


import Events_Listener  as el

import pygame
pygame.init()



def run_game():   
    settings = Settings()
    screen_size = (settings.screen_width, settings.screen_height)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("rooms & corridors")
    
    #render surfaces
    menu_surface = pygame.Surface(screen_size)
    world_surface = pygame.Surface(screen_size)
    
    #game stats
    stats = GameStats(settings)
    
    
    #initailize
    world = World(settings, world_surface)
    main_menu = MainMenu(menu_surface)
    
    
    # limit speed
    clock = pygame.time.Clock()
    
    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse
        el.check_events(settings, screen, stats,main_menu, world)

        if stats.game_active:
            #world.update()
            world.render()

            screen.blit(world_surface, (0, 0))
            #infos.fill((55,155,255))
        else :
            screen.blit(main_menu.render(), (0, 0))

        #flip display
        pygame.display.flip()
        # limit speed
        clock.tick(30)

if __name__ == "__main__":
    run_game()
