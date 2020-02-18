from .modifiers import *
from .utils import post_output

class Ability:
    """Parent class for all abilities."""
    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs.get("name")
        else:
            self.name = self.__doc__ if self.__doc__ else self.__class__.__name__

        self.description = kwargs.get("description", self.__init__.__doc__)
        
    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
            
        return self.name == other.name
        
    def __repr__(self):
        return f"<{self.__class__.__name__}>"

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
        if callable(self.cost):
            int_cost = self.cost(player, target)
        else:
            int_cost = self.cost
            
        if player.can_cast(int_cost):
            player.energy -= int_cost
            return True

        return False

    def effect(self, target):
        """Method to be overwritten that handles the actuall effect of the spell."""
        raise NotImplementedError
            
    @classmethod
    def add(cls, cost=0, **kwargs):
        def decorator(func):
            new_class = type(func.__name__, (cls,), {
                "cost": cost, 
                "effect": func,
                "name": kwargs.get("name", func.__name__),
                "description": kwargs.get("description", func.__doc__)
            })
            # new_class.__name__ = func.__name__
            # new_class.costing = cls.base_costing(cost)
            # new_class.effect = func
            
            return new_class
            
        return decorator
