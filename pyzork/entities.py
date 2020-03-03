from .enums import StatEnum, EndgameReason
from .errors import EndGame
from .equipment import NullWeapon, NullArmor, Inventory
from .levels import ExperienceLevels
from .utils import post_output
from .base import QM

import math

class Entity:
    """Abstract class representing an entity, can be an NPC, a player or an enemy."""
    def __init__(self, **kwargs):
        self.base_max_health = kwargs.get("max_health", 0)
        self._health = kwargs.get("health", self.base_max_health)

        self.base_damage = kwargs.get("damage", 0)
        self.base_defense = kwargs.get("defense", 0)

        self.base_max_energy = kwargs.get("max_energy", 0)
        self._energy = kwargs.get("energy", self.base_max_energy)

        self.weapon =  kwargs.get("weapon", NullWeapon())
        self.armor = kwargs.get("armor", NullArmor())
        self.inventory = kwargs.get("inventory", Inventory())
        
        self.experience = kwargs.get("experience", ExperienceLevels(requirements=[math.inf], max_level=1))
        self.experience.set_entity(self)
        
        self.money = kwargs.get("money", 0)
        
        if "name" in kwargs:
            self.name = kwargs.get("name")
        else:
            self.name = self.__doc__ if self.__doc__ else self.__class__.__name__

        self.description = kwargs.get("description", self.__init__.__doc__)

        self.modifiers = {}
        self.abilities = {}
        self.interacted = False
        
    def __repr__(self):
        return f'<{self.name} health={self.health}/{self.max_health} energy={self.energy}/{self.max_energy}>'
        
    def __str__(self):
        return self.name

    def interact(self, world):
        QM.progress_quests("on_interact", self, world)
        self.interaction(world)
        self.interacted = True
        
    def print_interaction(self, world):
        """Abstract method to be implemented, notifies the player that they can interact with this
        NPC, returns a string or None"""
        post_output(f"- Interact with {self.name}")
        
    def interaction(self, world):
        """Abstract method for interacting with this entity, give a quest, open a shop or fight."""
        pass
        
    def print_abilities(self):
        post_output(self.abilities)
        
    def print_inventory(self):
        self.inventory.print()
        self.print_abilities()
        
    def print_stats(self):
        post_output(f"{self.name}: LV {self.experience.level}")
        post_output(f"Health: {self.health}/{self.max_health}")
        post_output(f"Energy: {self.energy}/{self.max_energy}")
        post_output(f"Attack/Defense: {self.attack}/{self.defense}")
        post_output(f"Weapon/Armor: {self.weapon}/{self.armor}")
        post_output(f"Money: {self.money}")
        post_output(f"Modifiers: {self.modifiers}")

    def _big_calc(self, stat):
        """Calculate all the modifiers for a stat"""
        total = 0
        #modifiers
        for modifier in self.modifiers:
            if modifier.stat_type == stat:
                total += modifier.calc(self)
                
        #weapons
        for modifier in [*self.weapon.calc(self), *self.armor.calc(self)]:
            if modifier[0] == stat:
                total += modifier[1]
        
        #total
        return total

    @property
    def attack(self):
        """This method compiles all the buffs, equipment, attributes to generate the attack stat of a unit."""
        return max(0, self.base_damage + self._big_calc(StatEnum.attack))
        
    @property
    def defense(self):
        """This method compiles all the buffs, equipment, attributes to generate the defense stat of a unit."""
        return max(0, self.base_defense + self._big_calc(StatEnum.defense))

    @property
    def max_health(self):
        """This method compiles all the buffs, equipment, attributes to generate the max health stat of a unit."""
        return max(0, self.base_max_health + self._big_calc(StatEnum.max_health))

    @property
    def max_energy(self):
        """This method compiles all the buffs, equipment, attributes to generate the max health stat of a unit."""
        return max(0, self.base_max_energy + self._big_calc(StatEnum.max_energy))

    @property
    def health(self):
        max_health = self.max_health
        if self._health > max_health:
            self._health = max_health
            return self._health
        
        return self._health

    @health.setter
    def health(self, value):
        current = self._health
        if value <= 0:
            self._health = 0
            QM.progress_quests("on_death", self)
        elif value > self.max_health:
            self._health = self.max_health
        else:
            self._health = int(value)
            
        if current < value:
            post_output(f"{self.name} gains {value - current} health")
        else:
            post_output(f"{self.name} loses {current - value} health")

    @property
    def energy(self):
        max_energy = self.max_energy
        if self._energy > max_energy:
            self._energy = max_energy
            return self._energy
        
        return self._energy

    @energy.setter
    def energy(self, value):
        current = self._energy
        if value <= 0:
            self._energy = 0
        elif value > self.max_energy:
            self._energy = self.max_energy
        else:
            self._energy = int(value)
            
        if current < value:
            post_output(f"{self.name} gains {value - current} energy")
        else:
            post_output(f"{self.name} loses {current - value} energy")

    def is_alive(self):
        return self.health > 0

    def can_cast(self, value):
        return value <= self.energy

    def do_attack(self, target):
        post_output(f"{self.name} attacks {target.name} with their {self.weapon.name}")
        target.take_damage(self.attack)
        
    def take_damage(self, value):
        self.health -= max(1, value - self.defense)
        
    def take_pure_damage(self, value):
        self.health -= value
        
    def restore_health(self, value):
        self.health += value
        
    def use_energy(self, value):
        self.energy -= value
        
    def gain_energy(self, value):
        self.energy += value
        
    def use_ability(self, ability, target):
        return ability.cast(self, target)
        
    def end_turn(self):
        for name in list(self.modifiers.keys()):
            modifier = self.modifiers[name]
            modifier.end_turn(self)
            if modifier.is_expired():
                del self.modifiers[name]
            
    def add_to_inventory(self, item):
        self.inventory.add_item(item)
        
    def remove_from_inventory(self, item):
        self.inventory.remove_item(item)
        
    def add_modifier(self, modifier):
        if hash(modifier) in self.modifier:
            self.modifiers[hash(modifier)] = modifier if modifier.duration > self.modifiers[hash(modifier)] else self.modifiers[hash(modifier)]
        else:
            self.modifiers[hash(modifier)] = modifier
    
    def add_ability(self, ability):
        self.abilities[hash(ability)] = ability
        
    def gain_experience(self, value):
        self.experience += value
        
    def use_item_on_me(self, item):
        self.use_item_on(item, self)
        
    def use_item_on(self, item, target):
        self.inventory.use_item(item, target)
        
    def remove_money(self, value):
        self.money -= value
        
    def add_money(self, value):
        self.money += money
        
    @property
    def string(self):
        return f"{self.description} They are wearing {self.armor.string} and wield {self.weapon.string}"      

class Player(Entity):
    """You"""
    def __init__(self, **kwargs):
        """A normal person with an extrodinary destiny... probably."""
        super().__init__(**kwargs)
        self.world = None
        
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        current = self._health
        if value <= 0:
            self._health = 0
            QM.progress_quests("on_death", self)
            raise EndGame("Look like you've died, better luck next time.", victory=False, reason=EndgameReason.zero_health)
        elif value > self.max_health:
            self._health = self.max_health
        else:
            self._health = value
            
        if current < value:
            post_output(f"{self.name} gains {value - current} health")
        else:
            post_output(f"{self.name} loses {current - value} health")        
        
    def set_world(self, world):
        self.world = world
        
    def print_inventory(self):
        self.inventory.print()
        self.print_abilities()
        post_output(QM.active_quests)

class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.experience_points = kwargs.get("experience", 0)
    
    @classmethod
    def from_dict(cls, **kwargs):
        new_class = type(kwargs.get("name"), (cls,), kwargs)
        return new_class
        
    def experience(self, player):
        return self.experience_points
    
    def battle_logic(self, battle):
        """This method implement the behavior of enemies during battle. A basic logic is aready implemented which just attacks the player. 
        For boss battles this method is overwritten to implement more complex logic.
        This method takes the entire battle instance as the argument and therefore has full unrestricted access to the entire context
        of the battle, make full use of that."""
        self.do_attack(battle.player)
