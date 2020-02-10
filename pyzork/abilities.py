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
        
    
@Ability.add(cost=2)    
def WarRoarSpell(self, target):
    target.modifiers.append(WarRoarBuff())
    
    
def callable_cost(player, target):
    return player.max_energy * 0.1
    
@Ability.add(cost=callable_cost)    
def WarRoar2Spell(self, target):
    target.modifiers.append(WarRoarBuff())

# class WarRoarSpell(Ability):
#     """War Roar of War"""

#     def effect(self, target):
#         """Scream till you either feel stronger of faint from the lack of oxygen."""
#         target.modifiers.append(WarRoarBuff())
#         return True

#     def costing(self, player, target):
#         """2 Mana"""
#         if player.can_cast(2):
#             self.energy -= 2
#             return True

#         return False

class InsultSpell(Ability):
    """Insult"""

    def effect(self, target):
        """A weak insult likening the target's mother to a bovine and lower their defense by 3 but increases their attack by 1"""
        target.modifiers.append(InsultDebuff())
        target.modifiers.append(InsultBuff())
        return True

    def costing(self, player, target):
        """2 Mana"""
        if player.can_cast(2):
            player.energy -= 2
            return True

        return False

class HealSpell(Ability):
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

class FireballSpell(Ability):
    """Fireball"""

    def effect(self, target):
        """A small fireball emerges from your hands and burns the enmy. Dealing damage and reducing their max health"""
        target.health -= 5
        target.modifiers.append(FireDebuff())
        target.effects.append(BurntEffect())
        return True

    def costing(self, player, target):
        """2 Mana"""
        if player.can_cast(2):
            self.energy -= 2
            return True

        return False
