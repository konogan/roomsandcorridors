# encoding: utf-8

import random

from src.world.helper_grid import init_grid
from src.world.Room import Room
from src.world.Cell import Cell

class Bsd:
    def __init__(self, grid_size: (int, int), threshold):
        self.threshold = threshold
        self.width = grid_size[0]
        self.height = grid_size[1]
        self.bsd_grid = init_grid(grid_size)
        self.bsd_rooms = []
        self.leaves = []

    def run(self):
        self.__split(1, 1, self.height - 1, self.width - 1)
        self.__dig_rooms()
        self.__connect_rooms()

    def get_grid(self) -> [[Cell]]:
        return self.bsd_grid

    def get_rooms(self) -> [Room]:
        return self.bsd_rooms

    def __split(self, min_row, min_col, max_row, max_col):
        # We want to keep splitting until the sections get down to the threshold
        """
        Args:
            min_row:
            min_col:
            max_row:
            max_col:
        """
        seg_height = max_row - min_row
        seg_width = max_col - min_col

        if seg_height < self.threshold and seg_width < self.threshold:
            if random.random() < 0.60:
                self.leaves.append((min_row, min_col, max_row, max_col))
        elif seg_height < self.threshold <= seg_width:
            self.__split_on_vertical(min_row, min_col, max_row, max_col)
        elif seg_height >= self.threshold > seg_width:
            self.__split_on_horizontal(min_row, min_col, max_row, max_col)
        else:
            if random.random() < 0.5:
                self.__split_on_horizontal(min_row, min_col, max_row, max_col)
            else:
                self.__split_on_vertical(min_row, min_col, max_row, max_col)

    def __split_on_horizontal(self, min_row, min_col, max_row, max_col):
        """
        Args:
            min_row:
            min_col:
            max_row:
            max_col:
        """
        split = (min_row + max_row) // 2 + random.choice((-2, -1, 0, 1, 2))
        self.__split(min_row, min_col, split, max_col)
        self.__split(split + 1, min_col, max_row, max_col)

    def __split_on_vertical(self, min_row, min_col, max_row, max_col):
        """
        Args:
            min_row:
            min_col:
            max_row:
            max_col:
        """
        split = (min_col + max_col) // 2 + random.choice((-2, -1, 0, 1, 2))
        self.__split(min_row, min_col, max_row, split)
        self.__split(min_row, split + 1, max_row, max_col)

    def __dig_rooms(self):
        room_id = 0
        for leaf in self.leaves:
            room_id += 1

            # size of zone
            section_width = leaf[3] - leaf[1]
            section_height = leaf[2] - leaf[0]

            # random reduce the size
            room_width = round(random.randrange(60, 100) / 100 * section_width)
            room_height = round(random.randrange(
                60, 100) / 100 * section_height)

            # random shift placement
            if section_height > room_height:
                room_y = leaf[0] + \
                    random.randrange(section_height - room_height)
            else:
                room_y = leaf[0]

            if section_width > room_width:
                room_x = leaf[1] + random.randrange(section_width - room_width)
            else:
                room_x = leaf[1]

            # append room to the world
            room = Room(room_x, room_y, room_width, room_height, room_id)

            for coord_x in range(room.coord.x, room.coord.x + room.width):
                for coord_y in range(room.coord.y, room.coord.y + room.height):
                    self.bsd_grid[coord_x][coord_y].belong_to_room(room.room_id)
            self.bsd_rooms.append(room)

    @staticmethod
    def __get_center_of_leaf(leaf) ->(int,int):
        """
        Args:
            leaf:
        """
        section_width = leaf[3] - leaf[1]
        section_height = leaf[2] - leaf[0]
        return int(leaf[1] + section_width // 2), int(leaf[0] + section_height // 2)

    def __dig_corridors(self, leaf1, leaf2):
        """
        Args:
            leaf1:
            leaf2:
        """
        center1 = self.__get_center_of_leaf(leaf1)
        center2 = self.__get_center_of_leaf(leaf2)

        # draw Horizontal
        if center1[0] != center2[0]:
            y = center1[1]
            if center1[0] < center2[0]:
                start = center1[0]
                end = center2[0] + 1
            else:
                start = center2[0]
                end = center1[0]

            for x in range(start, end):
                if self.bsd_grid[x][y].is_free:
                    self.bsd_grid[x][y].set_corridor()

        # draw Vertical
        if center1[1] != center2[1]:
            x = center2[0]
            if center1[1] < center2[1]:
                start = center1[1]
                end = center2[1] + 1
            else:
                start = center2[1]
                end = center1[1]

            for y in range(start, end):
                if self.bsd_grid[x][y].is_free:
                    self.bsd_grid[x][y].set_corridor()

    def __connect_rooms(self):
        for i, _ in enumerate(self.leaves):
            if i != 0:
                self.__dig_corridors(self.leaves[i - 1], self.leaves[i])
