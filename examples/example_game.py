from pyzork.entities import Player
from pyzork.world import World
from pyzork.base import game_loop, QM
from pyzork.levels import ExperienceLevels
from pyzork.utils import post_output

from .example_world import *
from .example_quest import *

if __name__ == '__main__':
    tavern.two_way_connect(Direction.south, market)
    market.two_way_connect(Direction.south, docks)
    docks.two_way_connect(Direction.east, island)
    island.two_way_connect(Direction.north, temple)
    # hidden.one_way_connect(Direction.west, temple)
    market.two_way_connect(Direction.west, alley)
    market.two_way_connect(Direction.east, shop)
    
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
            reward=basic_reward
        ),
        money=100
    )
    world = World([tavern, market, island, temple, docks, hidden, shop], player, start=market)
    QM.start_quest("KillBigGoblin")
    
    post_output("="*15)
    post_output("WELCOME TO TEMPLATE ZORK")
    post_output("="*15)
    post_output("The realm is in terrible danger. With entire kingdom on the border of chaos you, Generic Protagonist #12, must slay the Big Golbin in the temple, on the island south of the market.")
    input("press enter to begin")
    game_loop(world)
    