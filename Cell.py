# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


import pygame


from Constants import Coord, My_colors


class Cell():

    def __init__(self, coord_x, coord_y):
        self.coord = Coord(coord_x, coord_y)
        self.is_free = True
        self.belongs_to = 0
        self.type = None
        self.visibility = False
        self.was_discovered = False
        self.last_time_was_seen = 0
        self.distance = 0

    def belong_to_room(self, room_id):
        self.is_free = False
        self.belongs_to = room_id
        self.type = "ROOM"

    def set_corridor(self):
        self.is_free = False
        self.belongs_to = 0
        self.type = "CORRIDOR"

    def set_door(self):
        self.is_free = False
        self.type = "DOOR"

    def set_wall(self):
        self.type = "WALL"

    def is_walkable(self):
        return self.type != "WALL"

    def block_fov(self):
        return self.type == "WALL" or self.type == "DOOR"

    def set_visibility(self, visibility, current_turn, distance_from_player=0):
        self.visibility = visibility
        self.distance = distance_from_player
        if visibility:
            self.last_time_was_seen = current_turn
            self.was_discovered = True
        else:
            # number of turn of memory
            if current_turn - self.last_time_was_seen > 100:
                self.was_discovered = False

    def to_json(self):
        export = {}
        export['x'] = self.coord.x
        export['y'] = self.coord.y
        export['f'] = self.is_free
        export['b'] = self.belongs_to
        export['t'] = self.type
        export['v'] = self.visibility
        export['d'] = self.was_discovered
        export['s'] = self.last_time_was_seen
        return export

    def from_json(self, json_data):
        self.is_free = json_data['f']
        self.belongs_to = json_data['b']
        self.type = json_data['t']
        self.visibility = json_data['v']
        self.was_discovered = json_data['d']
        self.last_time_was_seen = json_data['s']

    def render(self, world_surface, tile_size, offset=(0, 0), debug=False):
        # only render if necessary
        if self.visibility or self.was_discovered:

            local_surface = pygame.Surface((tile_size, tile_size))
            local_rect = pygame.Rect(0, 0, tile_size, tile_size)

            world_rect = pygame.Rect(
                (self.coord.x-offset[0])*tile_size,
                (self.coord.y-offset[1])*tile_size,
                tile_size,
                tile_size
            )

            # define style based on type
            if self.type == "WALL":
                cell_color = My_colors.GREY
                cell_color_in_memory = My_colors.GREY
            elif self.type == "ROOM":
                cell_color = My_colors.WHITE
                cell_color_in_memory = My_colors.GREY
            elif self.type == "CORRIDOR":
                cell_color = My_colors.WHITE
                cell_color_in_memory = My_colors.GREY
            elif self.type == "DOOR":
                cell_color = My_colors.GREEN
                cell_color_in_memory = My_colors.GREY
            else:
                cell_color = My_colors.BLACK

            # drawing local cell
            if self.visibility:
                pygame.draw.rect(local_surface, cell_color.value, local_rect)
            else:
                if self.was_discovered:
                    pygame.draw.rect(
                        local_surface, cell_color_in_memory.value, local_rect)

            if debug and self.visibility:
                cell_font = pygame.font.SysFont('arial', 15)
                number = cell_font.render("{}".format(
                    self.distance), True, (0, 0, 255))

                local_surface.blit(number, local_rect)

            # alpha pass based on distance from player
            # just for test
            # need to be placed in a lighting pass
            # local_surface_light = pygame.Surface(
            #     (tile_size, tile_size), pygame.SRCALPHA)
            # pygame.draw.rect(local_surface_light, (0,0,0,self.distance * 10), local_rect)
            # local_surface.blit(local_surface_light, local_rect)


            # append local cell in world surface
            world_surface.blit(local_surface, world_rect)
