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
        The description of the location, which gets printed when the user enters it if the :method:enter
        is not overriden.
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
        
    def _enter(self, player, from_location):
        if not self.visited:
            QM.progress_quests("on_discover", self)
            
        self.enter(player, from_location)
        self.visited += 0
        self.shop_loop(player)
        return False
    
    def print_interaction(self, world, direction):
        post_output(f"- Go {direction.name} to shop")
        
    def print_items(self, player):
        post_output(f"You have {player.money}")
        for item in self.items:
            post_output(f"- {item.item.name}: {item.price} coins - {item.item.description}")
        
    def shop_loop(self, player):
        while True:
            self.print_items(player)
            choice = get_user_input()
            intent, item = shop_parser(choice, self)
            if intent == "exit":
                return False
            
            if intent == "buy":
                item = self.items[int(choice[1])]
                item.buy(player)
            elif intent == "sell":
                item = self.items[int(choice[1])]
                item.sell(player, self.resell)
    
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
    def __init__(self, locations, player, **kwargs):
        self.current_location = kwargs.get("start", locations[0])
        self.locations = locations
        self.player = player
        self.end_game = kwargs.get("end_game", self.end_game)
        self.error_handler = kwargs.get("error_handler", self.error_handler)
        
        self.player.set_world(self)
        
    def world_loop(self):
        self.current_location._enter(self.player, Location())
        while True:
            QM.proccess_rewards(self.player, self)
            self.current_location.print_exits(self)
            self.current_location.print_npcs(self)
            self.print_menu()
            self.travel_parser()
            self.end_turn()
            
    def print_menu(self):
        post_output("- View inventory")
        post_output("- View stats")
            
    def end_turn(self):
        self.player.end_turn()
        
    def travel(self, new_location : Union[Direction, Location]):
        old_location = self.current_location
        if isinstance(new_location, Direction):
            new_location = self.directional_move(new_location)
        
        self.current_location = new_location
        can_exit = old_location._exit(self.player, new_location)
        can_enter = new_location._enter(self.player, old_location)
        if can_exit is False or can_enter is False:
            self.current_location = old_location
            return
        
        if new_location.enemies:
            self.initiate_battle(new_location.enemies)
        
    def initiate_battle(self, enemies):
        battle = Battle(self.player, enemies, self.current_location)
        battle.battle_loop()
            
    def can_move(self, location : Union[Direction, Location]):
        if isinstance(location, Direction):
            location = self.directional_move(location)
            
        return self.current_location.can_move_to(location)
        
    def legal_travel(self, location : Union[Direction, Location]):
        if self.can_move(location):
            self.travel(location)
        else:
            post_output("You cannot move there")
        
    def directional_move(self, direction : Direction):
        return self.current_location.directional_move(direction)
            
    def travel_parser(self):
        choice = clean(get_user_input().lower())
        if direction := direction_parser(choice, self.current_location):
            self.legal_travel(direction)
        elif npc := interact_parser(choice, self.current_location):
            npc.interact(self)
        elif view := view_parser(choice, self.player):
            hasattr(self.player, f"print_{view}")()
        elif item := equip_item_parser(choice, self.player):
            self.player.inventory.equip_item(item)
        elif item := use_item_parser(choice, self.player):
            self.player.inventory.use_item(item)
            
    def end_game(self, e):
        post_output(e)
        
    def error_handler(self, e):
        raise e
  