from pyzork.equipment import Weapon, Armor, QuestItem, Consumable
from pyzork.enums import StatEnum

from .example_modifiers import HealingOnguentModifier

@Weapon.add_buff()
def Sword(self, player):
    """This simple bronze sword gives you a small bonus to your attack"""

    return [(StatEnum.attack, 5)]
        
@Weapon.add_buff()
def SwordAndShield(self, player):
    """This bronze sword also has a shield included for bonus defense"""
    return [(StatEnum.attack, 5), (StatEnum.defense, 3)]
        
class LeatherArmor(Armor):
    """simple leather armor"""
    
    def buff(self, player):
        """This leather armor can block some blows"""
        
        return [(StatEnum.defense, 5)]
        
class Key(QuestItem):
    pass
    
@Consumable.add(amount=1)
def HealthPotion(item, player):
    player.restore_health(5)
    
@Consumable.add(amount=3)
def HealingOnguent(item, player):
    player.add_modifier(HealingOnguentModifier())