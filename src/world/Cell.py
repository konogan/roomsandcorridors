# encoding: utf-8


import pygame

from src.Constants import Coord, MyColors


class Cell:
    """A cell represent a location in the grid
    """

    def __init__(self, coord_x, coord_y):
        """
        Args:
            coord_x:
            coord_y:
        """
        self.coord = Coord(coord_x, coord_y)
        # occupation of the cell, by an item, a door, a wall, etc....
        self.is_free = True
        self.belongs_to = 0     # room id
        self.type = None        # type of cell
        self.save_type = " "    # char used for save
        self.visibility = False
        self.was_discovered = False
        self.last_time_was_seen = 0
        self.distance = 0
        self.state = ""
        self.items = []

    def __repr__(self):
        return '{coord ('+str(self.coord.x)+','+str(self.coord.y)+'), type='+str(self.type) + ', belongsto='+str(self.belongs_to) + '}'

    def __str__(self):
        return 'Cell(coord ('+str(self.coord.x)+','+str(self.coord.y)+'),free='+str(self.is_free) + ', type='+str(self.type) + ', belongsto='+str(self.belongs_to) + ')'

    def append_item(self, item_to_append):
        self.items.append(item_to_append)

    def belong_to_room(self, room_id):
        """
        Args:
            room_id:
        """
        self.belongs_to = room_id
        self.set_floor()

    def set_floor(self):
        self.is_free = False
        self.type = "ROOM_FLOOR"
        self.save_type = "."

    def set_corridor(self):
        self.is_free = False
        self.belongs_to = 0
        self.type = "CORRIDOR_FLOOR"
        self.save_type = "c"

    def set_door(self, state='CLOSE'):
        self.is_free = False
        self.type = "DOOR"
        if state == "CLOSE":
            self.close()
        else:
            self.open()

    def open(self):
        self.state = "OPEN"
        self.save_type = "O"

    def close(self):
        self.state = "CLOSE"
        self.save_type = "C"

    def set_wall(self):
        self.type = "WALL"
        self.save_type = "#"
        self.is_free = False

    def is_wall(self):
        return self.type == "WALL"

    def is_walkable(self):
        return self.type == "ROOM_FLOOR" or self.type == "CORRIDOR_FLOOR" or (self.type == "DOOR" and self.state == "OPEN")

    def is_door_close(self):
        return self.type == "DOOR" and self.state == "CLOSE"

    def is_door_open(self):
        return self.type == "DOOR" and self.state == "OPEN"

    def block_fov(self):
        return self.type == "WALL" or (self.type == "DOOR" and self.state == "CLOSE")

    def set_visibility(self, visibility, current_turn, distance_from_player=0):
        """
        Args:
            visibility:
            current_turn:
            distance_from_player:
        """
        self.visibility = visibility
        self.distance = distance_from_player
        if visibility:
            self.last_time_was_seen = current_turn
            self.was_discovered = True
        else:
            # number of turn of memory
            if current_turn - self.last_time_was_seen > 100:
                self.was_discovered = False

    def render(self, tile_size, debug=False, is_under_mouse=False):
        # TODO only render if necessary
        cell_surface = pygame.Surface((tile_size, tile_size))
        cell_rect = pygame.Rect((0, 0), (tile_size, tile_size))

        # define style based on type
        if self.type == "WALL":
            cell_color = MyColors.GREY
        elif self.type == "ROOM_FLOOR":
            cell_color = MyColors.WHITE
        elif self.type == "CORRIDOR_FLOOR":
            cell_color = MyColors.WHITE
        elif self.type == "DOOR":
            cell_color = MyColors.GREEN
        else:
            cell_color = MyColors.BLACK

        cell_color_in_memory = MyColors.HISTORY

        # drawing local cell
        if self.visibility or True:

            # cell pass
            if self.state == "OPEN":
                pygame.draw.rect(
                    cell_surface, cell_color.value, cell_rect, 2)
            else:
                pygame.draw.rect(
                    cell_surface, cell_color.value, cell_rect)

            # content pass
            for content_of_cell in self.items:
                object_surface = content_of_cell.render_surface(tile_size)
                cell_surface.blit(object_surface, cell_rect)

            # mouse pass
            if is_under_mouse and debug:
                pygame.draw.rect(
                    cell_surface, MyColors.RED.value, cell_rect, 1)

        else:
            if self.was_discovered:
                pygame.draw.rect(
                    cell_surface, cell_color_in_memory.value, cell_rect)

        # cell_font = pygame.font.SysFont('arial', 8)
        # number = cell_font.render("{},{}".format(
        #     self.coord.x, self.coord.y), True, (0, 0, 255))
        # cell_surface.blit(number, cell_rect)

        return cell_surface
