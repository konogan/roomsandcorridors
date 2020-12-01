
# encoding: utf-8
from enum import Enum
from collections import namedtuple


class States(Enum):
    INIT = 1  # on lauch
    LOAD = 1  # on load
    MENU = 2  # on menu display
    PLAY = 3  # on in-game running
    ITEM = 4  # on in-gmae inventory management


class My_colors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GREY = (125, 125, 125)
    RED = (255, 0, 0)
    PLAYER = (160, 32, 240)


Coord = namedtuple('Coord', 'x y')
