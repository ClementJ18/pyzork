from pyzork.entities import Player
from pyzork.world import World
from pyzork.base import game_loop, QM
from pyzork.levels import ExperienceLevels
from pyzork.utils import post_output
from pyzork.equipment import Inventory

from .example_world import *
from .example_quest import *
from .example_equipment import Sword
from .example_levels import 

tavern.two_way_connect(Direction.south, market)
market.two_way_connect(Direction.south, docks)
docks.two_way_connect(Direction.east, island)
docks.two_way_connect(Direction.west, beach)
island.two_way_connect(Direction.north, temple)
market.two_way_connect(Direction.west, alley)
market.two_way_connect(Direction.east, shop)
hidden.one_way_connect(Direction.east, temple)

def basic_reward(levels):
    levels.entity.base_damage *= 0.1
    levels.entity.base_defense *= 0.1
    levels.entity.health += levels.entity.base_max_health * 0.1
    levels.entity.base_max_health *= 0.1

player = Player(
    max_health=100,
    damage=3,
    defense=2,
    max_energy=15,
    experience=ExperienceLevels(
        requirement=100, 
        modifier=1.2, 
        max_level=10, 
        reward=basic_reward,
        r3=lambda levels: levels.player.add_ability(HealSpell()),
        r5=lambda levels: levels.player.add_ability(WarRoarSpell()),
        r7=lambda levels: levels.player.add_ability(FireballSpell()),
    ),
    money=100,
    inventory=Inventory(items=[Sword()])
)
world = World(locations=[tavern, market, island, temple, docks, hidden, shop, beach, alley], player=player, start=market)

if __name__ == '__main__':
    QM.start_quest("KillBigGoblin")
    
    player.add_to_inventory(Sword())
    
    post_output("="*15)
    post_output("WELCOME TO TEMPLATE ZORK")
    post_output("="*15)
    post_output("The realm is in terrible danger. With entire kingdom on the border of chaos you, Generic Protagonist #12, must slay the Big Golbin in the temple, on the island south of the market.")
    input("press enter to begin")
    game_loop(world)
    