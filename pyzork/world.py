from .enums import Direction
from .utils import get_user_input, post_output
from .base import QM
from .battle import Battle
from .actions import *

from typing import Union

class Location:
    def __init__(self, **kwargs):
        if not getattr(self, "name", False):
            if "name" in kwargs:
                self.name = kwargs.get("name")
            else:
                self.name = self.__doc__ if self.__doc__ else self.__class__.__name__
        
        if "description" in kwargs:
            self.description = kwargs.get("description", self.__init__.__doc__)
        
        self.exits = self._generate_exits()
        self.discovered = False
        
        if not getattr(self, "npcs", False):
            self.npcs = kwargs.pop("npcs", [])
            
        if not getattr(self, "enemies", False):
            self.enemies = kwargs.get("enemies", [])
            
        self.npcs = [npc() for npc in self.npcs]
        self.enemies = [enemy() for enemy in self.enemies]
        
    def __repr__(self):
        return f"<{self.name}>"

    def _generate_exits(self):
        return {key: None for key in Direction}

    def two_way_connect(self, direction : Direction, connected_location : "Location" = None):
        self.one_way_connect(direction, connected_location)
        connected_location.one_way_connect(Direction.opposite(direction), self)

    def one_way_connect(self, direction : Direction, connected_location : "Location" = None):
        self.exits[direction] = connected_location
        
    def _enter(self, player, from_location):
        if not self.discovered:
            QM.progress_quests("on_discover", self)
            can_enter = self.enter(player, from_location)
            self.discovered = True
            return can_enter
        else:
            return self.enter(player, from_location)

    def enter(self, player, from_location):
        post_output(f"{self.name}\n\n{self.description}")
        
    def _exit(self, player, to_location):
        return self.exit(player, to_location)

    def exit(self, player, to_location):
        pass
        
    def print_interaction(self, world, direction):
        """Abstract method to give the user control over how the exit is actually printed if they wanna
        add some funky flair."""
        post_output(f"- Go {direction.name} to {self.name}")
        
    def print_exits(self, world):
        for direction, location in self.exits.items():
            if location is not None:
                location.print_interaction(world, direction)

    def print_npcs(self, world):
        for npc in self.npcs:
            npc.print_interaction(world)
        
    def can_move_to(self, location : Union[Direction, "Location"]):
        if isinstance(location, Direction):
            return self.exits[location] is not None
            
        if location is None:
            return False
            
        return location in self.exits.values()
        
    def directional_move(self, direction : Direction):
        return self.exits[direction]
        
    def update_alive(self):
        self.npcs = [x for x in self.npcs if x.is_alive()]
        self.enemies = [x for x in self.enemies if x.is_alive()]
        
    @classmethod
    def from_dict(cls, **kwargs):
        new_class = type(kwargs.get("name"), (cls,), kwargs)
        return new_class

class Shop(Location):
    def __init__(self, **kwargs):
        if not getattr(self, "items", False):
            self.items = kwargs.get("items", [])
        
        if not getattr(self, "resell", False):
            self.resell = kwargs.get("resell", 1)
            
        if not getattr(self, "name", False):
            self.name = kwargs.get("name")
            
        if not getattr(self, "description", False):
            self.description = kwargs.get("description")
            
        super().__init__(**kwargs)
        
    def _enter(self, player, from_location):
        if not self.discovered:
            QM.progress_quests("on_discover", self)
            self.enter(player, from_location)
            self.discovered = True
        else:
            self.enter(player, from_location)
            
        self.shop_loop(player)
        return False
    
    def print_interaction(self, world, direction):
        post_output(f"- Go {direction.name} to shop")
        
    def print_items(self, player):
        for item in self.items:
            post_output(f"- {item.item.name}: {item.item.description}")
        
    def shop_parser(self, player):
        choice = get_user_input().lower().split()
        if choice[0] == "exit":
            return False
        elif choice[0] == "buy":
            item = self.items[int(choice[1])]
            item.buy(player)
        elif choice[0] == "sell":
            item = self.items[int(choice[1])]
            item.sell(player, self.resell)
        
    def shop_loop(self, player):
        while True:
            self.print_items(player)
            cont = self.shop_parser(player)
            if cont is False:
                return
    
    @classmethod
    def from_dict(cls, **kwargs):
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
        self.current_location = locations[0]
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
            self.better_travel_parser()
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
        choice = get_user_input().lower().split()
        if choice[0] == "go":
            direction = Direction[choice[1]]
            self.legal_travel(direction)
        elif choice[0] == "interact":
            npc = self.current_location.npcs[int(choice[1])]
            npc.interact(self)
        elif choice[0] == "view":
            if choice[1] == "stats":
                self.player.print_stats()
            elif choice[1] == "inventory":
                self.player.print_inventory()
        elif choice[0] == "equip":
            t = self.player.inventory.get_equipment(int(choice[1]))
            self.player.inventory.equip_item(t)
        elif choice[0] == "use":
            t = self.player.inventory.get_consumable([int(choice[1])])
            self.player.inventory.use_item(t)
            
    def better_travel_parser(self):
        choice = clean(get_user_input().lower())
        if direction := direction_parser(choice, self):
            self.legal_travel(direction)
        elif npc := interact_parser(choice, self.current_location):
            npc.interact(self)
        elif view := view_parser(choice, self.player):
            gettattr(self.player, f"print_{view}")()
        elif item := equip_item_parser(choice, self.player):
            self.player.inventory.equip_item(item)
        elif item := use_item_parser(choice, self.player):
            self.player.inventory.use_item(item)
            
    def end_game(self, e):
        post_output(e)
        
    def error_handler(self, e):
        raise e
  