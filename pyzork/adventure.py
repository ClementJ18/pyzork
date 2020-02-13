from .base import qm
from .errors import ZorkError


class Adventure: 
    def __init__(self, **kwargs):
        self.world = kwargs.get("world")
        self.player = kwargs.get("player")
        self.setup()
        
        self.game_loop()
        
    def setup(self):
        pass
        
    def game_loop(self):
        try:
            pass            
        except Exception as e:
            self.error_handler(e)
                    
            