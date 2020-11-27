# encoding: utf-8

class GameStats():
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.messages = []

    def reset_stats(self):
        self.game_active = False

    def add_message(self, text):
        self.messages.append(text)
        print(text)

    def player_move(self, direction):
        if direction is None:
            self.add_message('You hit the wall')
        else:
            if direction[1] < 0:
                orientation = "North"
            if direction[1] > 0:
                orientation = "South"
            if direction[0] > 0:
                orientation = "East"
            if direction[0] < 0:
                orientation = "West"
            self.add_message('You head '+orientation)
