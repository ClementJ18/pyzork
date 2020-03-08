from pyzork import World, Player

#All the code that gets called before your adventure start should go here
def intro():
    pass
    
PLAYER = Player()

LOCATIONS = []

WORLD = World(locations=LOCATIONS, player=PLAYER)
