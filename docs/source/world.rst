.. currentmodule:: pyzork.world

World
======

The world is where your adventure lives, this is the root of you entire story and where all the events happen. To create the basis of a World you use and subclass the two classes described bellow:

.. autoclass:: pyzork.world.Location
    :members: one_way_connect, two_way_connect, enter, exit, print_interaction, can_move_to, directional_move, from_dict, print_exits, print_npcs, 

.. autoclass:: pyzork.world.Shop
    :members:
    :inherited-members:


.. autoclass:: pyzork.world.World
    :members:

Examples
----------

Basic Location
###############
The most basic form of a location is one created which only has a name, description, list of npcs and list of enemies. This kind of locations use the default behaviour of the parent class:: 

    from pyzork import Location
    
    from my_adventure.enemies import Goblin
    from my_adventure.npcs import OldMan, Table
    
    MarketPlace = Location.from_dict(
        name="Market Place", 
        description="This is a nice market"
        npcs=[OldMan, Table], 
        enemies=[Goblin]
    )

Here we see a basic example, of a markeplace with a Goblin as an enemy as a table and old man that can be interacted with. NOTE: As you can notice, the parameters being passed to npcs and enemies are list of CLASSES not instances, this is key to avoid all instances of that location having the same instance.

Sublcassed Location
######################
A more complex example, giving more flexibility, and a chanc to overwrite any methods you desire to add in your own::

    from pyzork import Location
    
    from my_adventure.locations import Docks
    
    class Island(Location):
    """A Small Island"""
    def enter(self, player, from_location):
        post_output(self.name)
        if isinstance(from_location, Docks):
            post_output("\n\nYou beach your boat on the sand")
        else:
            post_output("\n\nYou arrive on a beach")
            
    def exit(self, player, to_location):
        post_output(self.name)
        if isinstance(to_location, Docks):
            post_output("\n\nYou take the boat back to the docks")
        else:
            post_output("\n\nYou leave the beach")

In this example we ovveride the enter and exit method to print different message based on where the player is coming from. Logically if they're going to the docks from the island you can't just walk there, you take a boat. Therefore, overwriting these methods allow you to add some flair to your game, with different messages based on where the user is coming from.

Shop Example
##############
Shop are special locations where the player buys and sells items, allowing them to make money or buy powerful weapons. Making a shop is very simple, you don't need to subclass anything to make your own version of a shop, you can easily pass the required argument to Shop.from_dict, like so::

    from pyzork import Shop
    
    MarketShop = Shop.from_dict(
        resell=0.25,
        name="A Big Shop",
        items=[
            ShopItem(item=Sword, price=25, amount=1), 
            ShopItem(item=HealthPotion, amount=5, price=10),
            ShopItem(item=HealingOnguent, amount=3, price=5),
            ShopItem(item=SwordAndShield, price=30)
        ]
    )

This shop is called "A Big Shop", sells swords, healing potions, healing onguents. It also sells sword and shield combos but since it starts with an amount of zero it won't sell any till the player sells some the shop first. Items sold to the shop are taken at a quarter of their original value.

World Example
##############
So how it come all together? How do you take all the creations you made and group them up into a single world? Here's a basic example, regrouping the class we created in previous examples::

    from pyzork import Player, World, Direction
    
    from my_adventure.locations import MarketShop, Island, Docks, MarketPlace
    
    shop = MarketShop()
    island = Island()
    docks = Docks()
    market = MarketPlace()
    
    market.two_way_connect(Direction.east, docks)
    market.two_way_connect(Direction.north, shop)
    docks.two_way_connect(Direction.east, island)
    
    player = Player()
    
    world = World(locations=[shop, island, docks, market], start=market, player=player)

Using the module's visualisation function we can see that this is what our world looks like:

.. image:: https://github.com/ClementJ18/pyzork/blob/master/examples/example_world.png
