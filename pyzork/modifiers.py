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
        and `effect` method.
       
    """
    def __init__(self, **kwargs):
        if not getattr(self, "stat_type", False):
            self.stat_type = kwargs.pop("stat_type", StatEnum.null)
        
        if not getattr(self, "duration", False):
            self.duration = kwargs.pop("duration")

        if not getattr(self, "name", False):
            if "name" in kwargs:
                self.name = kwargs.pop("name")
            else:
                self.name = self.__doc__ if self.__doc__ else self.__class__.__name__
        
        if not getattr(self, "description", False):
            self.description = kwargs.pop("description", f"{self.buff.__doc__} {self.effect.__doc__}")
        
    def __hash__(self):
        return hash(self.__class__.__name__)
        
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
            
        return self.__class__.__name__ == other.__class__.__name__
        
    def __repr__(self):
        return f"<{self.name} duration={self.duration} stat={self.stat_type.name}>"
        
    def __str__(self):
        return self.name
    
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
    def add_effect(cls, **kwargs):
        """Decorator function to allow the user to define an effect by decorating a function. Takes the
        same parameters as the class. """        
        def decorator(func):
            if not cls is Modifier:
                cls.effect = func
                return func
            else:
                new_class = type(func.__name__, (cls,), {
                    "duration": kwargs.pop("duration"), 
                    "effect": func, 
                    "name": kwargs.pop("name", func.__name__),
                    "description": kwargs.pop("description", func.__doc__)
                })
                
                return new_class
            
        return decorator
        
    @classmethod
    def add_buff(cls, **kwargs):
        """Decorator function to allow the user to define a buff by decorating a function. Takes
        the same parameters as the class. Since this specifically adds a buff, the `stat_type` parameter
        is required"""
        def decorator(func):
            if not cls is Modifier:
                cls.buff = func
                cls.stat_type = kwargs.pop("stat_type")
                return func
            else:
                new_class = type(func.__name__, (cls,), {
                    "duration": kwargs.pop("duration"), 
                    "stat_type": kwargs.pop("stat_type"), 
                    "buff": func,
                    "name": kwargs.pop("name", func.__name__),
                    "description": kwargs.pop("description", func.__doc__)
                })
                
                return new_class
        
        return decorator
