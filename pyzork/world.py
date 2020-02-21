from .enums import Direction
from .utils import get_user_input, post_output
from .base import qm
from .battle import Battle

from typing import Union


class Location:
    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs.get("name")
        else:
            self.name = self.__doc__ if self.__doc__ else self.__class__.__name__

        self.description = kwargs.get("description", self.__init__.__doc__)
        
        self.exits = self._generate_exits()
        self.discovered = False
        self.npcs = kwargs.get("npcs", [])
        self.enemies = kwargs.get("enemies", [])
        
    def __str__(self):
        return f"<{self.name}>"

    def _generate_exits(self):
        return {key: None for key in Direction}

    def two_way_connect(self, direction : Direction, connected_location : "Location" = None):
        self.one_way_connect(direction, connected_location)
        connected_location.one_way_connect(Direction.opposite(direction), self)

    def one_way_connect(self, direction : Direction, connected_location : "Location" = None):
        self.exits[direction] = connected_location
        
    def _enter(self, from_location):
        if not self.discovered:
            qm.progress_quests("on_discover", self)
            return self.enter(from_location)
            self.discovered = True
        else:
            return self.enter(from_location)

    def enter(self, from_location):
        post_output(f"{self.name}\n\n{self.description}")
        
    def _exit(self, to_location):
        return self.exit(to_location)

    def exit(self, to_location):
        pass
        
    def print_interaction(self, world, direction):
        """Abstract method to give the user control over how the exit is actually printed if they wanna
        add some funky flair."""
        post_output(f"- Go {direction.key} to {self.name}")
        
    def print_exits(self, world):
        for direction, location in self.exits.items():
            if location is not None:
                location.print_interaction(world, direction)

    def print_npcs(self, world):
        for npc in self.npcs:
            npc.print_interaction(world)
                
    def print_pickups(self, world):
        for item in self.items:
            item.print_interaction(world)
        
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
    pass

class World:
    def __init__(self, locations, player, **kwargs):
        self.current_location = locations[0]
        self.locations = locations
        self.player = player
        self.end_game = kwargs.get("end_game", self.end_game)
        self.error_handler = kwargs.get("error_handler", self.error_handler)
        
        self.player.set_world(self)
        
    def world_loop(self):
        self.current_location._enter(Location())
        while True:
            qm.proccess_rewards(self.player, self)
            self.current_location.print_exits(self)
            self.current_location.print_interactions(self)
            self.travel_parser()
        
    def travel(self, new_location : Union[Direction, Location]):
        old_location = self.current_location
        if isinstance(new_location, Direction):
            new_location = self.directional_move(new_location)
        
        self.current_location = new_location
        can_exit = old_location._exit(new_location)
        can_enter = new_location._enter(old_location)
        if can_exit is False or can_enter is False:
            self.current_location = old_location
            return
        
        if new_location.enemies:
            self.initiate_battle(new_location.enemies)

        # new_location.print_exits(self)
        # new_location.print_interactions(self)
        
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
        
    def better_travel_parser(self):
        keywords = ["go", "walk", "move", "run", "enter", "exit"]
        possible_actions = [actions.SystemMove, actions.SystemItem, actions.SystemEquipment]
        choice = get_user_input().lower()
        
        if not any(x in choice for x in self.keywords):
            return
            
        #destination
        for exit in self.current_location.exits:
            pass
            
        if len(self.current_location.exits) == 1:
            exit = list(self.current_location.exits.values())[0]
            return self.travel(exit)
            
    def end_game(self, e):
        post_output(e)
        
    def error_handler(self, e):
        raise e
  