# encoding: utf-8
import math
import random

from src.Constants import Coord
from src.actors.Player import Player
from src.generators.Bsd import Bsd
from src.items.Item import *
from src.world.Cell import Cell


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

    def to_json(self):
        export = {"rooms": []}
        for room in self.rooms:
            export["rooms"].append(room.to_json())
        export["grid"] = []
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j].type:
                    export["grid"].append(self.grid[i][j].to_json())
        return export

    def from_json(self, world_json):
        # populate the rooms
        """
        Args:
            world_json:
        """
        # self.rooms = []
        # for r in world_json['rooms']:
        #     self.rooms.append(Room(r['x'], r['y'], r['w'], r['h'], r['i']))
        #
        # # populate the grid
        # self.grid = make_grid(self.grid_size)
        # for g in world_json['grid']:
        #     self.grid[g['x']][g['y']].from_json(g)
        #
        # # for the moment the player respawn in the first room
        # # TODO : get player from save file
        # spawn = self.rooms[0].get_center()
        # self.player = Player(spawn[0], spawn[1], self.rooms[0].room_id)
        # self.camera.look_at(self.player.coord.x, self.player.coord.y)
        #
        # # random place items
        # place_items(self)

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

    def cell_in_front(self, coord_x, coord_y, orientation):
        """
        Args:
            coord_x:
            coord_y:
            orientation:
        """
        if self.grid[coord_x + orientation.value[0]][coord_y + orientation.value[1]]:
            return self.grid[coord_x + orientation.value[0]][coord_y + orientation.value[1]]

    def move_player_intent(self, new_orientation):

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
                        self.messages.add_message('You find a Chest, (o)pen it up')
                    else:
                        self.messages.add_message('You find a ' + str(item) + ', (p)ick it up')

    def set_mouse(self, mouse_x, mouse_y):
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

    def update_fov(self, current_turn):
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


def make_grid(grid_size):
    """
    Args:
        grid_size:
    """
    cols = grid_size[0]
    rows = grid_size[1]
    grid = []
    for i in range(cols + 1):
        grid.append([])
        for j in range(rows + 1):
            grid[i].append(Cell(i, j))
    return grid


def randomize_rooms(world):
    """
    Args:
        world:
    """
    Bsd(world, 12)


def build_walls(world):
    # iterate over all FREE cells
    """
    Args:
        world:
    """
    for i in range(world.grid_size[0]):
        for j in range(world.grid_size[1]):
            if world.grid[i][j].is_free:
                need_a_wall = False
                if not world.grid[i - 1][j].is_free:
                    need_a_wall = True
                if not world.grid[i + 1][j].is_free:
                    need_a_wall = True
                if not world.grid[i][j - 1].is_free:
                    need_a_wall = True
                if not world.grid[i][j + 1].is_free:
                    need_a_wall = True
                if not world.grid[i - 1][j + 1].is_free:
                    need_a_wall = True
                if not world.grid[i - 1][j - 1].is_free:
                    need_a_wall = True
                if not world.grid[i + 1][j - 1].is_free:
                    need_a_wall = True
                if not world.grid[i + 1][j + 1].is_free:
                    need_a_wall = True

                if need_a_wall:
                    world.grid[i][j].set_wall()


def place_door(world):
    """
    Args:
        world:
    """
    for i in range(world.grid_size[0]):
        for j in range(world.grid_size[1]):
            if world.grid[i][j].type == "CORRIDOR_FLOOR":
                corridor = 0
                room = 0
                # 2 walls around
                if (world.grid[i - 1][j].type == "WALL" and world.grid[i + 1][j].type == "WALL") or (
                        world.grid[i][j - 1].type == "WALL" and world.grid[i + 1][j + 1].type == "WALL"):
                    # count corridors
                    if world.grid[i - 1][j].type == "CORRIDOR_FLOOR":
                        corridor += 1
                    if world.grid[i + 1][j].type == "CORRIDOR_FLOOR":
                        corridor += 1
                    if world.grid[i][j - 1].type == "CORRIDOR_FLOOR":
                        corridor += 1
                    if world.grid[i][j + 1].type == "CORRIDOR_FLOOR":
                        corridor += 1

                    # count room
                    if world.grid[i - 1][j].type == "ROOM_FLOOR":
                        room += 1
                    if world.grid[i + 1][j].type == "ROOM_FLOOR":
                        room += 1
                    if world.grid[i][j - 1].type == "ROOM_FLOOR":
                        room += 1
                    if world.grid[i][j + 1].type == "ROOM_FLOOR":
                        room += 1

                    if corridor == 1 and room == 1 and random.random() < 0.60:
                        world.grid[i][j].set_door(
                            random.choice(['OPEN', 'CLOSE']))


# def random_item():
#     # generate a random item
#     if random.random() < 0.90:
#         ret = Torch()
#     else:
#         ret = Chest()
#         for _ in range(random.randint(0, 4)):
#             if random.random() < 0.50:
#                 ret.add_item(Torch())
#     return ret


def place_items(world):
    # place randomly items in the world
    """
    Args:
        world:
    """
    for i in range(world.grid_size[0]):
        for j in range(world.grid_size[1]):
            if world.grid[i][j].type == "ROOM_FLOOR":
                if random.random() < 0.05:
                    new_item = Torch()
                    world.grid[i][j].items.append(new_item)


def update_fov(world, current_turn, max_distance=10):
    # init display of all cells
    # Initially set all tiles to not visible.
    """
    Args:
        world:
        current_turn:
        max_distance:
    """
    for i in range(world.grid_size[0]):
        for j in range(world.grid_size[1]):
            world.grid[i][j].set_visibility(False, current_turn)

    # field of view around the player
    for i in range(0, 360):
        x = math.cos(i * 0.01745)
        y = math.sin(i * 0.01745)

        do_fov(world, current_turn, x, y, max_distance)


def do_fov(world, current_turn, x, y, max_distance):
    """
    Args:
        world:
        current_turn:
        x:
        y:
        max_distance:
    """
    origin_x = float(world.player.coord.x) + .5
    origin_y = float(world.player.coord.y) + .5
    for distance in range(max_distance):
        if world.grid[int(origin_x)][int(origin_y)]:
            world.grid[int(origin_x)][int(origin_y)].set_visibility(
                True, current_turn, distance)
            if world.grid[int(origin_x)][int(origin_y)].block_fov():
                return
            origin_x += x
            origin_y += y
