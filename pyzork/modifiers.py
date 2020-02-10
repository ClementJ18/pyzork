from .enums import StatEnum

class Modifier:
    def __init__(self, **kwargs):
        self.type = kwargs.get("type", StatEnum.null)
        self.duration = kwargs.get("duration")

        self.name = self.__doc__
        self.description = self.buff.__doc__
        
    def is_expired(self):
        return duration == 0

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

class WarRoarBuff(Modifier):
    """War Roar of War"""
    def __init__(self):
        super().__init__(type=StatEnum.attack, duration=5)

    def buff(self, target):
        """You are entranced by the roar and your attack is increased for a short time"""
        return 2

class InsultDebuff(Modifier):
    """Insult"""
    def __init__(self):
        super().__init__(type=StatEnum.defense, duration=3)

    def buff(self, target):
        """You feel insulted and as a result the target's defense is lowered."""
        return -3

class InsultBuff(Modifier):
    """Insult"""
    def __init__(self):
        super().__init__(type=StatEnum.attack, duration=3)

    def buff(self, target):
        """You feel insulted and as a result the target's attack is increased."""
        return 1

class FireDebuff(Modifier):
    """Burnt"""

    def __init__(self):
        super().__init__(type=StatEnum.max_health, duration=5)

    def buff(self, target):
        """The burns leaves a scar, reducing the target's maximum health."""
        return -5

class PoisonEffect(Modifier):
    """Poison"""
    def __init__(self):
        super().__init__(duration=5)

    def effect(self, player):
        """Lose 3 health every turn."""
        self.player.health -= 3

class BurntEffect(Modifier):
    """Burnt"""

    def __init__(self):
        super().__init__(duration=5, type=StatEnum.attack)
        
    def buff(self, player):
        """The burn makes it hard to fight"""
        return -2

    def effect(self, player):
        """Lose 2 health every turn"""
        self.player.health -= 2
