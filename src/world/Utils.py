

import math
import random

from src.generators.Bsd import Bsd
from src.world.Cell import Cell
from src.items.Item import Torch


def make_grid(grid_size: (int, int)):
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
