from pyzork.base import Quest, QM
from pyzork.enums import Direction, EndgameReason
from pyzork.utils import post_output
from pyzork.errors import EndGame

from .example_entities import Goblin, OldMan, BigGoblin
from .example_equipment import Sword
from .example_world import temple, hidden

@QM.add(id="KillGoblin")
class KillGoblin(Quest):
    def on_death(self, entity):
        if isinstance(entity, Goblin):
            return True
                
    def reward(self, player, world):
        post_output("You have discovered a secret entrance to the temple")
        temple.two_way_connect(Direction.west, hidden)
        
@QM.add(id="KillBigGoblin")
class KillBigGoblin(Quest):
    def on_death(self, entity):
        if isinstance(entity, BigGoblin):
            return True
            
    def reward(self, player, world):
        raise EndGame("You win!", victory=True, reason=EndgameReason.victory)

@QM.add(id="FindTheOldMan", name="FindTheOldMan")    
class TerribleQuestName(Quest):
    def on_interact(self, entity):
        if isinstance(entity, OldMan):
            return True
            
    def reward(self, player, world):
        sword = Sword()
        player.add_to_inventory(sword)
        
        #it is usually not recommended to force the player to equip a
        #certain item but this is just an example
        player.inventory.equip(player, sword)
    
