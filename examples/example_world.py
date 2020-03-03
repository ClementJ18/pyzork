from pyzork.world import World, Location, Shop
from pyzork.utils import post_output
from pyzork.enums import Direction
from pyzork.base import QM
from pyzork.equipment import ShopItem

from .example_entities import OldMan, Goblin, BigGoblin, Table
from .example_equipment import Sword, SwordAndShield, HealthPotion, HealingOnguent, Key
       
MarketPlace = Location.from_dict(name="MarketPlace", description="This is a nice market")
Tavern = Location.from_dict(name="Tavern of the Bork", description="Reeks of Drunkards", npcs=[OldMan, Table])
        
class BackAlley(Location):
    """Back Alley"""
    
    def enter(self, player, from_location):
        post_output(f"{self.name}\n\nCareful, golbins hang out here.")
        self.enemies.append(Goblin())
        
class Island(Location):
    """A Small Island"""
    def enter(self, player, from_location):
        post_output(self.name)
        if isinstance(from_location, Docks):
            post_output("\n\nYou beach your boat on the sand")
        else:
            post_output("\n\nYou arrive on a beach")
            
    def exit(self, player, to_location):
        post_output(self.name)
        if isinstance(to_location, Docks):
            post_output("\n\nYou take the boat back to the docks")
        else:
            post_output("\n\nYou leave the beach")
            
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
         
HiddenTemple = Location.from_dict(name="Hidden Temple (Outside)", description="You are standing in front of a temple entrance")   
HiddenTempleInside = Location.from_dict(name="Hidden Temple (Inside)", description="It's really dusty in here", enemies=[BigGoblin])    
        
class Docks(Location):
    """The Docks"""
    def enter(self, player, from_location):
        post_output(self.name)        
        if not isinstance(from_location, Island):
            post_output("some ugly docks")
    
    def exit(self, player, to_location):
        post_output(self.name)
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
beach = Beach()
