from pyzork.world import World, Location, Shop
from pyzork.utils import post_output
from pyzork.enums import Direction
from pyzork.base import QM
from pyzork.equipment import ShopItem

from .example_entities import OldMan, Goblin, BigGoblin, Table
from .example_equipment import Sword, SwordAndShield, HealthPotion, HealingOnguent, Key


#run in main directory with python -m examples.example_world

class MarketPlace(Location):
    """The Market"""
    def enter(self, player, from_location):
        post_output("This is a nice market")
        
class Tavern(Location):
    """The Tavern"""
    def __init__(self):
        super().__init__(
            npcs=[OldMan(), Table()]    
        )
    
    def enter(self, player, from_location):
        post_output("Reeks of drunkards")
        
class BackAlley(Location):
    """back alley"""
    def enter(self, player, from_location):
        self.enemies.append(Goblin())
        
class Island(Location):
    """A Small Island"""
    def enter(self, player, from_location):
        if isinstance(from_location, Docks):
            post_output("You beach your boat on the sand")
        else:
            post_output("You arrive on a beach")
            
    def exit(self, to_location):
        if isinstance(to_location, Docks):
            post_output("You take the boat back to the docks")
        else:
            post_output("You leave the beach")
            
Beach = Location.from_dict(name="Beach", description="A sandy beach")

MarketShop = Shop.from_dict(
    resell=0.25,
    name="A Big Shop",
    items=[
        ShopItem(item=Sword, price=25, amount=1), 
        ShopItem(item=HealthPotion, amount=5, price=10),
        ShopItem(item=HealingOnguent, amount=3, price=5),
        ShopItem(item=SwordAndShield, price=30)
    ]
)
            
class HiddenTemple(Location):
    """A hidden temple"""
    def enter(self, player, from_location):
        post_output("You enter the jungle and find a temple")
        
class HiddenTempleInside(Location):
    """Hidden Temple (Inside)"""
    def __init__(self):
        super().__init__(enemies=[BigGoblin])
        
    def enter(self, player, from_location):
        post_output("It's really dusty in here")
        
class Docks(Location):
    """The Docks"""
    def enter(self, player, from_location):
        # if not self.discovered:
        #     QM.start_quest("KillGoblin")
        
        if not isinstance(from_location, Island):
            post_output("some ugly docks")
    
    def exit(self, player, to_location):
        if isinstance(to_location, Island):
            post_output("You take the boat")
        
        
tavern = Tavern()
market = MarketPlace()
island = Island()
temple = HiddenTemple()
docks = Docks()
hidden = HiddenTempleInside()
alley = BackAlley()
shop = MarketShop()
