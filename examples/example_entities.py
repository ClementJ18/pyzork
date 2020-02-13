from pyzork.entities import Enemy
from example_equipment import Sword

class Goblin(Enemy):
    """Golbin"""
    def __init__(self):
        super().__init__(
            base_max_health=15,
            base_damage=2,
            base_defense=0,
            weapon=Sword()
        )
