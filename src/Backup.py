# encoding: utf-8
import os

from src.actors.Player import Player
from src.world.Room import Room
from src.world.helper_grid import *


class Backup:
    """Backup class handle the save en restore of the world"""

    def __init__(self, save_name="default"):
        """
        Args:
            save_name (str): name of the save
        """
        self.save_directory = "saves"
        self.save_name = save_name
        self.grid_size = None
        self.grid = None
        self.rooms = []
        self.items = []
        self.player = None

        self.save_path = "{}/{}".format(self.save_directory, self.save_name)
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def is_available(self):
        return os.path.isfile("{}/topology.save".format(self.save_path)) and os.path.isfile(
            "{}/items.save".format(self.save_path)) and os.path.isfile(
            "{}/rooms.save".format(self.save_path)) and os.path.isfile("{}/player.save".format(self.save_path))

    def save(self, world):
        # save the world topology
        """
        Args:
            world: world instance
        """
        self.__save_topology(world)
        # save the rooms
        self.__save_rooms(world.rooms)
        # save items
        self.__save_items(world)
        # save player
        self.__save_player(world.player)
        # TODO save the player history ?

    def load(self, grid_size=(0, 0)):
        # rebuild the topology of the grid from the save of the cell and the room
        self.grid_size = grid_size
        self.__load_grid()
        self.__load_rooms_and_add_in_the_room()
        self.__load_items_on_the_grid()
        self.__load_player()

    def get_grid(self):
        return self.grid

    def get_rooms(self):
        return self.rooms

    def get_player(self):
        return self.player

    def get_items(self):
        return self.items

    def __save_topology(self, world):
        # TODO save different level in different file
        """
        Args:
            world: world instance
        """
        with open("{}/topology.save".format(self.save_path), 'w') as outfile:
            # save the world geography
            for y in range(world.grid_size[1]):
                row_str = ""
                for x in range(world.grid_size[0]):
                    row_str += str(world.grid[x][y].save_type)
                row_str += "\n"
                outfile.writelines(row_str)
        outfile.close()

    def __save_rooms(self, rooms):
        """
        Args:
            rooms: world rooms instances
        """
        with open("{}/rooms.save".format(self.save_path), 'w') as outfile:
            # save the rooms
            row_str = ""
            for _, room in enumerate(rooms):
                row_str += "{}:{},{},{},{}|".format(
                    str(room.room_id),
                    str(room.coord.x),
                    str(room.coord.y),
                    str(room.width),
                    str(room.height))
            row_str += "\n"
            outfile.writelines(row_str)
        outfile.close()

    def __save_items(self, world):
        """
        Args:
            world: world instance
        """
        with open("{}/items.save".format(self.save_path), 'w') as outfile:
            # save the world geography
            item_str = ""

            for x in range(world.grid_size[0]):
                for y in range(world.grid_size[1]):
                    if len(world.grid[x][y].items) > 0:
                        for _, item in enumerate(world.grid[x][y].items):
                            item_str += "{},{},{}|".format(
                                str(x),
                                str(y),
                                str(item)
                            )
            item_str += "\n"
            outfile.writelines(item_str)
        outfile.close()

    def __save_player(self, player):
        """
        Args:
            player: player instance
        """
        with open("{}/player.save".format(self.save_path), 'w') as outfile:
            # save player coordinate
            player_str = "Position :{},{},{}\n".format(
                str(player.coord.x), str(player.coord.y), str(player.current_room))
            outfile.writelines(player_str)

            # save inventory
            inventory_str = "Inventory :"
            for index, _ in enumerate(player.inventory.items):
                inventory_str += "{},{}|".format(
                    str(player.inventory.items[index]),
                    str(player.inventory.quantities[index])
                )
            inventory_str += "\n"
            outfile.writelines(inventory_str)

            # TODO save equipment

        outfile.close()

    def __load_grid(self) -> [[Cell]]:
        new_grid = init_grid(self.grid_size)
        topology_file = open("{}/topology.save".format(self.save_path), 'r')
        coord_y = 0
        for line in topology_file:
            coord_x = 0
            for _, char in enumerate(line):
                cell = Cell(coord_x, coord_y)
                if char == ".":
                    cell.set_floor()
                elif char == "#":
                    cell.set_wall()
                elif char == "c":
                    cell.set_corridor()
                elif char == "O":
                    cell.set_door()
                    cell.open()
                elif char == "C":
                    cell.set_door()
                    cell.close()
                else:
                    pass
                new_grid[coord_x][coord_y] = cell
                coord_x += 1
            coord_y += 1
        topology_file.close()
        self.grid = deepcopy(new_grid)

    def __load_rooms_and_add_in_the_room(self):
        room_file = open("{}/rooms.save".format(self.save_path), 'r')
        line = room_file.readline()

        self.rooms = []

        for room_save in line.rstrip('|\n').split('|'):
            room = room_save.split(':')
            coord = room[1].split(',')
            room_new = Room(int(coord[0]), int(coord[1]), int(
                coord[2]), int(coord[3]), int(room[0]))

            for coord_x in range(room_new.coord.x, room_new.coord.x + room_new.width):
                for coord_y in range(room_new.coord.y, room_new.coord.y + room_new.height):
                    self.grid[coord_x][coord_y].belong_to_room(
                        room_new.room_id)

            self.rooms.append(room_new)
        room_file.close()

    def __load_items_on_the_grid(self):
        item_file = open("{}/items.save".format(self.save_path), 'r')
        line = item_file.readline()
        item_file.close()

        for item_save in line.rstrip('|\n').split('|'):
            details = item_save.split(',')
            coord_x = int(details[0])
            coord_y = int(details[1])
            item_class = globals()[details[2]]
            my_item = item_class()
            self.grid[coord_x][coord_y].append_item(my_item)


    def __load_player(self):
        # load the player save file
        player_file = open("{}/player.save".format(self.save_path), 'r')
        player_line = player_file.readline().split(":")[1].split(',')
        inventory_line = player_file.readline().rstrip('|\n').split(":").pop(1).split("|")
        player_file.close()

        # initialize the player
        saved_player = Player(
            int(player_line[0]),
            int(player_line[1]),
            int(player_line[2]))

        # populate is inventory
        for inventory_item in inventory_line:
            details = inventory_item.split(',')
            item_class = globals()[details[0]]
            number_of_type = int(details[1])
            my_item = item_class()
            for _ in range(number_of_type):
                saved_player.pick_item(my_item)

        # save it on backup
        self.player = saved_player


