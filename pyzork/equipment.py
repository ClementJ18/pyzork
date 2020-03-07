from .enums import *
from .base import QM
from .utils import post_output, get

class Item:
    """An item is a physical object the player can interact with and carry aroun with them everywhere they
    various subclasses of item have various uses. Equipments are meant to provide a buff when equipped, consumables
    provide an effect, kinda like a handheld ability. Quest items don't usually provide an direct benefit but rather
    are a prequisite for unlocking certain areas and progressing the story.
    
    Parameters
    -----------
    name : str
        The name of the item, if it is not provided then defaults first to the class docs and then the class name
    description : Optional[str]
        The description of the item
    
    Attributes
    -----------
    name : str
        Name of the item
    description : str
        Description of the item
    """
    def __init__(self, **kwargs):
        if not hasattr(self, "name"):
            if "name" in kwargs:
                self.name = kwargs.get("name")
            else:
                self.name = self.__doc__ if self.__doc__ else self.__class__.__name__

        if not hasattr(self, "description"):
            self.description = kwargs.get("description", self.__init__.__doc__)
        
    def __repr__(self):
        return f"<{self.name}>"
        
    def __str__(self):
        return self.name
        
    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
            
        return self.name == other.name

        
class Consumable(Item):
    """Consumable are items which the player can use at pretty much anytime to gain an effect, kinda
    like an ability with limited uses which costs no energy. Each consumable can be used a certain number
    of times before it disappears, if the player buys more of the consumable then the charges will be
    added together. When selling a consumable the charges will be split up based on how many charges the
    buyer accepts, for example if the shop takes consumables with 2 charges and you have one with 5 then
    it will make two sales and discrd the remainer.
    
    Parameters
    -----------
    name : str
        The name of the item, if it is not provided then defaults first to the class docs and then the class name
    description : Optional[str]
        The description of the item
    charges : int
        The amount of times this item can be used    
    
    Attributes
    -----------
    name : str
        Name of the item
    description : str
        Description of the item
    charges : int
        The amount of times this item can be used
    """
    def __init__(self, **kwargs):
        if not hasattr(self, "charges"):
            self.charges = kwargs.pop("charges")
            
        super().__init__(kwargs)
        
    def use(self, target):
        if self.charges > 0:
            self.charges -= 1
            self.effect(target)
            
            return True
        else:
            return False
            
    def effect(self, target):
        """The function called when the item is used, overwrite this to cause an effect
        
        Parameters
        -----------
        target : Entity
            The target of the item, can be the user or could be an NPC
        """
        pass
        
    @classmethod
    def add(cls, **kwargs):
        """Decorator method to create a consumable off a method, takes the same parameters
        as the class."""
        def decorator(func):
            new_class = type(func.__name__, (cls,), {
                "charges": kwargs.pop("charges"), 
                "effect": func, 
                "name": kwargs.pop("name", func.__name__),
                "description": kwargs.pop("description", func.__doc__),
            })
            
            return new_class
            
        return decorator

class QuestItem(Item):
    """Quest items are special item which do nothing on their own but can be used as requirement for certain
    part of the story, for example the guards at the palace entrance won't let you enter unless you have a letter
    of recommendation in your inventory.
    
    Parameters
    -----------
    name : str
        The name of the item, if it is not provided then defaults first to the class docs and then the class name
    description : Optional[str]
        The description of the item
    
    Attributes
    -----------
    name : str
        Name of the item
    description : str
        Description of the item
    """
    pass

class Equipment(Item):
    """Equipment can't be used on their own and don't do anything special while they sit in your inventory. They're
    instead meant to be equipped on the player, in which case they can provide a buff and effect
    
    Parameters
    -----------
    name : str
        The name of the item, if it is not provided then defaults first to the class docs and then the class name
    description : Optional[str]
        The description of the item
    
    Attributes
    -----------
    name : str
        Name of the item
    description : str
        Description of the item
    """
    def calc(self, player):
        return self.buff(player)
    
    def buff(self, player):
        """Abstract method that must be implemented by every piece of equipment, this is the method used when
        calculating damage that dictates the various modifiers and buffs gotten"""
        return []
        
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
        
class Armor(Equipment):
    pass

class Weapon(Equipment):
    pass

NullWeapon = Weapon(name="bare hands")
NullArmor = Armor(name="linen clothes")
        
class ShopItem:
    """A shop item is an item that can be sold or bought in a shop. 
    
    Parameters
    -----------
    item : Union[Consumable, QuestItem, Equipment]
        The item to sell, this is the class itself, not an instance of the object
    price : int
        The price of the item
    amount : int
        The number of items that are available for sale, if a player sells an item 
        it will increment the amount
    """
    def __init__(self, **kwargs):
        self.item = kwargs.pop("item")
        self.price = kwargs.pop("price")
        self.charges = kwargs.pop("amount", 0)
        
    def __repr__(self):
        return f"<{self.item.name} amount={self.charges} price={self.price}>"
        
    def buy(self, entity : "Entity"):
        """Buy an instance of that item
        
        Parameters
        -----------
        entity : Entity
            The entity purchasing the item
        """
        if not self.charges > 0:
            return post_output("No items left")
            
        if entity.money < self.price:
            return post_output("Not enough money")
            
        self.charges -= 1
        entity.remove_money(self.price)
        entity.add_to_inventory(self.item())
        
        post_output(f"Bought {self.item.name} and payed {self.price}")
        
    def sell(self, entity : "Entity", resell : float):
        """Sell an instance of that item
        
        Parameters
        -----------
        entity : Entity
            The entity selling the item
        resell : float
            The resale value, this is usually passed down from the shop instance
        """
        to_remove = entity.inventory.get_item(name=self.item.name)
        if to_remove is None:
            return post_output("Couldn't find the item")
            
        if isinstance(to_remove, Consumable):
            entity.inventory.remove_item(to_remove)
            amount = to_remove.amount // self.item.amount
            self.charges += amount
            money = (self.price * resell) * amount
            entity.add_money(money)
        else:
            entity.inventory.remove_item(to_remove)
            self.charges += 1
            money = self.price * resell
            entity.add_money(money)
        
        post_output(f"Sold {self.item.name} and gained {money}")

class Inventory:
    """Inventories store all items: Equipment, Consumables and QuestItem. """
    def __init__(self, **kwargs):
        self.consumables = kwargs.get("consumables", {})
        self.quest = kwargs.get("quest", [])
        self.equipment = kwargs.get("equipment", set())
        
        self.weapon =  kwargs.get("weapon", NullWeapon())
        self.armor = kwargs.get("armor", NullArmor())
        
    def __repr__(self):
        return f"<Inventory consumables={len(self.consumables)} quest={len(self.quest)} equipment={len(self.equipment)}>"
    
    def print(self):
        """Print all the item in the entity's inventory"""
        post_output(f"Consumables: {self.consumables}")
        post_output(f"Quest Items: {self.quest}")
        post_output(f"Equipment: {self.equipment}")
    
    def add_item(self, item : Item):
        """Add an item to the entity's inventory
        
        Parameters
        ------------
        item : Item
            The item you want to add to the inventory, the
            method will sort out where it needs to go.    
        """
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
    
    def use_item(self, item : Consumable, target):
        """Use a consumable on a target
        
        Parameters
        -----------
        item : Consumable
            The item to use
        target : Entity
            The entity to use it on
        """
        used = item.use(target)
        if not used:
            post_output("You cannot use this item")
            
        return used
            
    def equip_item(self, item : Equipment):
        """Equip either a weapon or armor
        
        Parameters
        -----------
        item : Equipment
            The piece of equipment to add
        """
        if not isinstance(item, Equipment):
            raise TypeError("This type of item cannot be equipped")
            
        if isinstance(item, Weapon):
            self.equipment.add(self.weapon)
            self.weapon = item
            self.equipment.remove(self.weapon)
            post_output(f"Weapon {item.name} equipped")
        else:
            self.equipment.add(self.armor)
            self.armor = item
            self.equipment.remove(self.armor)
            post_output(f"Armor {item.name} equipped")
            
    def remove_item(self, item : Item):
        """Remove an item from the inventory
        
        Parameters
        -----------
        item : Item
            The item to remove
        """
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
        """Print all the consumables"""
        for consumable in self.consumables:
            post_output(f"- {consumable.name}: {consumable.description}")
        
    def print_equipment(self):
        """Print all the equipments"""
        for equipment in self.equipment:
            post_output(f"- {equipment.name}: {equipment.description}")
        
    def print_quest(self):
        """Print all the quest items"""
        for quest in self.quest:
            post_output(f"- {quest.name}: {quest.description}")
        
    def get_equipment(self, **kwargs):
        """Get an equipment instance based on a parameter. The parameter
        is any kwarg to you pass, if you want the parameter to be the name
        of the item then you can do something like `get_equipment(name='Big Sword')`"""
        return get(self.equipment, **kwargs)
        
    def get_quest(self, **kwargs):
        """Get an quest instance based on a parameter. The parameter
        is any kwarg to you pass, if you want the parameter to be the name
        of the item then you can do something like `get_quest(name='Old Key')`"""
        return get(self.quest, **kwargs)
        
    def get_consumable(self, **kwargs):
        """Get an consumable instance based on a parameter. The parameter
        is any kwarg to you pass, if you want the parameter to be the name
        of the item then you can do something like `get_consumable(name='Health Potion')`"""
        return get(self.consumables, **kwargs)
        
    def get_item(self, **kwargs):
        """Get an equipment, consumable or quest instance based on a parameter. The parameter
        is any kwarg to you pass, if you want the parameter to be the name
        of the item then you can do something like `get_item(name='Big Sword')`"""
        item = self.get_consumable(**kwargs)
        
        if item is not None:
            return item
            
        item = self.get_quest(**kwargs)
        
        if item is not None:
            return item
            
        item = self.get_equipment(**kwargs)
        
        return item
