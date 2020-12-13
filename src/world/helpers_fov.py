import math


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
