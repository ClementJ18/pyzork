from pyzork.abilities import Ability

from .example_modifiers import WarRoarBuff, InsultDebuff, InsultBuff, FireDebuff, BurntEffect

@Ability.add(cost=2, name="War Roar")    
def WarRoarSpell(ability, user, target):
    """A terrible war cry that envigorates you"""
    target.add_modifier(WarRoarBuff())
    
def callable_cost(ability, player, target):
    return player.max_energy * 0.1
    
@Ability.add(cost=callable_cost, description="Very loud yelling")    
def WarRoar2Spell(ability, user, target):
    target.add_modifier(WarRoarBuff())

class InsultSpell(Ability):
    """Insult"""

    def effect(self, user, target):
        """A weak insult likening the target's mother to a bovine and lower their defense by 3 but increases 
        their attack by 1"""
        target.add_modifier(InsultDebuff())
        target.add_modifier(InsultBuff())

    def cost(self, user, target):
        """2 Mana"""
        return 2

class HealSpell(Ability):
    """Heal"""

    def effect(self, user, target):
        """You feel a touch slide down your spine and heal you."""
        target.restore_health(5)

    def cost(self, user, target):
        """2 Mana"""
        return 2

class FireballSpell(Ability):
    """Fireball"""

    def effect(self, user, target):
        """A small fireball emerges from your hands and burns the enmy. Dealing damage and reducing 
        their max health"""
        target.take_pure_damage(5)
        target.add_modifier(FireDebuff())
        target.add_modifier(BurntEffect())

    def cost(self, user, target):
        """2 Mana"""
        return 2
