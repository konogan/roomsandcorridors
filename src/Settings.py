# encoding: utf-8
from dataclasses import dataclass


@dataclass
class Settings:
    screen_width = 1200
    screen_height = 800
    ui_width = 400
    grid_width = 30
    grid_height = 30
    tile_size = 24
    name = "Rooms & Corridors"

    @property
    def screen_size(self) -> (int, int):
        return self.screen_width, self.screen_height

    @property
    def world_size(self) -> (int, int):
        return self.screen_width - self.ui_width, self.screen_height

    @property
    def world_size_center(self) -> (int, int):
        return int((self.screen_width - self.ui_width) // 2), int(self.screen_height // 2)

    @property
    def ui_size(self) -> (int, int):
        return self.ui_width, self.screen_height
