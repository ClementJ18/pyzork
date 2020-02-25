from pyzork.equipment import Weapon, Armor, QuestItem
from pyzork.enums import StatEnum

class Sword(Weapon):
    """A Simple Sword"""

    def calc(self, player):
        """This simple bronze sword gives you a small bonus to your attack"""

        return [(StatEnum.attack, 5)]
        
class SwordAndShield(Weapon):
    """A Sword and a shield"""
    
    def calc(self, player):
        """This bronze sword also has a shield included for bonus defense"""
        return [(StatEnum.attack, 5), (StatEnum.defense, 3)]
        
class LeatherArmor(Armor):
    """simple leather armor"""
    
    def calc(self, player):
        """This leather armor can block some blows"""
        
        return [(StatEnum.defense, 5)]
        

class Key(QuestItem):
    pass