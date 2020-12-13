# encoding: utf-8

import pygame

from src.Backup import Backup
from src.Constants import Coord
from src.Constants import States
from src.Settings import Settings
from src.ui import Events_listeners
from src.ui.MainMenu import MainMenu
from src.ui.Messages import Messages
from src.world.World import World

pygame.init()


class Game:

    def __init__(self):
        self.settings = Settings()
        self.current_state = States.LOAD

        pygame.display.set_caption(self.settings.name)
        game_icon = pygame.image.load('src/assets/logo.png')
        pygame.display.set_icon(game_icon)

        self.screen = pygame.display.set_mode(self.settings.screen_size)
        self.center = self.settings.world_size_center

        # render surfaces
        self.menu_surface = pygame.Surface(self.settings.screen_size)  # loading screen
        self.game_surface = pygame.Surface(self.settings.world_size)  # game screen
        self.inventory_surface = pygame.Surface(self.settings.world_size)  # game screen inventory
        self.ui_surface = pygame.Surface(self.settings.ui_size)  # ui bar

        # in game messages
        self.messages = Messages(self.settings, self.ui_surface)

        # gameobjects
        self.world = None
        self.mouse = Coord(0, 0)

        # begin
        backup = Backup()
        self.main_menu = MainMenu(self.menu_surface, backup.is_available())
        self.current_state = States.MENU
        self.turns = 0

    def set_mouse(self, mouse_x: int, mouse_y: int):
        self.mouse = Coord(mouse_x, mouse_y)

    def new_turn(self):
        self.turns += 1

    def switch_inventory(self):
        if self.current_state == States.INVENTORY:
            self.current_state = States.PLAY
        else:

            self.current_state = States.INVENTORY

    def switch_debug(self):
        if self.world.debug:
            self.world.debug = False
        else:
            self.world.debug = True

    def new(self):
        self.current_state = States.LOAD
        print("Generate a new world")
        self.world = World(self.settings, self.messages, self.game_surface, self.inventory_surface, None)
        self.world.new()
        self.current_state = States.PLAY

    def load(self):
        self.current_state = States.LOAD
        print('Loading world fro save')
        self.world = World(self.settings, self.messages, self.game_surface, self.inventory_surface, None)
        self.world.load()
        self.current_state = States.PLAY

    def save(self):
        self.current_state = States.LOAD
        print('Saving world')
        backup = Backup()
        backup.save(self.world)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # Watch for keyboard and mouse
            Events_listeners.check_events(self)

            if self.current_state == States.PLAY:
                # self.world.update()

                # self.world.update_fov(self.turns)

                # render
                self.world.render()
                self.messages.render()

                # display
                self.screen.blit(self.game_surface, (0, 0))
                self.screen.blit(self.ui_surface, (self.settings.screen_width -
                                                   self.settings.ui_width, 0))

            if self.current_state == States.INVENTORY:
                # update the inventory surface
                self.world.player.inventory.render(
                    self.world.inventory_surface)
                # blit it
                self.screen.blit(self.world.inventory_surface, (0, 0))

            if self.current_state == States.MENU:
                self.screen.blit(self.main_menu.render(), (0, 0))

            # flip display
            pygame.display.flip()

            # limit speed
            clock.tick(30)
