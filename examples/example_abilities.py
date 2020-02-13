from pyzork.abilities import Ability

from example_modifiers import WarRoarBuff, InsultDebuff, InsultBuff, FireDebuff, BurntEffect

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