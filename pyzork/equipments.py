from .enums import *

class Equipment:
    def __init__(self):
        self.name = self.__doc__
        self.description = self.calc.__doc__

    def equip(self, player):
        """Abstract method that must be implemented by every piece of equipment, this is the method when equipping
        a piece of equipment to add the required buffs."""
        raise NotImplementedError
        
    @property
    def string(self):
        return self.name
        
Armor = Equipment
Weapon = Equipment
    
        
class NullWeapon(Weapon):
    """bare knuckles"""
    
    def calc(self, player):
        """This slot is empty"""
        return []
        
class NullArmor(Weapon):
    """linen clothes"""
    
    def calc(self, player):
        """This slot is empty"""
        return []

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

