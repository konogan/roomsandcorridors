
# encoding: utf-8
from enum import Enum
from collections import namedtuple


class States(Enum):
    INIT = 1  # on lauch
    LOAD = 1  # on load
    MENU = 2  # on menu display
    PLAY = 3  # on in-game running
    INVENTORY = 4  # on in-game inventory management


class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


class My_colors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GREY = (125, 125, 125)
    RED = (255, 0, 0)
    PLAYER = (160, 32, 240)
    HISTORY = (50, 50, 50)
    ITEM = (230, 126, 48)


Coord = namedtuple('Coord', 'x y')
