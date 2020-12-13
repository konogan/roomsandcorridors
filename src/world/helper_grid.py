import random
from copy import deepcopy

from src.items.Item import Torch
from src.world.Cell import Cell


def init_grid(grid_size: (int, int)) -> [[Cell]]:
    new_grid = []
    for i in range(grid_size[0] + 1):
        new_grid.append([])
        for j in range(grid_size[1] + 1):
            new_grid[i].append(Cell(i, j))
    return new_grid


def grid_generate_walls(grid: [[Cell]], grid_size: (int, int)) -> [[Cell]]:
    width, height = grid_size
    local_copy = deepcopy(grid)
    for i in range(width + 1):
        for j in range(height + 1):
            if grid[i][j].is_free:
                need_a_wall = False

                if i > 0 and not grid[i - 1][j].is_free:
                    need_a_wall = True
                if i < width and not grid[i + 1][j].is_free:
                    need_a_wall = True
                if j > 0 and not grid[i][j - 1].is_free:
                    need_a_wall = True
                if j < height and not grid[i][j + 1].is_free:
                    need_a_wall = True
                if i > 0 and j < height and not grid[i - 1][j + 1].is_free:
                    need_a_wall = True
                if i > 0 and j > 0 and not grid[i - 1][j - 1].is_free:
                    need_a_wall = True
                if i < width and j > 0 and not grid[i + 1][j - 1].is_free:
                    need_a_wall = True
                if i < width and j < height and not grid[i + 1][j + 1].is_free:
                    need_a_wall = True

                if need_a_wall:
                    local_copy[i][j].set_wall()
    return local_copy


def grid_generate_doors(grid: [[Cell]], grid_size: (int, int)) -> [[Cell]]:
    width, height = grid_size
    local_copy = deepcopy(grid)
    for i in range(width + 1):
        for j in range(height + 1):
            if local_copy[i][j].type == "CORRIDOR_FLOOR":
                corridor = 0
                room = 0
                # 2 walls around
                if (local_copy[i - 1][j].type == "WALL" and local_copy[i + 1][j].type == "WALL") or (
                        local_copy[i][j - 1].type == "WALL" and local_copy[i + 1][j + 1].type == "WALL"):
                    # count corridors
                    if local_copy[i - 1][j].type == "CORRIDOR_FLOOR":
                        corridor += 1
                    if local_copy[i + 1][j].type == "CORRIDOR_FLOOR":
                        corridor += 1
                    if local_copy[i][j - 1].type == "CORRIDOR_FLOOR":
                        corridor += 1
                    if local_copy[i][j + 1].type == "CORRIDOR_FLOOR":
                        corridor += 1

                    # count room
                    if local_copy[i - 1][j].type == "ROOM_FLOOR":
                        room += 1
                    if local_copy[i + 1][j].type == "ROOM_FLOOR":
                        room += 1
                    if local_copy[i][j - 1].type == "ROOM_FLOOR":
                        room += 1
                    if local_copy[i][j + 1].type == "ROOM_FLOOR":
                        room += 1

                    if corridor == 1 and room == 1:
                        local_copy[i][j].set_door()
                        if random.random() < 0.60:
                            local_copy[i][j].open()
                        else:
                            local_copy[i][j].close()
    return local_copy


def grid_random_place_items(grid: [[Cell]], grid_size: (int, int)) -> [[Cell]]:
    width, height = grid_size
    local_copy = deepcopy(grid)
    for i in range(width + 1):
        for j in range(height + 1):
            if grid[i][j].type == "ROOM_FLOOR":
                if random.random() < 0.05:
                    new_item = Torch()
                    local_copy[i][j].items.append(new_item)

    return local_copy
