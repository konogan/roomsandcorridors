
# encoding: utf-8
from collections import namedtuple
from enum import Enum


class States(Enum):
    INIT = 1  # on launch
    LOAD = 1  # on load
    MENU = 2  # on menu display
    PLAY = 3  # on in-game running
    INVENTORY = 4  # on in-game inventory management
    PLAYER_TURN = 5
    DUNGEON_TURN = 6


class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


class MyColors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GREY = (125, 125, 125)
    RED = (255, 0, 0)
    PLAYER = (160, 32, 240)
    HISTORY = (50, 50, 50)
    ITEM = (230, 126, 48)
    SELECTED = (255, 175, 0)
    BACKGROUND = (20, 20, 0)
    BACKGROUND_LIGHT = (50, 50, 20)
    TEXT = (200, 200, 200)


Coord = namedtuple('Coord', 'x y')
