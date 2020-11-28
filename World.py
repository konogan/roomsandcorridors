# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import World_Functions as wf
from Room import Room
from Player import Player


class World():

    def __init__(self, settings, stats, screen):
        self.screen = screen
        self.stats = stats
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.grid_size = ( self.settings.grid_width , self.settings.grid_height)
        self.grid = None
        self.rooms = []
        self.player = None

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

    def toJson(self):
        export = {}
        export["rooms"] = []
        for room in self.rooms:
            export["rooms"].append(room.toJson())
        export["grid"] = []
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                export["grid"].append(self.grid[i][j].toJson())
        return export

    def fromJson(self, worldjson):
        # populate the rooms
        self.rooms = []
        for r in worldjson['rooms']:
            self.rooms.append(Room(r['x'], r['y'], r['w'], r['h'], r['i']))
        # populate the grid
        self.grid = wf.make_grid(self.grid_size)
        for g in worldjson['grid']:
            self.grid[g['x']][g['y']].fromJson(g)

        # for the moment the player respawn in the first room
        spawn = self.rooms[0].get_center()
        self.player = Player(spawn[0], spawn[1], self.rooms[0].room_id)

    def move_player_intent(self, direction):
        target_cell = self.grid[self.player.coord.x +
                                direction[0]][self.player.coord.y+direction[1]]
        
        if self.player.current_room != target_cell.belongs_to:
            if target_cell.belongs_to == 0:
                self.stats.add_message('You enter a corridor')
            else:
                self.stats.add_message('You enter a room')

        if target_cell.is_walkable():
            self.stats.player_move(direction)
            self.player.move(direction, target_cell.belongs_to)
        else:
            self.stats.player_move(None)

    def update(self):
        # update world content
        pass

    def render(self):
        # iterate over each cell and render it
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.grid[i][j].render(self.screen, self.settings.tile_size)

        # iterate over each room and render it
        # for i, _ in enumerate(self.rooms):
        #     self.rooms[i].render(self.screen, self.settings.tile_size)

        # render the player
        self.player.render(self.screen, self.settings.tile_size)
