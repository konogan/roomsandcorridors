# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import World_Functions as wf
from Room import Room
from Player import Player


class World():

    def __init__(self, settings, stats, surface, camera):
        self.surface = surface
        self.stats = stats
        self.settings = settings
        self.surface_rect = surface.get_rect()
        self.grid_size = (self.settings.grid_width, self.settings.grid_height)
        self.grid = None
        self.rooms = []
        self.player = None
        self.camera = camera
        self.debug = False
        self.mouse_x = None
        self.mouse_y = None

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
        spawn = self.rooms[0].get_center()
        self.player = Player(spawn[0], spawn[1], self.rooms[0].room_id)
        self.camera.look_at(self.player.coord.x, self.player.coord.y)

    def move_player_intent(self, direction):
        target_cell = self.grid[self.player.coord.x +
                                direction[0]][self.player.coord.y+direction[1]]

        if target_cell.is_walkable():
            if self.player.current_room != target_cell.belongs_to:
                if target_cell.belongs_to == 0:
                    self.stats.add_message('You enter a corridor')
                else:
                    self.stats.add_message('You enter a room')
            self.stats.player_move(direction)
            self.player.move(direction, target_cell.belongs_to)

            # check the player postion against the camera viewport
            # move the center look if necessary
            self.camera.look_at(self.player.coord.x, self.player.coord.y)

        else:
            self.stats.player_move(None)

    def set_mouse_click(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        print(mouse_x, mouse_y)

    def update(self):
        # update world content
        pass

    def update_fov(self, current_turn):
        # update field of view of the player
        wf.update_fov(self, current_turn)

    def render(self):
        self.surface.fill((0, 0, 0))
        offset = (self.camera.top_left_x, self.camera.top_left_y)
        # iterate over all the cells covered by the camera
        # and offest them
        for coord_x in range(self.camera.top_left_x, self.camera.bottom_right_x+1):
            for coord_y in range(self.camera.top_left_y, self.camera.bottom_right_y+1):
                if self.grid[coord_x][coord_y]:
                    self.grid[coord_x][coord_y].render(
                        self.surface, self.settings.tile_size, offset, self.debug)

        # iterate over each room and render it
        if self.debug:
            for i, _ in enumerate(self.rooms):
                self.rooms[i].render(
                    self.surface, self.settings.tile_size, offset)

        # render the player
        self.player.render(self.surface, self.settings.tile_size, offset)
