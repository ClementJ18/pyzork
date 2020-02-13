from pyzork.base import RepeatableQuest, qm
from .example_entities import Goblin
from .example_equipement import Sword

class Kill10Goblin(Quest):
    def setup(self):
        self.kills = 0
        
    def on_kill(self, entity):
        if isinstance(entity, Goblin):
            self.kills += 1
            if self.kills == 10:
                return True
                
    def reward(self, player, world):
        sword = Sword()
        player.add_to_inventory(sword)
        player.inventory.equip(player, sword)
        
qm.add_quest("Kill10Goblin", Kill10Goblin)
