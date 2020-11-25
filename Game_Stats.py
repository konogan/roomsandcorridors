# encoding: utf-8

class GameStats():
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        
        
    def reset_stats(self):
        self.game_active = False
        
        