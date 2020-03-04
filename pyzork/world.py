from .enums import Direction
from .utils import get_user_input, post_output
from .base import QM
from .battle import Battle
from .actions import *

from typing import Union

class Location:
    """A location represents a place in which the player exists while out of combat, this is where players
    usually go about their normal tasks of discovering things and such. A location can be of any scale, it
    could be a room or individual corners of the room or it could be an entire country, you can design 
    as you wish. 
    
    Parameters
    -----------
    name : Optional[str]
        The name of the location, if this is not provided then the library will fall back to the 
        docstring of the class and then to the class name itself
    description : Optional[str]
        A description of the location, if none is provided it will default to the __init__ docstring.
    npcs : Optional[List[Entity]]
        Optional list of entities with which the player can interact
    enemies : Optional[List[Enemy]]
        Optional list of enemies against which the player will fight when they enter the location
    
    Attributes
    -----------
    name : str
        The name of the location
    description : Optional[str]
        The description of the location, which gets printed when the user enters it if the `enter`
        method is not overriden.
    npcs : List[Entity]
        List of npcs that can be interacted with
    enemies : List[Enemy]
        List of enemies the user will battle when entering the first time
    visited : int
        How many times the user has visited this place
    """
    def __init__(self, **kwargs):
        if not hasattr(self, "name"):
            if "name" in kwargs:
                self.name = kwargs.get("name")
            else:
                self.name = self.__doc__ if self.__doc__ else self.__class__.__name__
        
        if "description" in kwargs:
            self.description = kwargs.get("description", self.__init__.__doc__)
        
        self.exits = self._generate_exits()
        self.visited = 0
        
        if not hasattr(self, "npcs"):
            self.npcs = kwargs.pop("npcs", [])
            
        if not hasattr(self, "enemies"):
            self.enemies = kwargs.get("enemies", [])
            
        self.npcs = [npc() for npc in self.npcs]
        self.enemies = [enemy() for enemy in self.enemies]
        
    def __repr__(self):
        return f"<{self.name} npcs={len(self.npcs)} enemies={len(self.enemies)}>"
        
    def __str__(self):
        return self.name

    def _generate_exits(self):
        return {key: None for key in Direction}

    def two_way_connect(self, direction : Direction, connected_location : "Location" = None):
        """Connect this Location with the `connected_location` in a way that the connected location
        can be reached by going in the `direction`. If no location is provided then the connection in
        that direction will be broken in both ways. The two way connections means that the player
        will also be able to go from the `connection_location` to this location in the opposite way.
        
        Parameters
        -----------
        direction : Direction
            The direction of the exit you wish to edit
        connected_location : Optiona[Location]
            The location you want to make the connection to, if none are provided then it will
            break off any existing connection both ways
        """
        if connected_location is None:
            try:
                opposite = Direction.opposite(direction)
                self.exits[direction].one_way_connect(opposite)
            except AttributeError:
                pass
        else:
            connected_location.one_way_connect(Direction.opposite(direction), self)
            
        self.one_way_connect(direction, connected_location)

    def one_way_connect(self, direction : Direction, connected_location : "Location" = None):
        """Create or remove a one way connection to `connected_location`. This means that going in `direction`
        will take the use to `connected_location`. If no `connected_location` is provided then it will remove
        any exit for this location in that direction, all other connections remain intact.
        
        Parameters
        -----------
        direction : Direction
            The direction of the exit you wish to edit
        connected_location : Optional[Location]
            The location you want to connect this one to, if none are provided then it will
            break of any existing connection.
        """
        self.exits[direction] = connected_location
        
    def _enter(self, player : "Player", from_location : "Location"):
        if not self.visited:
            QM.progress_quests("on_discover", self)
            
        can_enter = self.enter(player, from_location)
        self.visited += 0
        return can_enter

    def enter(self, player : "Player", from_location : "Location") -> "Optional[bool]":
        """Method to be overwritten by the user to create a custom behavior when the player enters
        this location. By default simply prints the name and description.
        
        Parameters
        -----------
        player : Player
            The player instance entering the location
        from_location : Location
            The location the player is coming from
            
        Returns
        --------
        Optional[Bool]
            If the method returns False then the move will be cancelled and the player will be
            sent back to `from_location`
        """
        post_output(f"{self.name}\n\n{self.description}")
        
    def _exit(self, player : "Player", to_location : "Location"):
        return self.exit(player, to_location)

    def exit(self, player : "Player", to_location : "Location") -> "Optional[bool]":
        """Method to be overwritten by the user to create a custom behavior when the player exits
        this location. Does nothing by default.
        
        Parameters
        -----------
        player : Player
            The player instance leaving the location
        to_location : Location
            The location the player is going to
            
        Returns
        --------
        Optional[Bool]
            If the method returns False then the move will be cancelled and the player will remain
            in this current location.
        """
        pass
        
    def print_interaction(self, world : "World", direction : "Direction"):
        """Method called to print a flavor text related to reaching this location from another location.
        Prints the direction and name of the location by default 
        
        Parameters
        -----------
        world : World
            The world the location is in
        direction : Direction
            The direction the location is in compared to the `world.current_location`
        """
        post_output(f"- Go {direction.name} to {self.name}")
        
    def print_exits(self, world : "World"):
        """Print all the exits for this location"""
        for direction, location in self.exits.items():
            if location is not None:
                location.print_interaction(world, direction)

    def print_npcs(self, world : "World"):
        """Print all the npc interactions for this location"""
        for npc in self.npcs:
            npc.print_interaction(world)
        
    def can_move_to(self, location : Union[Direction, "Location"]) -> bool:
        """Boolean check if the player can travel in this direction or location
        
        Parameters
        ----------
        location : Union[Direction, Location]
            The location/direction to check
            
        Returns
        --------
        bool
            True if you can travel that way, else False
        """
        if isinstance(location, Direction):
            return self.exits[location] is not None
            
        if location is None:
            return False
            
        return location in self.exits.values()
        
    def directional_move(self, direction : Direction) -> "Location":
        """Returns the location of of the exit in this direction
        
        Parameters
        -----------
        direction : Direction
            The direction to check
            
        Returns
        --------
        Optional[Location]
            The location or None
        """
        return self.exits[direction]
        
    def update_alive(self):
        """remove all the dead stuff"""
        self.npcs = [x for x in self.npcs if x.is_alive()]
        self.enemies = [x for x in self.enemies if x.is_alive()]
        
    @classmethod
    def from_dict(cls, **kwargs):
        """Create a Location from a set of kwargs, takes the same parameters as the class
        and returns a subclass of it by the same name. If you add npcs and enemies through this you must
        pass the classes themselves and not the instances."""
        new_class = type(kwargs.get("name"), (cls,), kwargs)
        return new_class

class Shop(Location):
    """Shops are special locations where the only interactions that can be performed are related to buying 
    and selling items. You can only buy and sell items which are registed in the shop, you cannot sell an item
    which is not registered in the shop, as this allows for dynamic pricing accross shops.
    
    Parameters
    -----------
    items : List[ShopItem]
        List of items for sale
    resell : Optional[float]
        The value of an item when being sold to the shop, percentage of the initial value, 1 by default.
        If this is set for zero then resale is disabled for this shop.
    name : str
        Name of the shop
    description : Optional[str]
        Optional description of the shop
    
    Attributes
    -----------
    name : str
        The name of the shop
    description : Optional[str]
        The description of the shop, which gets printed when the user enters it if the :method:enter
        is not overriden.
    items : List[ShopItem]
        The list of items that can be bought or sold
    resell : float
        The multipler applied on the original price to get the resale value of an item.
    """
    def __init__(self, **kwargs):
        if not hasattr(self, "items"):
            self.items = kwargs.get("items", [])
        
        if not hasattr(self, "resell"):
            self.resell = kwargs.get("resell", 1)
            
        if not hasattr(self, "name"):
            self.name = kwargs.get("name")
            
        if not hasattr(self, "description"):
            self.description = kwargs.get("description")
            
        super().__init__(**kwargs)
        
    def _enter(self, player : "Player", from_location : "Location") -> False:
        if not self.visited:
            QM.progress_quests("on_discover", self)
            
        self.enter(player, from_location)
        self.visited += 0
        self.shop_loop(player)
        return False
    
    def print_interaction(self, world : "World", direction : "Direction"):
        """Method called to print a flavor text related to reaching this shop from another location.
        
        Parameters
        -----------
        world : World
            The world the location is in
        direction : Direction
            The direction the location is in compared to the `world.current_location`
        """
        post_output(f"- Go {direction.name} to shop")
        
    def print_items(self, player : "Player"):
        """Print all the items for sale in this shop on the money of the player."""
        post_output(f"You have {player.money}")
        for item in self.items:
            post_output(f"- {item.item.name} ({item.amount}): {item.price} coins - {item.item.description}")
        
    def shop_loop(self, player : "Player"):
        """The heart of the shop system, this allows the player to buy, sell, exit the shop, view his
        stats/inventory and use/equip items."""
        self.print_items(player)
        while True:
            choice = get_user_input()
            intent, item = shop_parser(choice, self)
            if intent == "exit":
                return False
            
            if intent == "buy":
                item = self.items[int(choice[1])]
                item.buy(player)
            elif intent == "sell":
                if self.resell == 0:
                    return post_output("You cannot sell items in this shop")
                item = self.items[int(choice[1])]
                item.sell(player, self.resell)
            elif view := view_parser(choice, player):
                hasattr(player, f"print_{view}")()
            elif item := equip_item_parser(choice, player):
                player.inventory.equip_item(item)
            elif item := use_item_parser(choice, player):
                player.inventory.use_item(item)

    @classmethod
    def from_dict(cls, **kwargs):
        """Allows you to create a shop from kwargs, takes the same parameters as the class."""
        name = kwargs.get("name", "AShop")
        new_class = type(name, (cls,), {
                "name": name,
                "description": kwargs.get("description"),
                "resell": kwargs.get("resell", 1),
                "items": kwargs.get("items", [])
            })
        
        return new_class

class World:
    """The world is the class that englobes everything, this is where your adventure lives and happens.
    You don't need to subclass this class, only call it and pass it to the `game_loop`
    
    Parameters
    -----------
    locations : List[Location]
        A list of all the location in this world
    player : Player
        The player of this world
    start : Optional[Location]
        The place where the player starts, by default it is the first Location in locations
    end_game : Optional[Callable[[EndGame], None]]
        Optional method for handling what happens when the game is finished, could be
        either because the player has won, died or many other possible reasons.
    error_handler : Optional[Callable[[Exception], None]]
        Optional method to handle other errors in case any arise.
        
    Attributes
    -----------
    current_location : Location
        The location the Player is currently in
    player : Player
        The player of this world
    locations : List[Location]
        A list of location instances representing all possible locations in the world
    """
    def __init__(self, **kwargs):
        self.locations = kwargs.pop("locations")
        self.current_location = kwargs.pop("start", self.locations[0])
        self.player = kwargs.pop("player")
        self.end_game = kwargs.pop("end_game", self.end_game)
        self.error_handler = kwargs.pop("error_handler", self.error_handler)
        
        self.player.set_world(self)
        
    def world_loop(self):
        """Handler for traveling around the world. This method calls end turn so modifiers and effects
        will expire while the user travels in the world. Unless you're doing some advanced stuff with the
        library such as handling the game loop on your own you shouldn't need to call this."""
        self.current_location._enter(self.player, Location())
        while True:
            QM.proccess_rewards(self.player, self)
            self.current_location.print_exits(self)
            self.current_location.print_npcs(self)
            self.print_menu()
            self.travel_parser()
            self.end_turn()
            
    def print_menu(self):
        """Prints the context menu that is available everywhere, this is only visual."""
        post_output("- View inventory")
        post_output("- View stats")
            
    def end_turn(self):
        """Decrement the duration of all player modifiers by 1"""
        self.player.end_turn()
        
    def travel(self, new_location : Location):
        """Travel in a to a location regadless of if it is a "legal" move, this instantly transports
        the player to the target location and initatie battle if any enemies are present.
        
        Parameters
        -----------
        new_location : Location
            The location to travel to, this does not have to be connected to the current location.
        """
        old_location = self.current_location
        self.current_location = new_location
        can_exit = old_location._exit(self.player, new_location)
        can_enter = new_location._enter(self.player, old_location)
        if can_exit is False or can_enter is False:
            self.current_location = old_location
            return
        
        if new_location.enemies:
            self.initiate_battle(new_location.enemies)
        
    def initiate_battle(self, enemies : "List[Enemy]"):
        """Start a battle and the battle loop between the player of this world and a list of enemies. If
        you want to inject your own battle class. This method must start the battle, this is usually done
        through the Battle.battle_loop method
        
        Parameters
        -----------
        enemies : List[Enemy]
            List of enemies to fight
        """
        battle = Battle(self.player, enemies, self.current_location)
        battle.battle_loop()
            
    def can_move(self, location : "Union[Direction, Location]") -> bool:
        """Check if the player can move from their current location in that direction/location
        
        Parameters
        -----------
        location : Union[Direction, Location]
            The direction/location 
            
        Returns
        --------
        bool
            True if the player can move there
        """
        if isinstance(location, Direction):
            location = self.directional_move(location)
            
        return self.current_location.can_move_to(location)
        
    def legal_travel(self, location : Location):
        """Attempt a travel move, compared to simply World.travel this checks if the player can
        move to this location from their current location and move there if they can.
        
        Parameters
        -----------
        location : Location
            The location to attept moving too    
        """
        if self.can_move(location):
            self.travel(location)
        else:
            post_output("You cannot move there")
        
    def directional_move(self, direction : Direction) -> "Optional[Location]":
        """Convert a direction into a location, if it exists, else return None
        
        Parameters
        -----------
        direction : Direction
            The direction you want to move in
            
        Returns
        --------
        Optional[Location]
            The location that is in that direction
        """
        return self.current_location.directional_move(direction)
            
    def travel_parser(self):
        """Gets the user input and check if it matches against a set of parsers using python's
        new walrus operator."""
        choice = clean(get_user_input().lower())
        if direction := direction_parser(choice, self.current_location):
            location = self.directional_move(direction)
            self.legal_travel(location)
        elif npc := interact_parser(choice, self.current_location):
            npc.interact(self)
        elif view := view_parser(choice, self.player):
            hasattr(self.player, f"print_{view}")()
        elif item := equip_item_parser(choice, self.player):
            self.player.inventory.equip_item(item)
        elif item := use_item_parser(choice, self.player):
            self.player.inventory.use_item(item)
            
    def end_game(self, e : "EndGame"):
        """Method to be overwritten either through subclassing or by passing it as a parameters
        when instancing the world. Is called when an Endgame exception is raised. Signifying the player
        has either died or won.
        
        Parameters
        -----------
        e : EndGame
            The endgame error that caused this
        """
        post_output(e)
        
    def error_handler(self, e : Exception):
        """Error handler for all other errors, can be used to either restart the loop or kill the game.
        Can be overriden by either subclassing or by passing it as a parameter when instancing the world.
        
        Parameters
        ------------
        e : Exception
            the error that was caught
        """
        raise e
  