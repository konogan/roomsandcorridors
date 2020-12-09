# encoding: utf-8
import os

from src.world.Cell import Cell
from src.world.Room import Room

class Backup:
    """Backup class handle the save en restore of the world"""

    def __init__(self, save_name="default"):
        """
        Args:
            save_name (str): name of the save
        """
        self.save_directory = "saves"
        self.save_name = save_name

        self.save_path = "{}/{}".format(self.save_directory, self.save_name)

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

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

    def load(self, world):
        # rebuild the topology of the grid from the save
        """
        Args:
            world:
        """
        self.__load_topology(world)

        # repopulate the grid items

        # repopulate the rooms from the save and assign them to the grid

        # restore the player position ans inventory

        pass

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
                    row_str += world.grid[x][y].save_type
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
            item_str = "Items : "
            for y in range(world.grid_size[1]):
                for x in range(world.grid_size[0]):
                    if len(world.grid[x][y].items) > 0:
                        for _, item in enumerate(world.grid[x][y].items):
                            item_str += "{},{}-{}|".format(
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
            player_str = "Position :{},{},{}\n".format(
                str(player.coord.x), str(player.coord.y), str(player.orientation))
            outfile.writelines(player_str)
            inventory_str = "Inventory :"
            for index, _ in enumerate(player.inventory.items):
                inventory_str += "{}:{}|".format(
                    str(player.inventory.items[index]),
                    str(player.inventory.quantities[index])
                )
            inventory_str += "\n"
            outfile.writelines(inventory_str)
            # TODO save equipment

        outfile.close()

    def __load_topology(self, world):
        """
        Args:
            world:
        """
        initial_grid = world.grid
        topology_file = open("{}/topology.save".format(self.save_path), 'r')
        y = 0
        for line in topology_file:
            for x, char in enumerate(line.strip()):
                cell = Cell(x, y)
                if char == ".":
                    cell.set_floor()
                elif char == "#":
                    cell.set_wall()
                elif char == "O":
                    cell.set_door()
                    cell.open()
                elif char == "C":
                    cell.set_door()
                    cell.close()
                else:
                    pass
                initial_grid[x][y] = cell
            y += 1
        topology_file.close()
        world.grid = initial_grid

    def __load_rooms(self, world):
        """
        Args:
            world: world instance
        """
        room_file = open("{}/rooms.save".format(self.save_path), 'r')
        line = room_file.readline()
        for room_save in line.split('|'):
            #1:1,1,4,7 room_id:x,y,w,h
            room=room_save.split(':')
            coord= room[1].split(',')
            newroom = Room(coord[0], coord[1], coord[2], coord[3], room[0])
            
            for coord_x in range(room.coord.x, room.coord.x + room.width):
                for coord_y in range(room.coord.y, room.coord.y + room.height):
                    world.grid[coord_x][coord_y].belong_to_room(newroom.room_id)

            world.rooms.append(newroom)
        room_file.close()

    def __load_items(self, world):
        """
        Args:
            world:
        """
        pass

    def __load_player(self, world):
        """
        Args:
            world:
        """
        pass
