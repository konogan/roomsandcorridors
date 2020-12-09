# encoding: utf-8

from src.Constants import Coord, Direction
from src.actors.Player import Player
from src.items.Item import PickableItem
from src.world.Utils import *

class World:

    def __init__(self, settings, messages, surface, inventory_surface, camera):
        """
        Args:
            settings:
            messages:
            surface:
            inventory_surface:
            camera:
        """
        self.surface = surface
        self.inventory_surface = inventory_surface
        self.messages = messages
        self.settings = settings
        self.surface_rect = surface.get_rect()
        self.grid_size = (self.settings.grid_width, self.settings.grid_height)
        self.grid = None
        self.rooms = []
        self.player = None
        self.camera = camera
        self.debug = False
        self.mouse = Coord(0, 0)
        self.new()

    def new(self):
        # empty elements
        self.grid = None
        self.rooms = []

        # initialize the one level grid
        self.grid = make_grid(self.grid_size)

        # initialize the rooms
        randomize_rooms(self)

        # place walls
        build_walls(self)

        # place doors
        place_door(self)

        # place items
        place_items(self)

        # place enemies

        # init player
        spawn = self.rooms[0].get_center()
        self.player = Player(spawn[0], spawn[1], self.rooms[0].room_id)
        self.camera.look_at(self.player.coord.x, self.player.coord.x)

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
            self.camera.look_at(self.player.coord.x,
                                self.player.coord.y)

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

    def set_mouse(self, mouse_x: int, mouse_y: int):
        """
        Args:
            mouse_x:
            mouse_y:
        """
        self.mouse = Coord(int(mouse_x // self.settings.tile_size + self.camera.top_left_x),
                           int(mouse_y // self.settings.tile_size + self.camera.top_left_y))

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
        update_fov(self, current_turn, self.player.view_distance)

    def render_grid(self):
        self.surface.fill((0, 0, 0))
        offset = (self.camera.top_left_x, self.camera.top_left_y)
        # iterate over all the cells covered by the camera
        # and offset them
        for coord_x in range(self.camera.top_left_x, self.camera.bottom_right_x + 1):
            for coord_y in range(self.camera.top_left_y, self.camera.bottom_right_y + 1):
                if self.grid[coord_x][coord_y]:
                    self.grid[coord_x][coord_y].render(
                        self.surface, self.settings.tile_size, offset, self.debug,
                        self.mouse.x == coord_x and self.mouse.y == coord_y)

        # iterate over each room and render it
        if self.debug:
            for i, _ in enumerate(self.rooms):
                self.rooms[i].render(
                    self.surface, self.settings.tile_size, offset)

        # render the player
        self.player.render(self.surface, self.settings.tile_size, offset)
