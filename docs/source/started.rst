..currentmodule::pyzork

Getting Started
================
First step to using this library is installing it, for it you can simply use pip and the following command::

    pip install pyzork

Once you have the library installed you can get started coding in any directory, here's some boilerplate code to get you started, just copy paste this into a new file:: 

    import pyzork
    from pyzork.utils import game_loop

    #All the code that gets called before your adventure start should go here
    def intro():
        pass
        
    PLAYER = pyzork.Player()

    LOCATIONS = []
    
    START = None

    WORLD = pyzork.World(locations=LOCATIONS, player=PLAYER, start=START)

    if __name__ == '__main__':
        intro()
        game_loop(WORLD)

This code creates a empty Player and an empty world, based on that you can then modify the classes to suit your needs. Your first step should be to create some locations so that your player actually has places to run around, for more information on head down to the :doc:`World <world>` documentation. Here's an easy example, just a little tavern that provides some DnD mood to your adventure:: 

    Tavern = pyzork.Location.from_dict(name="Tavern of the Prancing Pony", description="A lovely little tavern")
    tavern = Tavern()
    
    START = tavern
    LOCATIONS = [tavern]

Now your player has a location to start in, but not much to do in it, but that's fine, let's add an enemy for them to fight, oh and let's not forget to add some actual stats to the player:: 
    
    PLAYER = pyzork.Player(max_health=50, damage=3, defense=1)
    Goblin = pyzork.NPC.from_dict(name="Goblin", max_health=10, damage=2)
    
    tavern = Tavern(enemies=Goblin())

Now when the player starts the game they'll be met by a goblin they'll need to battle before they get move on to the next step. For the final bit of this tutorial section let's just add a second location the player can go to once they're done fighting the Goblin::
    
    MarketPlace = pyzork.Location.from_dict(name="Marketplace", description="A nice markerplace")
    market = MarketPlace()
    
    tavern.two_way_connect(pyzork.Direction.south, market)
    
    LOCATIONS = [tavern, market]

Now, once the goblin is dead the player can move south to the Market.
