from pyzork.base import Quest, qm
from pyzork.enums import Direction
from pyzork.utils import post_output

from .example_entities import Goblin, OldMan
from .example_equipment import Sword
from .example_world import temple, hidden

@qm.add(repeatable=5)
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
        
        #it is usually not recommended to force the player to equip a
        #certain item but this is just an example
        player.inventory.equip(player, sword)

@qm.add(name="FindTheOldMan")    
class TerribleQuestName(Quest):
    def on_interact(self, entity):
        if isinstance(entity, OldMan):
            return True
            
    def reward(self, player, world):
        post_output("You have discovered a secret entrance to the temple")
        temple.one_way_connect(Direction.west, hidden)
    
