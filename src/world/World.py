# encoding: utf-8

import pygame

from src.Backup import Backup
from src.Constants import Coord, Direction
from src.actors.Player import Player
from src.generators.Bsd import Bsd
from src.items.Item import PickableItem
from src.world.helper_grid import *


class World:

    def __init__(self, settings, messages, game_surface, inventory_surface, camera):
        self.game_surface = game_surface
        self.game_surface_rect = game_surface.get_rect()
        self.inventory_surface = inventory_surface

        self.messages = messages
        self.settings = settings
        self.grid_size = (self.settings.grid_width, self.settings.grid_height)
        self.grid = None
        self.rooms = []
        self.player = None
        self.camera = camera

        self.debug = False
        self.mouse = Coord(0, 0)

    def new(self):
        # initialize the one level grid and associated rooms
        generator = Bsd(self.grid_size, 12)
        generator.run()

        # update the grid with the generator grid version
        self.grid = generator.get_grid()
        self.rooms = generator.get_rooms()

        self.grid = grid_generate_walls(self.grid, self.grid_size)
        self.grid = grid_generate_doors(self.grid, self.grid_size)
        self.grid = grid_random_place_items(self.grid, self.grid_size)

        # init player
        spawn = self.rooms[0].get_center()
        self.player = Player(spawn[0], spawn[1], self.rooms[0].room_id)
        # self.camera.look_at(self.player.coord.x, self.player.coord.x)

    def load(self):
        backup = Backup()
        backup.load(self.grid_size)
        self.grid = backup.get_grid()
        self.rooms = backup.get_rooms()
        self.player = backup.get_player()

    def player_open_door(self):
        # test 4 directions for a door and reverse his state
        for potential_door_coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            candidate = self.grid[self.player.coord.x + potential_door_coord[0]
                                  ][self.player.coord.y + potential_door_coord[1]]
            if candidate and candidate.type == "DOOR":
                if candidate.is_door_close:
                    candidate.open()
                    self.messages.add_message('You open the door')

    def player_close_door(self):
        # test 4 directions for a door and reverse his state
        for potential_door_coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            candidate = self.grid[self.player.coord.x + potential_door_coord[0]
                                  ][self.player.coord.y + potential_door_coord[1]]
            if candidate and candidate.type == "DOOR":
                if candidate.is_door_open:
                    candidate.close()
                    self.messages.add_message('You close the door')

    def player_pick_item(self):
        # pick all items on player location
        for found_item in self.grid[self.player.coord.x][self.player.coord.y].items:
            self.messages.add_message('You pick a ' + str(found_item))
            if isinstance(found_item, PickableItem):
                self.grid[self.player.coord.x][self.player.coord.y].items.remove(
                    found_item)
            self.player.inventory.add(found_item)

    def cell_in_front(self, coord_x, coord_y, orientation: Direction):
        """
        Args:
            coord_x:
            coord_y:
            orientation:
        """
        if self.grid[coord_x + orientation.value[0]][coord_y + orientation.value[1]]:
            return self.grid[coord_x + orientation.value[0]][coord_y + orientation.value[1]]

    def move_player_intent(self, new_orientation: Direction):
        """
        Args:
            new_orientation:
        """
        current_orientation = self.player.orientation
        self.player.orient(new_orientation)

        if current_orientation != new_orientation:
            # player turn on itself
            self.messages.player_orient(new_orientation)

        # player stay on same orientation
        target_cell = self.cell_in_front(
            self.player.coord.x, self.player.coord.y, self.player.orientation)

        if target_cell and target_cell.is_walkable():
            current_room = self.player.current_room
            # perform the move
            self.messages.player_move(new_orientation)
            self.player.move(target_cell.coord, target_cell.belongs_to)

            # check the player position against the camera viewport
            # move the center look if necessary
            # self.camera.look_at(self.player.coord.x,self.player.coord.y)

            if self.player.current_room != current_room:
                if self.player.current_room == 0:
                    self.messages.add_message('You enter a corridor')
                else:
                    self.messages.add_message('You enter a room')

            next_target_cell = self.cell_in_front(
                self.player.coord.x, self.player.coord.y, self.player.orientation)

            if next_target_cell.is_door_open():
                self.messages.add_message('You face a open door')

            if next_target_cell.is_door_close():
                self.messages.add_message('You face a close door')

            if next_target_cell.is_wall():
                self.messages.add_message('You face a Wall')

            # interact with the content of the cell
            if self.grid[self.player.coord.x][self.player.coord.y].items:
                for item in self.grid[self.player.coord.x][self.player.coord.y].items:
                    if item == 'CHEST':
                        self.messages.add_message(
                            'You find a Chest, (o)pen it up')
                    else:
                        self.messages.add_message(
                            'You find a ' + str(item) + ', (p)ick it up')

    def mouse_clicked(self):
        # inspect world at mouse coordinate
        print(self.grid[self.mouse.x][self.mouse.y])
        print(self.grid[self.mouse.x][self.mouse.y].items)

    def update(self):
        # update world content
        pass

    def update_fov(self, current_turn: int):
        # update field of view of the player
        """
        Args:
            current_turn:
        """
        # update_fov(self, current_turn, self.player.view_distance)

    def render(self):
        # render all the world on its own surface
        # TODO clip this surface related to game surface display
        world_size = (self.grid_size[0] * self.settings.tile_size,
                      self.grid_size[1] * self.settings.tile_size)
        local_surface = pygame.Surface(world_size)

        # render each tiles
        for coord_x in range(self.grid_size[0]):
            for coord_y in range(self.grid_size[1]):
                cell_coord = (coord_x * self.settings.tile_size,
                              coord_y * self.settings.tile_size)
                cell_rect = pygame.Rect(cell_coord, (self.settings.tile_size, self.settings.tile_size))
                cell_surface = self.grid[coord_x][coord_y].render(self.settings.tile_size, self.debug)
                local_surface.blit(cell_surface, cell_rect)

        # render each rooms
        if self.debug:
            for i, _ in enumerate(self.rooms):
                self.rooms[i].render(local_surface, self.settings.tile_size)

        # render the player
        self.player.render(local_surface, self.settings.tile_size)

        # blit this surface on the game surface
        self.game_surface.blit(local_surface, (0, 0))
