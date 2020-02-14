from .enums import StatEnum

class Modifier:
    def __init__(self, **kwargs):
        self.type = kwargs.get("type", StatEnum.null)
        self.duration = kwargs.get("duration")

        self.name = self.__doc__ if self.__doc__ else self.__class__.__name__
        self.description = self.buff.__doc__
        
    def is_expired(self):
        return duration == 0
        
    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
            
        return self.name == other.name

    def calc(self, player):
        """This is normally the method that would have to be implemented by the user but because buffs are timed we use this 
        to check if they're still valid before calling the logic."""
        if self.duration != 0:
            return self.buff(player)

    def buff(self, player):
        """Abstract method to be implemented on a per buff basis to determine the stat change."""
        pass
        
    def effect(self, player):
        """Abstract method to be implemented for turn based effects."""
        pass

    def end_turn(self, player):
        """Method called at the end of the turn for each buff to show time passed and left until the buff expires. 
        Permanent buffs are set to -1"""
        if self.duration > 0:
            self.duration -= 1

        if self.duration == 0:
            return
            
        self.effect(player)
