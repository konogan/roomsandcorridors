# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import World_Functions as wf
from Constants import Coord,Direction
from Room import Room
from Player import Player


class World():

    def __init__(self, settings, messages, surface, camera):
        self.surface = surface
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

        # inititialize the one level grid
        self.grid = wf.make_grid(self.grid_size)

        # initialize the rooms
        wf.randomize_rooms(self)

        # place walls
        wf.build_walls(self)

        # place doors
        wf.place_door(self)

        # place items

        # place ennemies

        # init player
        spawn = self.rooms[0].get_center()
        self.player = Player(spawn[0], spawn[1], self.rooms[0].room_id)
        self.camera.look_at(self.player.coord.x, self.player.coord.x)

    def to_json(self):
        export = {}
        export["rooms"] = []
        for room in self.rooms:
            export["rooms"].append(room.to_json())
        export["grid"] = []
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j].type:
                    export["grid"].append(self.grid[i][j].to_json())
        return export

    def from_json(self, worldjson):
        # populate the rooms
        self.rooms = []
        for r in worldjson['rooms']:
            self.rooms.append(Room(r['x'], r['y'], r['w'], r['h'], r['i']))

        # populate the grid
        self.grid = wf.make_grid(self.grid_size)
        for g in worldjson['grid']:
            self.grid[g['x']][g['y']].from_json(g)

        # for the moment the player respawn in the first room
        # TODO : get player from savefile
        spawn = self.rooms[0].get_center()
        self.player = Player(spawn[0], spawn[1], self.rooms[0].room_id)
        self.camera.look_at(self.player.coord.x, self.player.coord.y)

        # random place items
        wf.place_items(self)

    def save(self):
        # TODO rework on saveformat
        pass

    def load(self):
        # TODO from the new saveformat load
        pass

    def player_open_door(self):
        # test 4 directions for a door and reverse his state
        for potential_door_coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            candidate = self.grid[self.player.coord.x + potential_door_coord[0]
                                  ][self.player.coord.y+potential_door_coord[1]]
            if candidate and candidate.type == "DOOR":
                if candidate.is_door_close:
                    candidate.open()
                    self.messages.add_message('You open the door')

    def player_close_door(self):
        # test 4 directions for a door and reverse his state
        for potential_door_coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            candidate = self.grid[self.player.coord.x + potential_door_coord[0]
                                  ][self.player.coord.y+potential_door_coord[1]]
            if candidate and candidate.type == "DOOR":
                if candidate.is_door_open:
                    candidate.close()
                    self.messages.add_message('You close the door')

    def cell_in_front(self, coord_x, coord_y, orientation):
        if self.grid[coord_x + orientation.value[0]][coord_y+orientation.value[1]]:
            return self.grid[coord_x + orientation.value[0]][coord_y+orientation.value[1]]

    def move_player_intent(self, new_orientation):

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

            # check the player postion against the camera viewport
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

    def set_mouse(self, mouse_x, mouse_y):
        self.mouse = Coord(int(mouse_x//self.settings.tile_size + self.camera.top_left_x),
                           int(mouse_y//self.settings.tile_size+self.camera.top_left_y))

    def mouse_clicked(self):
        # inspect world at mouse coordinate
        print(self.grid[self.mouse.x][self.mouse.y])
        print(self.grid[self.mouse.x][self.mouse.y].items)

    def update(self):
        # update world content
        pass

    def update_fov(self, current_turn):
        # update field of view of the player
        wf.update_fov(self, current_turn, self.player.view_distance)

    def render(self):
        self.surface.fill((0, 0, 0))
        offset = (self.camera.top_left_x, self.camera.top_left_y)
        # iterate over all the cells covered by the camera
        # and offest them
        for coord_x in range(self.camera.top_left_x, self.camera.bottom_right_x+1):
            for coord_y in range(self.camera.top_left_y, self.camera.bottom_right_y+1):
                if self.grid[coord_x][coord_y]:
                    self.grid[coord_x][coord_y].render(
                        self.surface, self.settings.tile_size, offset, self.debug, self.mouse.x == coord_x and self.mouse.y == coord_y)

        # iterate over each room and render it
        if self.debug:
            for i, _ in enumerate(self.rooms):
                self.rooms[i].render(
                    self.surface, self.settings.tile_size, offset)

        # render the player
        self.player.render(self.surface, self.settings.tile_size, offset)
