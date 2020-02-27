from .enums import *
from .base import QM
from .utils import post_output, get

class Item:
    def __init__(self, **kwargs):
        if not getattr(self, "name", False):
            if "name" in kwargs:
                self.name = kwargs.get("name")
            else:
                self.name = self.__doc__ if self.__doc__ else self.__class__.__name__

        if not getattr(self, "description", False):
            self.description = kwargs.get("description", self.__init__.__doc__)
        
    def __repr__(self):
        return f"<{self.name}>"
        
    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
            
        return self.name == other.name

        
class Consumable(Item):
    def __init__(self, **kwargs):
        if "amount" in kwargs:
            self.amount = kwargs.pop("amount")
        super().__init__(kwargs)
        
    def use(self, player):
        if self.amount > 0:
            self.amount -= 1
            self.effect(player)
            
            return True
        else:
            return False
            
    def effect(self, player):
        """"""
        pass
        
    @classmethod
    def add(cls, **kwargs):
        def decorator(func):
            new_class = type(func.__name__, (cls,), {
                "amount": kwargs.pop("amount", 1), 
                "effect": func, 
                "name": kwargs.pop("name", func.__name__),
                "description": kwargs.pop("description", func.__doc__),
            })
            
            return new_class
            
        return decorator

class QuestItem(Item):
    pass

class Equipment(Item):
    def calc(self, player):
        return self.buff(player)
    
    def buff(self, player):
        """Abstract method that must be implemented by every piece of equipment, this is the method used when
        calculating damage that dictates the various modifiers and buffs gotten"""
        pass
        
    def effect(self, target):
        """Abstract class that applies an effect when attacking"""
        pass
        
    @classmethod
    def add_effect(cls, **kwargs):
        """Decorator function to allow the user to define an effect by decorating a function. Takes the
        same parameters as the class. """        
        def decorator(func):
            if not cls is Equipment:
                cls.effect = func
                return func
            else:
                new_class = type(func.__name__, (cls,), {
                    "effect": func, 
                    "name": kwargs.pop("name", func.__name__),
                    "description": kwargs.pop("description", func.__doc__),
                })
                
                return new_class
            
        return decorator
        
    @classmethod
    def add_buff(cls, **kwargs):
        """Decorator function to allow the user to define a buff by decorating a function. Takes
        the same parameters as the class. Since this specifically adds a buff, the `stat_type` parameter
        is required"""
        def decorator(func):
            if not cls is Equipment:
                cls.buff = func
                return func
            else:
                new_class = type(func.__name__, (cls,), {
                    "buff": func,
                    "name": kwargs.pop("name", func.__name__),
                    "description": kwargs.pop("description", func.__doc__),
                })
                
                return new_class
        
        return decorator
        
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
        
class ShopItem:
    def __init__(self, **kwargs):
        self.item = kwargs.pop("item")
        self.price = kwargs.pop("price")
        self.amount = kwargs.pop("amount", 0)
        
    def __repr__(self):
        return f"<{self.item.name} amount={self.amount} price={self.price}>"
        
    def buy(self, player):
        if not self.amount > 0:
            return post_output("No items left")
            
        if player.money < self.price:
            return post_output("Not enough money")
            
        self.amount -= 1
        player.remove_money(self.price)
        player.add_to_inventory(self.item())
        
    def sell(self, player, resell):
        to_remove = player.inventory.get_item(name=self.item.name)
        if to_remove is None:
            return post_output("Couldn't find the item")
            
        if isinstance(to_remove, Consumable):
            player.inventory.remove_item(to_remove)
            amount = to_remove.amount // self.item.amount
            self.amount += amount
            player.add_money((self.price * resell) * amount)
        else:
            player.inventory.remove_item(to_remove)
            self.amount += 1
            player.add_money(self.price * resell)

class Inventory:
    def __init__(self, **kwargs):
        self.consumables = kwargs.get("consumables", {})
        self.quest = kwargs.get("quest", [])
        self.equipment = kwargs.get("equipment", set())
        
    def __repr__(self):
        return f"<Inventory consumables={len(self.consumables)} quest={len(self.quest)} equipment={len(self.equipment)}>"
    
    def print(self):
        post_output(f"Consumables: {self.consumables}")
        post_output(f"Quest Items: {self.quest}")
        post_output(f"Equipment: {self.equipment}")
    
    def add_item(self, item : Item):
        if isinstance(item, Equipment):
            self.equipment.add(item)
            post_output(f"Equipment {item.name} added")
        
        if isinstance(item, Consumable):
            if type(item) in self.consumables:
                self.consumables[type(item)].amount += item.amount
            else:
                self.consumables[type(item)] = item
            post_output(f"Consumable {item.name} added")    
                
        if isinstance(item, QuestItem):
            self.quest.append(item)
            post_output(f"Quest item {item.name} added")
        
        QM.progress_quests("on_pickup", item)
    
    def use_item(self, item : Consumable, player : "Player"):
        used = item.use(player)
        if not used:
            post_output("You cannot use this item")
            
        return used
            
    def equip_item(self, item : Equipment, player : "Player"):
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
            
    def remove_item(self, item : Item):
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
        for consumable in self.consumables:
            post_output(f"- {consumable.name}: {consumable.description}")
        
    def print_equipment(self):
        for equipment in self.equipment:
            post_output(f"- {equipment.name}: {equipment.description}")
        
    def print_quest(self):
        for quest in self.quest:
            post_output(f"- {quest.name}: {quest.description}")
        
    def get_equipment(self, **kwargs):
        return get(self.equipment, **kwargs)
        
    def get_quest(self, **kwargs):
        return get(self.quest, **kwargs)
        
    def get_consumable(self, **kwargs):
        return get(self.consumables, **kwargs)
        
    def get_item(self, **kwargs):
        item = self.get_consumable(**kwargs)
        
        if item is not None:
            return item
            
        item = self.get_quest(**kwargs)
        
        if item is not None:
            return item
            
        item = self.get_equipment(**kwargs)
        
        return item
