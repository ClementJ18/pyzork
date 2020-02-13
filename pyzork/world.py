from .enums import Direction
from .utils import get_user_input, post_output
from .base import qm
from .battle import Battle

from typing import Union


class Location:
    def __init__(self, **kwargs):
        self.coordinates = kwargs.get("coordinates", None)

        self.name = self.__doc__
        self.exits = self._generate_exits()
        self.discovered = False
        
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
            self.enter(from_location)
            self.discovered = True
        else:
            self.enter(from_location)

    def enter(self, from_location):
        pass
        
    def _exit(self, to_location):
        self.exit(to_location)

    def exit(self, to_location):
        pass
        
    def print_exits(self):
        for key, value in self.exits.items():
            if value is not None:
                post_output(f"- Go {key.name} to {value.name}")
                
    def print_interactions(self, world):
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

class Shop(Location):
    pass

class World:
    def __init__(self, locations, player):
        self.current_location = locations[0]
        self.locations = locations
        self.player = player
        
    def world_loop(self):
        self.current_location._enter(Location())
        self.current_location.print_exits()
        while True:
            qm.proccess_rewards(player, self)
            self.travel_parser()
        
    def travel(self, location : Union[Direction, Location]):
        if isinstance(location, Direction):
            location = self.directional_move(location)
            
        self.current_location._exit(location)
        location._enter(self.current_location)
        
        if location.enemies:
            battle = Battle(player, location.enemies, location)
            battle.battle_loop()
            
        location.print_exits()
        location.print_interactions()
        self.current_location = location
            
        
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
        choice = get_user_input().lower()
        direction = Direction[choice.split()[1]]
        self.legal_travel(direction)
        
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
  