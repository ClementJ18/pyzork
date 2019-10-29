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
        pass

    def end_turn(self, player):
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

class Effect:
    """Parent class for all the effects, effect are different to buffs since they cause a permanent change at the end
    of the turn, such as a poison damage or regenerating health. These are essentially the same as buffs in how they function."""
    def __init__(self, **kwargs):
        self.duration = kwargs.get("duration")

        self.name = self.__doc__
        self.description = self.effect.__doc__

    def effect(self, player):
        """Abstract method to be implemented on the buff to determine an action that takes place only once a turn
        at the end of the turn such as poison."""
        pass

    def end_turn(self, player):
        """Method called at the end of the turn for each buff to show time passed and left until the buff expires."""
        if self.duration > 0:
            self.duration -= 1

        if self.duration == 0:
            return True
        else:
            self.effect(player)

        return False

class PoisonEffect(Effect):
    """Poison"""
    def __init__(self):
        super().__init__(duration=5)

    def effect(self, player):
        """Lose 3 health every turn."""
        self.player.health -= 3

class BurntEffect(Effect):
    """Burnt"""

    def __init__(self):
        super().__init__(duration=5)

    def effect(self, player):
        """Lose 2 health every turn"""
        self.player.health -= 2
