from enums import StatEnum

class Buff:
    """Parent class for all the buffs of this game. Buffs are stat modifiers that can be stack indefinitely unlike equipments
    that need a limb to attach to but that are time and will expire after a certain number of turns. All buffs need to inherit
    this class."""
    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self.duration = kwargs.get("duration")

        self.name = self.__doc__
        self.description = self.buff.__doc__

    def calc(self, player):
        """This is normally the method that would have to be implemented by the user but because buffs are timed we use this 
        to check if they're still valid before calling the logic."""
        if self.duration != 0:
            return self.buff(player)

    def buff(self, player):
        """Abstract method to be implemented on a per buff basis to determine the stat change."""
        raise NotImplementedError

    def end_turn(self):
        """Method called at the end of the turn for each buff to show time passed and left until the buff expires."""
        if self.duration > 0:
            self.duration -= 1

        if self.duration == 0:
            return True

        return False

class WarRoarBuff(Buff):
    """War Roar of War"""
    def __init__(self):
        super().__init__(type=StatEnum.attack, duration=5)

    def buff(self, target):
        """You are entranced by the roar and your attack is increased for a short time"""
        return 2

class InsultDebuff(Buff):
    """Insult"""
    def __init__(self):
        super().__init__(type=StatEnum.defense, duration=3)

    def buff(self, target):
        """You feel insulted and as a result the target's defense is lowered."""
        return -3

class InsultBuff(Buff):
    """Insult"""
    def __init__(self):
        super().__init__(type=StatEnum.attack, duration=3)

    def buff(self, target):
        """You feel insulted and as a result the target's attack is increased."""
        return 1

class FireDebuff(Buff):
    """Burnt"""

    def __init__(self):
        super().__init__(type=StatEnum.max_health, duration=5)

    def buff(self, target):
        """The burns leaves a scar, reducing the target's maximum health."""
        return -5
