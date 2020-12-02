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
        self.state = ""

    def belong_to_room(self, room_id):
        self.is_free = False
        self.belongs_to = room_id
        self.type = "ROOM"

    def set_corridor(self):
        self.is_free = False
        self.belongs_to = 0
        self.type = "CORRIDOR"

    def set_door(self, state='CLOSE'):
        self.is_free = False
        self.state = state
        self.type = "DOOR"

    def set_wall(self):
        self.type = "WALL"

    def is_walkable(self):
        return self.type != "WALL"

    def block_fov(self):
        return self.type == "WALL" or (self.type == "DOOR" and self.state == "CLOSE")

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
        export['a'] = self.state
        return export

    def from_json(self, json_data):
        self.is_free = json_data['f']
        self.belongs_to = json_data['b']
        self.type = json_data['t']
        self.visibility = json_data['v']
        self.was_discovered = json_data['d']
        self.last_time_was_seen = json_data['s']
        self.state = json_data['a']

    def render(self, world_surface, tile_size, offset=(0, 0), debug=False, is_under_mouse=False):
        # only render if necessary
        if self.visibility or self.was_discovered:

            local_surface = pygame.Surface((tile_size, tile_size))
            light_surface = pygame.Surface((tile_size, tile_size))

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

            elif self.type == "ROOM":
                cell_color = My_colors.WHITE
            elif self.type == "CORRIDOR":
                cell_color = My_colors.WHITE
            elif self.type == "DOOR":
                cell_color = My_colors.GREEN
            else:
                cell_color = My_colors.BLACK

            cell_color_in_memory = My_colors.HISTORY

            # drawing local cell
            if self.visibility:

                # cell pass
                if self.state == "OPEN":
                    pygame.draw.rect(
                        local_surface, cell_color.value, local_rect, 2)
                else:
                    pygame.draw.rect(
                        local_surface, cell_color.value, local_rect)

                # mouse pass
                if is_under_mouse and debug:
                    pygame.draw.rect(
                        local_surface, My_colors.RED.value, local_rect, 1)

                # light pass for the cell based on distance of the player

                # solution 1 lerp colors
                # color = color1.lerp(color2, t)  # Lerp the two colors. With 0<t<1

                # solution 2 new function
                # def blend_colors(initial_color, final_color, amount):
                #     # Calc how much to add or subtract from start color
                #     r_diff = (final_color.r - initial_color.r) * amount
                #     g_diff = (final_color.g - initial_color.g) * amount
                #     b_diff = (final_color.b - initial_color.b) * amount
                #     # Create and return new color
                #     return pygame.Color((int)(round(initial_color.r + r_diff)),
                #                         (int)(round(initial_color.g + g_diff)),
                #                         (int)(round(initial_color.b + b_diff)))

                # solution 3 add a light layer with an alpha
                # pygame.draw.rect(light_surface, My_colors.HISTORY.value, local_rect)
                # light_surface.set_alpha((self.distance+5 )* 10)
                # local_surface.blit(light_surface, local_rect,local_rect)

            else:
                if self.was_discovered:
                    pygame.draw.rect(
                        local_surface, cell_color_in_memory.value, local_rect)

            if debug and self.visibility:
                cell_font = pygame.font.SysFont('arial', 15)
                number = cell_font.render("{}".format(
                    self.distance), True, (0, 0, 255))

                local_surface.blit(number, local_rect)

            # append local cell in world surface
            world_surface.blit(local_surface, world_rect)
