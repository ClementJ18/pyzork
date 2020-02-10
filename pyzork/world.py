from .enums import Direction
from .utils import get_user_input, post_output

from typing import Union


class Location:
    def __init__(self, **kwargs):
        self.coordinates = kwargs.get("coordinates", None)

        self.name = self.__doc__
        self.exits = self._generate_exits()
        
    def __str__(self):
        return f"<{self.name}>"

    def _generate_exits(self):
        return {key: None for key in Direction}

    def two_way_connect(self, direction : Direction, connected_location : "Location" = None):
        self.one_way_connect(direction, connected_location)
        connected_location.one_way_connect(Direction.opposite(direction), self)

    def one_way_connect(self, direction : Direction, connected_location : "Location" = None):
        self.exits[direction] = connected_location

    def enter(self):
        pass

    def exit(self):
        pass
        
    def print_exits(self):
        for key, value in self.exits.items():
            if value is not None:
                print(f"Go {key.name} to {value.name}")
        
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
    def __init__(self, locations):
        self._current_location = locations[0]
        self.locations = locations
        
    @property
    def current_location(self):
        return self._current_location
    
    @current_location.setter
    def current_location(self, value):
        # self._current_location.exit()
        self._current_location = value
        # value.enter()
        # value.print_exits()
        
    def game_loop(self):
        while True:
            self.travel_parser()
        
    def travel(self, location : Union[Direction, Location]):
        if isinstance(location, Direction):
            location = self.directional_move(location)
            
        self.current_location.exit()
        self.current_location = location
        location.enter()
        location.print_exits()
        
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
  