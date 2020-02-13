from .enums import *
from .base import qm

class Inventory:
    def __init__(self, **kwargs):
        self.consumables = kwargs.get("consumables", {})
        self.quest = kwargs.get("quest", [])
        self.equipment = kwargs.get("equipment", [])
        
    def add_item(self, item):
        if isinstance(Equipment, item):
            self.equipment.append(item)
        
        if isinstance(Consumable, item):
            if type(item) in self.consumables:
                self.consumables[type(item)] += 1
            else:
                self.consumables[type(item)] = 1
                
        if isinstance(QuestItem, item):
            qm.progress_quests("on_pickup", item)
            self.quest.append(item)
    
    def use_item(self, item):
        try:
            if self.consumables[type(item)] > 0:
                self.consumables[type(item)] -= 1
                return True
            else:
                raise KeyError("You don't have this item")
        except KeyError:
            raise KeyError("This item doesn't exist")
            
    def equip_item(self, player, item):
        if not isinstance(item, Equipment):
            raise TypeError("This type of item cannot be equipped")
            
        if isinstance(item, Weapon):
            self.equipment.append(player.weapon)
            player.weapon = item
            self.equipment.remove(player.weapon)
        else:
            self.equipment.append(player.armor)
            player.armor = item
            self.equipment.remove(player.armor)
            
    def remove_item(self, item):
        if isinstance(item, Equipment):
            self.equipment.remove(item)
        elif isinstance(item, Consumable):
            del self.consumables[type(item)]
        elif isinstance(item, QuestItem):
            self.quest.remove(item)
            
    def print_consumables(self):
        pass
        
    def print_equipment(self):
        pass
        
    def print_quest(self):
        pass
        
    def get_item(self, iterable, name):
        for x in iterable:
            if x.name == name:
                return x
                
        return None
        
class Consumable:
    pass
    
class QuestItem:
    pass

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
