# encoding: utf-8

import os.path

import pygame

from src.Backup import Backup
from src.Constants import States
from src.Settings import Settings
from src.ui import Events_listeners
from src.ui.Camera import Camera
from src.ui.MainMenu import MainMenu
from src.ui.Messages import Messages
from src.world.World import World

pygame.init()


class Game:
    def __init__(self):
        self.settings = Settings()
        self.state = States.LOAD

        # geometries
        screen_size = (self.settings.screen_width,
                       self.settings.screen_height)

        world_size = (self.settings.screen_width - self.settings.ui_width,
                      self.settings.screen_height)

        ui_size = (self.settings.ui_width,
                   self.settings.screen_height)

        self.screen = pygame.display.set_mode(screen_size)

        self.center = (int((self.settings.screen_width - self.settings.ui_width) //
                           2), int(self.settings.screen_height // 2))

        pygame.display.set_caption("rooms & corridors")
        game_icon = pygame.image.load('src/assets/logo.png')
        pygame.display.set_icon(game_icon)

        self.save_exist = os.path.isfile('world.save')

        # camera
        self.camera = Camera(self)

        # render surfaces
        self.menu_surface = pygame.Surface(screen_size)  # loading screen
        self.world_surface = pygame.Surface(world_size)  # game screen
        self.inventory_surface = pygame.Surface(
            world_size)  # game screen inventory
        self.ui_surface = pygame.Surface(ui_size)  # ui bar

        # in game messages
        self.messages = Messages(self.settings, self.ui_surface)

        # init
        self.world = World(self.settings,
                           self.messages,
                           self.world_surface,
                           self.inventory_surface,
                           self.camera)

        self.main_menu = MainMenu(self.menu_surface,
                                  self.save_exist)

        self.turns = 0
        self.new()

    def new_turn(self):
        self.turns += 1

    def switch_inventory(self):
        if self.state == States.INVENTORY:
            self.state = States.PLAY
        else:

            self.state = States.INVENTORY

    def switch_debug(self):
        if self.world.debug:
            self.world.debug = False
        else:
            self.world.debug = True

    def new(self):
        print("Generate a new world")
        self.world.new()
        self.save()

    def load(self):
        print('Loading world')

    def save(self):
        print('Saving generated world')
        backup = Backup()
        backup.save(self.world)
        self.state = States.PLAY

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Watch for keyboard and mouse
            Events_listeners.check_events(self)

            if self.state == States.PLAY:
                self.world.update()

                self.world.update_fov(self.turns)

                # render
                self.world.render_grid()
                self.messages.render()

                # display
                self.screen.blit(self.world_surface, (0, 0))
                self.screen.blit(self.ui_surface, (self.settings.screen_width -
                                                   self.settings.ui_width, 0))

            if self.state == States.INVENTORY:
                # update the inventory surface
                self.world.player.inventory.render(
                    self.world.inventory_surface)
                # blit it
                self.screen.blit(self.world.inventory_surface, (0, 0))

            if self.state == States.MENU:
                self.screen.blit(self.main_menu.render(), (0, 0))

            # flip display
            pygame.display.flip()

            # limit speed
            clock.tick(30)
