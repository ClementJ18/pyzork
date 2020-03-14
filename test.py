import pyzork
from pyzork.utils import game_loop

#All the code that gets called before your adventure start should go here
def intro():
    pass
    
PLAYER = pyzork.Player(max_health=50, damage=3, defense=1)
Goblin = pyzork.NPC.from_dict(name="Goblin", max_health=10, damage=2)

Tavern = pyzork.Location.from_dict(name="Tavern of the Prancing Pony", description="A lovely little tavern")
tavern = Tavern(enemies=[Goblin])

START = tavern
LOCATIONS = [tavern]

WORLD = pyzork.World(locations=LOCATIONS, player=PLAYER, start=START)

if __name__ == '__main__':
    intro()
    game_loop(WORLD)