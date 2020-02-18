from .enums import StatEnum
from .entities import Entity

class Modifier:
    """Modifiers define changes to the stats of the entity they are attached to. They can do stuff like 
    increase the attack of an ally for 3 turns or deal poison damage to an enemy over 5 turns. You can
    stack as many different modifiers as you want on a single entity but you can never give an entity
    the same modifier twice. This is the default behavior for every entity but it can be overwritten.
    
    Parameters
    -----------
    duration : int
        How many "turns" a buff lasts. A turn is all the players and enemies present in the battle
        doing one action. This can be a positive int to demonstrate a temporary modifier which will
        expire after a certain number of turns or it can be -1 to represent a permanent buff which
        will only expire at the end of the battle.
    stat_type : Optional[StatEnum]
        An optional StatEnum that defines which stat this modifiers affect, this is only necessary
        if you have defined the `buff` method.
    name : Optional[str]
        An optional string to give a name to the modifier, if this is not provided, the library will
        fall back to the docstring of the class and if this isn't provided either it will fallback to
        the nameof the class
    description : Optional[str]
        An optional string to give a short (or long) description about the buff and its effects. If
        this is not provided the library will fall back to combining the docstring of the `buff`
        and `effect` method    
    """
    def __init__(self, **kwargs):
        self.type = kwargs.get("stat_type", StatEnum.null)
        self.duration = kwargs.get("duration")

        if "name" in kwargs:
            self.name = kwargs.get("name")
        else:
            self.name = self.__doc__ if self.__doc__ else self.__class__.__name__

        self.description = kwargs.get("description", f"{self.buff.__doc__} {self.effect.__doc__}")
        
    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
            
        return self.name == other.name
    
    def is_expired(self):
        """Simple method to check if is a buff is expired.
        
        Returns
        --------
        bool
            Whether or not the modifier is expired
        """
        return self.duration == 0

    def calc(self, entity : Entity):
        """This is normally the method that would have to be implemented by the user but because 
        buffs are timed we use this to check if they're still valid before calling the logic."""
        if not self.is_expired():
            return self.buff(entity)

    def buff(self, entity : Entity):
        """Method to implement to provide a stat buff to an entity. This method is called everytime
        the library calculates the stat that this modifier changes. There is no guarantee that this
        method will only be called once per turn so don't make any permanent changes to the player 
        such as restoring health or granting experience.
        
        Parameters
        -----------
        entity : Entity
            The entity this modifier is attached to.
        """
        pass
        
    def effect(self, entity : Entity):
        """Method to implement to do a once per turn change to an entity. This method is called
        exactly once per turn (given the buff is not expired) during the end turn phase. This is where
        you can do stuff like restore or take away health from the entity or make other permanent changes
        that the entity will carry on beyond this battle.
        
        Parameters
        -----------
        entity : Entity
            The entity this modifier is attached to.
        """
        pass

    def end_turn(self, entity : Entity):
        """Method called at the end of the turn for each buff to show time passed and left until the buff expires. 
        Permanent buffs are set to -1"""
        if self.duration > 0:
            self.duration -= 1

        if self.is_expired():
            return
            
        self.effect(entity)
        
    @classmethod
    def add_effect(cls, duration : int, **kwargs):
        """Decorator function to allow the user to define an effect by decorating a function. Takes the
        same parameters as the class. """        
        def decorator(func):
            new_class = type(func.__name__, (cls,), {
                "duration": duration, 
                "effect": func, 
                "name": kwargs.get("name", func.__name__),
                "description": kwargs.get("description", func.__doc__)
            })
            
            return new_class
            
        return decorator
        
    @classmethod
    def add_buff(cls, duration : int, stat_type : StatEnum, **kwargs):
        """Decorator function to allow the user to define a buff by decorating a function. Takes
        the same parameters as the class. Since this specifically adds a buff, the `stat_type` parameter
        is required"""
        def decorator(func):
            new_class = type(func.__name__, (cls,), {
                "duration": duration, 
                "stat_type": stat_type, 
                "buff": func,
                "name": kwargs.get("name", func.__name__),
                "description": kwargs.get("description", func.__doc__)
            })
            
            return new_class
            
        return decorator
