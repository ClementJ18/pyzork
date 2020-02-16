from pyzork.entities import Enemy
from pyzork.utils import yes_or_no, post_output
from pyzork.base import qm
from pyzork.errors import EndGame
from pyzork.enums import EndgameReason

from .example_equipment import Sword

class Goblin(Enemy):
    """Golbin"""
    def __init__(self):
        super().__init__(
            base_max_health=15,
            base_damage=2,
            base_defense=0,
            weapon=Sword()
        )
        
class BigGoblin(Enemy):
    def __init__(self):
        super().__init__(
            base_max_health=30,
            base_damage=4,
            base_defense=5,
            weapon=Sword()    
        )        
        
class OldMan(Enemy):
    """OldMan"""
    def __init__(self):
        super().__init__(
            base_max_health=5,
            base_damage=4,
            base_defense=3,    
        )
    
    def print_interaction(self, world):
        post_output("- Talk to the old man in the corner")
        
    def interact(self, world):
        post_output("Hello there traveler, I have a quest, you wanna kill the goblin in the back alley?")
        answer = yes_or_no()
        if answer:
            post_output("Nice")
            qm.start_quest("KillGoblin")
        else:
            post_output("No? Then die!")
            world.initiate_battle([self])
            raise EndGame("You win!", victory=True, reason=EndgameReason.victory)