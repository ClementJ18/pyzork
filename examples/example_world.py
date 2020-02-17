from pyzork.world import World, Location
from pyzork.utils import post_output
from pyzork.enums import Direction
from pyzork.base import qm

from .example_entities import OldMan, Goblin, BigGoblin


#run in main directory with python -m examples.example_world

class MarketPlace(Location):
    """The Market"""
    def enter(self, from_location):
        post_output("This is a nice market")
        
class Tavern(Location):
    """The Tavern"""
    def __init__(self):
        super().__init__(
            npcs=[OldMan()]    
        )
    
    def enter(self, from_location):
        post_output("Reeks of drunkards")
        
class BackAlley(Location):
    """back alley"""
    def enter(self, from_location):
        self.enemies.append(Goblin())
        
class Island(Location):
    """A Small Island"""
    def enter(self, from_location):
        if isinstance(from_location, Docks):
            post_output("You beach your boat on the sand")
        else:
            post_output("You arrive on a beach")
            
    def exit(self, to_location):
        if isinstance(to_location, Docks):
            post_output("You take the boat back to the docks")
        else:
            post_output("You leave the beach")
            
class HiddenTemple(Location):
    """A hidden temple"""
    def enter(self, from_location):
        post_output("You enter the jungle and find a temple")
        
class HiddenTempleInside(Location):
    """Hidden Temple (Inside)"""
    def __init__(self):
        super().__init__(enemies=[BigGoblin])
        
    def enter(self, from_location):
        post_output("It's really dusty in here")
        
class Docks(Location):
    """The Docks"""
    def enter(self, from_location):
        # if not self.discovered:
        #     qm.start_quest("KillGoblin")
        
        if not isinstance(from_location, Island):
            post_output("some ugly docks")
    
    def exit(self, to_location):
        if isinstance(to_location, Island):
            post_output("You take the boat")
        
        
tavern = Tavern()
market = MarketPlace()
island = Island()
temple = HiddenTemple()
docks = Docks()
hidden = HiddenTempleInside()
alley = BackAlley()
