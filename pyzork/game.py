from pyzork import World, Player
from pyzork.utils import game_loop

#All the code that gets called before your adventure start should go here
def intro():
    pass
    
PLAYER = Player()

LOCATIONS = []

WORLD = World(locations=LOCATIONS, player=PLAYER)

if __name__ == '__main__':
    intro()
    game_loop(WORLD)
