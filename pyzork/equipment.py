from .enums import *
from .base import qm
from .utils import post_output

class Inventory:
    def __init__(self, **kwargs):
        self.consumables = kwargs.get("consumables", {})
        self.quest = kwargs.get("quest", [])
        self.equipment = kwargs.get("equipment", set())
        
    def __repr__(self):
        return f"<Inventory consumables={len(self.consumables)} quest={len(self.quest)} equipment={len(self.equipment)}>"
        
    def add_item(self, item):
        if isinstance(item, Equipment):
            self.equipment.add(item)
            post_output(f"Equipment {item.name} added")
        
        if isinstance(item, Consumable):
            if type(item) in self.consumables:
                self.consumables[type(item)] += 1
            else:
                self.consumables[type(item)] = 1
            post_output(f"Consumable {item.name} added")    
                
        if isinstance(item, QuestItem):
            qm.progress_quests("on_pickup", item)
            self.quest.append(item)
            post_output(f"Quest item {item.name} added")
    
    def use_item(self, item):
        try:
            if self.consumables[type(item)] > 0:
                self.consumables[type(item)] -= 1
                post_output(f"Consumable {item.name} used")
                return True
            else:
                raise KeyError("You don't have this item")
        except KeyError:
            raise KeyError("This item doesn't exist")
            
    def equip_item(self, player, item):
        if not isinstance(item, Equipment):
            raise TypeError("This type of item cannot be equipped")
            
        if isinstance(item, Weapon):
            self.equipment.add(player.weapon)
            player.weapon = item
            self.equipment.remove(player.weapon)
            post_output(f"Weapon {item.name} equipped")
        else:
            self.equipment.add(player.armor)
            player.armor = item
            self.equipment.remove(player.armor)
            post_output(f"Armor {item.name} equipped")
            
    def remove_item(self, item):
        if isinstance(item, Equipment):
            self.equipment.remove(item)
            post_output(f"Equipment {item.name} removed")
        elif isinstance(item, Consumable):
            del self.consumables[type(item)]
            post_output(f"Consumable {item.name} removed")
        elif isinstance(item, QuestItem):
            post_output(f"Quest Item {item.name} removed")
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
        
class Item:
    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs.get("name")
        else:
            self.name = self.__doc__ if self.__doc__ else self.__class__.__name__

        self.description = kwargs.get("description", self.__init__.__doc__)
        
    def __repr__(self):
        return f"<{self.name}>"
        
    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
            
        return self.name == other.name
        
class Consumable:
    pass
    
class QuestItem:
    pass

class Equipment(Item):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def calc(self, player):
        """Abstract method that must be implemented by every piece of equipment, this is the method used when
        calculating damage that dictates the various modifiers and buffs gotten"""
        pass
        
    def effect(self, target):
        """Abstract class that applies an effect when attacking"""
        pass
        
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
