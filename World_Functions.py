# encoding: utf-8`
from collections import namedtuple
import random


from BSD_Generator import BSDGenerator

from Cell import Cell

Coord = namedtuple('Coord', 'x y')


def make_grid(grid_size):
    cols = grid_size[0]
    rows = grid_size[1]
    grid = []
    for i in range(cols+1):
        grid.append([])
        for j in range(rows+1):
            grid[i].append(Cell(i, j))
    return grid


def randomize_rooms(world):
    BSDGenerator(world, 15)


def build_walls(world):
    # iterate over all FREE cells
    for i in range(world.grid_size[0]):
        for j in range(world.grid_size[1]):
            if world.grid[i][j].is_free:
                need_a_wall = False
                if not world.grid[i-1][j].is_free:
                    need_a_wall = True
                if not world.grid[i+1][j].is_free:
                    need_a_wall = True
                if not world.grid[i][j-1].is_free:
                    need_a_wall = True
                if not world.grid[i][j+1].is_free:
                    need_a_wall = True
                if not world.grid[i-1][j+1].is_free:
                    need_a_wall = True
                if not world.grid[i-1][j-1].is_free:
                    need_a_wall = True
                if not world.grid[i+1][j-1].is_free:
                    need_a_wall = True
                if not world.grid[i+1][j+1].is_free:
                    need_a_wall = True

                if need_a_wall:
                    world.grid[i][j].set_wall()


def place_door(world):
    for i in range(world.grid_size[0]):
        for j in range(world.grid_size[1]):
            if world.grid[i][j].type == "CORRIDOR":
                corridor = 0
                room = 0
                # 2 walls arround
                if (world.grid[i-1][j].type == "WALL" and world.grid[i+1][j].type == "WALL") or (world.grid[i][j-1].type == "WALL" and world.grid[i+1][j+1].type == "WALL"):
                    # count corridors
                    if world.grid[i-1][j].type == "CORRIDOR":
                        corridor += 1
                    if world.grid[i+1][j].type == "CORRIDOR":
                        corridor += 1
                    if world.grid[i][j-1].type == "CORRIDOR":
                        corridor += 1
                    if world.grid[i][j+1].type == "CORRIDOR":
                        corridor += 1

                    # count room
                    if world.grid[i-1][j].type == "ROOM":
                        room += 1
                    if world.grid[i+1][j].type == "ROOM":
                        room += 1
                    if world.grid[i][j-1].type == "ROOM":
                        room += 1
                    if world.grid[i][j+1].type == "ROOM":
                        room += 1

                    if corridor == 1 and room == 1 and random.random() < 0.60:
                        world.grid[i][j].set_door()
