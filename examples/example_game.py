from pyzork.entities import Player
from pyzork.world import World
from pyzork.base import game_loop, QM

from .example_world import *
from .example_quest import *

if __name__ == '__main__':
    tavern.two_way_connect(Direction.south, market)
    market.two_way_connect(Direction.south, docks)
    docks.two_way_connect(Direction.east, island)
    island.two_way_connect(Direction.north, temple)
    # hidden.one_way_connect(Direction.west, temple)
    market.two_way_connect(Direction.west, alley)
    
    player = Player()
    world = World([tavern, market, island, temple, docks, hidden], player)
    QM.start_quest("KillBigGoblin")
    
    game_loop(world)
    