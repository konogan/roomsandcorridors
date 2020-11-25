# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import World_Functions  as wf


class World():

    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.grid_size = (
            int(self.settings.screen_width / self.settings.tile_size), 
            int(self.settings.screen_height / self.settings.tile_size)
        )
        self.grid = None
        self.rooms = []
        self.init()

    def init(self):
        self.grid = None
        self.rooms = []

        #inititialize the one level grid
        self.grid = wf.make_grid(self.grid_size)

        #initialize the rooms
        wf.randomize_rooms(self)
        
        #place walls
        wf.build_walls(self)
        
        #place doors
        wf.place_door(self)
        
        #place items
        
        #place ennemies
        
        #init hero

    def update(self):
        #update world content
        pass

    def render(self):
        # render the world
        
        # iterate over each cell and render it
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                self.grid[i][j].render(self.screen,self.settings.tile_size)
                
        # iterate over each room and render it
        for i, _ in enumerate(self.rooms):
            self.rooms[i].render(self.screen,self.settings.tile_size)
