# encoding: utf-8

class Camera():
    def __init__(self, world):
        self.width_display = world.settings.screen_width - world.settings.ui_width
        self.height_display = world.settings.screen_height
        self.width_grid = int(
            (world.settings.screen_width - world.settings.ui_width)//world.settings.tile_size)
        self.height_grid = int(
            (world.settings.screen_height)//world.settings.tile_size)
        self.center_shift_x = int(
            ((world.settings.screen_width - world.settings.ui_width)//world.settings.tile_size)//2)
        self.center_shift_y = int(
            ((world.settings.screen_height)//world.settings.tile_size)//2)
        self.look_at(0, 0)

    def __repr__(self):
        return "<Camera lookAt(x={},y={}) tl(x={},y={}) br(x={},y={})>".format(self.look_at_x, self.look_at_y, self.top_left_x, self.top_left_y, self.bottom_right_x, self.bottom_right_y)

    def look_at(self, position_x, position_y):
        self.look_at_x = position_x
        self.look_at_y = position_y
        self.top_left_x = self.look_at_x-self.center_shift_x
        self.top_left_y = self.look_at_y-self.center_shift_y
        self.bottom_right_x = self.look_at_x+self.center_shift_x
        self.bottom_right_y = self.look_at_y+self.center_shift_y
