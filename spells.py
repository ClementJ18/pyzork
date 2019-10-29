from modifiers import *

class Spell:
    """Parent class for all spell."""
    def __init__(self):
        self.name = self.__doc__
        self.description = self.effect.__doc__
        self.cost = self.costing.__doc__

    def cast(self, user, target = None):
        """Method that verifies if all conditions have been met."""
        if target is None:
            target = user

        if not self.cost(user, target):
            return False

        return self.effect(target)

    def costing(self, player, target):
        """Abstract method that does the logic part of the cost. This allow for flexibility on how you want your cost system to work
        wether it rage or mana or whatever other custom cost system you may create your class with. This method must return true if
        the user has enough resource and false if it doesn't."""
        raise NotImplementedError

    def effect(self, target):
        """Method to be overwritten that handles the actuall effect of the spell."""
        raise NotImplementedError

class WarRoarSpell(Spell):
    """War Roar of War"""

    def effect(self, target):
        """Scream till you either feel stronger of faint from the lack of oxygen."""
        target.buffs.append(WarRoarBuff())
        return True

    def costing(self, player, target):
        """2 Mana"""
        if player.can_cast(2):
            self.energy -= 2
            return True

        return False

class InsultSpell(Spell):
    """Insult"""

    def effect(self, target):
        """A weak insult likening the target's mother to a bovine and lower their defense by 3 but increases their attack by 1"""
        target.buffs.append(InsultDebuff())
        target.buffs.append(InsultBuff())
        return True

    def costing(self, player, target):
        """2 Mana"""
        if player.can_cast(2):
            self.energy -= 2
            return True

        return False

class HealSpell(Spell):
    """Gay Touch"""

    def effect(self, target):
        """You feel a homo erotic touch slide down your spine and heal you."""
        target.health += 5
        return True

    def costing(self, player, target):
        """2 Mana"""
        if player.can_cast(2):
            self.energy -= 2
            return True

        return False

class FireballSpell(Spell):
    """Fireball"""

    def effect(self, target):
        """A small fireball emerges from your hands and burns the enmy. Dealing damage and reducing their max health"""
        target.health -= 5
        target.buffs.append(FireDebuff())
        target.effects.append(BurntEffect())
        return True

    def costing(self, player, target):
        """2 Mana"""
        if player.can_cast(2):
            self.energy -= 2
            return True

        return False
