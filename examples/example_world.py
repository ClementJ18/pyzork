from pyzork.world import World, Location
from pyzork.utils import post_output
from pyzork.enums import Direction

#run in main directory with python -m examples.example_world

class MarketPlace(Location):
    """The Market"""
    def enter(self):
        post_output("This is a nice market")
        
class Tavern(Location):
    """The Tavern"""
    def enter(self):
        post_output("Reeks of drunkards")
        
tavern = Tavern()
market = MarketPlace()

tavern.two_way_connect(Direction.south, market)

world = World([tavern, market])
world.game_loop()
