from pyzork.entities import NPC
from pyzork.utils import yes_or_no, post_output
from pyzork.base import QM
from pyzork.errors import EndGame
from pyzork.enums import EndgameReason

from .example_equipment import Sword, Key

class Goblin(NPC):
    """Golbin"""
    def __init__(self):
        super().__init__(
            max_health=15,
            damage=2,
            defense=0,
            weapon=Sword()
        )
        
BigGoblin = NPC.from_dict(
    max_health=30,
    damage=4,
    defense=5,
    weapon=Sword(),
    name="Big Golbin",
    description="The BBG"
)        
        
class OldMan(NPC):
    """OldMan"""
    def __init__(self):
        super().__init__(
            max_health=5,
            damage=4,
            defense=3,    
        )
    
    def print_interaction(self, world):
        post_output("- Talk to the old man in the corner")
        
    def interaction(self, world):
        post_output("oi m8 shank that gobbo in the back and I'll give you a key")
        answer = yes_or_no()
        if answer:
            post_output("Nice")
            QM.start_quest("KillGoblin")
        else:
            post_output("No? Then die!")
            world.initiate_battle([self])
            raise EndGame("You win!", victory=True, reason=EndgameReason.victory)
            
class Table(NPC):
    def print_interaction(self, world):
        post_output("- Check the drawers of a weird looking table in the corner")
        
    def interaction(self, world):
        if self.interacted:
            post_output("There is nothing left")
        else:
            post_output("You find a key in the drawer.")
            world.player.add_to_inventory(Key())
