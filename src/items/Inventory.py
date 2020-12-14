# encoding: utf-8

class Inventory():
    def __init__(self):
        self.items = []
        self.quantities = []

    def print(self):
        length = len(self.items)
        i = 0
        while i < length:
            print(str(self.items[i]) + "->" + str(self.quantities[i]))
            i += 1

    def add(self, item_to_add, quantity=1):
        if item_to_add in self.items:
            self.quantities[self.items.index(item_to_add)] += quantity
        else:
            self.items.append(item_to_add)
            self.quantities.append(quantity)

    def remove(self, item_to_remove, quantity=1):
        if item_to_remove in self.items:
            item_to_remove_index = self.items.index(item_to_remove)
            new_quantity = self.quantities[item_to_remove_index] - quantity
            if new_quantity < 0:
                new_quantity = 0
            self.quantities[item_to_remove_index] = new_quantity

    def transfer(self, other_inventory):
        # TODO transfer an item betwenn two inventories
        pass
