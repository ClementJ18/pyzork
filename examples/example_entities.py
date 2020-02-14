from pyzork.entities import Enemy, NPC
from pyzork.utils import yes_or_no, post_output
from pyzork.base import qm

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
        post_output("Hello there traveler, I have a quest, you wanna kill 10 golbins?")
        answer = yes_or_no()
        if answer:
            post_output("Nice")
            qm.start_quest("Kill10Goblin")
        else:
            post_output("No? Then die!")
            world.initiate_battle([self])
