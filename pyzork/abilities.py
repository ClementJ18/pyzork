from .modifiers import *
from .utils import post_output

class Ability:
    """Parent class for all abilities."""
    def __init__(self):
        self.name = self.__doc__
        self.description = self.effect.__doc__
        self.cost = self.costing.__doc__

    def cast(self, user, target = None):
        """Method that verifies if all conditions have been met."""
        if target is None:
            target = user

        if not self.costing(user, target):
            return False
        
        post_output(f"{user.name} casts {self.name} on {target.name}")
        return self.effect(target)

    def costing(self, player, target):
        """Abstract method that does the logic part of the cost. This allow for flexibility on how you want your cost system to work
        wether it rage or mana or whatever other custom cost system you may create your class with. This method must return true if
        the user has enough resource and false if it doesn't."""
        raise NotImplementedError

    def effect(self, target):
        """Method to be overwritten that handles the actuall effect of the spell."""
        raise NotImplementedError
    
    @classmethod
    def base_costing(cls, cost):
        def func(self, player, target):
            if callable(cost):
                int_cost = cost(player, target)
            else:
                int_cost = cost
                
            if player.can_cast(int_cost):
                player.energy -= int_cost
                return True

            return False
            
        return func
            
    @classmethod
    def add(cls, cost=0):
        def decorator(func):
            new_class = cls
            new_class.costing = cls.base_costing(cost)
            new_class.effect = func
            
            return new_class
            
        return decorator
