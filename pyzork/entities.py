from .enums import StatEnum, EndgameReason
from .errors import EndGame
from .equipment import NullWeapon, NullArmor, Inventory
from .levels import ExperienceLevels
from .utils import post_output
from .base import qm


class Entity:
    """Abstract class representing an entity, can be an NPC, a player or an enemy."""
    def __init__(self, **stats):
        self.base_max_health = stats.get("base_max_health", 0)
        self._health = stats.get("base_health", self.base_max_health)

        self.base_damage = stats.get("base_damage", 0)
        self.base_defense = stats.get("base_defense", 0)

        self.base_max_energy = stats.get("base_max_energy", 0)
        self._energy = stats.get("base_energy", self.base_max_energy)

        self.weapon =  stats.get("weapon", NullWeapon())
        self.armor = stats.get("armor", NullArmor())
        self.inventory = stats.get("inventory", Inventory())

        self.name = self.__doc__ if self.__doc__ else self.__class__.__name__
        self.description = self.__init__.__doc__

        self.modifiers = set()
        self.abilities = set()
        self.interacted = False

    def interact(self, world):
        """Abstract method for interacting with this entity, give a quest, open a shop or fight."""
        pass
        
    def __str__(self):
        return f'<{self.name}>'
        
    def print_interaction(self, world):
        """Abstract method to be implemented, notifies the player that they can interact with this
        NPC, returns a string or None"""
        raise NotImplementedError
        
    def _interact(self):
        pass

    def _big_calc(self, stat):
        """Calculate all the modifiers for a stat"""
        return (sum([x.calc(self) for x in self.modifiers if x.type == stat]) 
            + sum([x[1] for x in [*self.weapon.calc(self), *self.armor.calc(self)] if x[0] == stat]))

    @property
    def attack(self):
        """This method compiles all the buffs, equipment, attributes to generate the attack stat of a unit."""
        return self.base_damage + self._big_calc(StatEnum.attack)
        
    @property
    def defense(self):
        """This method compiles all the buffs, equipment, attributes to generate the defense stat of a unit."""
        return self.base_defense + self._big_calc(StatEnum.defense)

    @property
    def max_health(self):
        """This method compiles all the buffs, equipment, attributes to generate the max health stat of a unit."""
        return self.base_max_health + self._big_calc(StatEnum.max_health)

    @property
    def max_energy(self):
        """This method compiles all the buffs, equipment, attributes to generate the max health stat of a unit."""
        return self.base_max_energy + self._big_calc(StatEnum.max_energy)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        current = self._health
        if value <= 0:
            self._health = 0
            qm.progress_quests("on_death", self)
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
        return self._energy

    @energy.setter
    def energy(self, value):
        current = self._energy
        if value <= 0:
            self._energy = 0
        elif value > self.max_energy:
            self._energy = self.max__energy
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
        
    def use_ability(self, ability, target=None):
        if target is None:
            target = self
        
        return ability.cast(self, target)
        
    def end_turn(self):
        for _, modifier in enumerate(self.modifiers):
            modifier.end_turn(self)
            if modifier.is_expired():
                self.modifiers.remove(modifier)
            
    def add_to_inventory(self, item):
        self.inventory.add_item(item)
        
    def remove_from_inventory(self, item):
        self.inventory.remove_item(item)
        
    def add_modifier(self, modifier):
        self.modifiers.add(modifier)
        
    @property
    def string(self):
        return f"{self.description} They are wearing {self.armor.string} and wield {self.weapon.string}"        

class Player(Entity):
    """You"""
    def __init__(self, **kwargs):
        """A normal person with an extrodinary destiny... probably."""
        super().__init__(
            base_max_health=kwargs.get("base_max_health", 100),
            base_damage=kwargs.get("base_damage", 5),
            base_defense=kwargs.get("base_defense", 0),
            base_max_energy=kwargs.get("base_max_energy", 25),
        )
        
        self.experience = kwargs.get("experience", ExperienceLevels(requirement=100, modifier=1.2, max_level=10))
        self.experience.set_player(self)
        
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        current = self._health
        if value <= 0:
            self._health = 0
            qm.progress_quests("on_death", self)
            raise EndGame("Look like you've died, better luck next time.", victory=False, reason=EndgameReason.zero_health)
        elif value > self.max_health:
            self._health = self.max_health
        else:
            self._health = value
            
        if current < value:
            post_output(f"{self.name} gains {value - current} health")
        else:
            post_output(f"{self.name} loses {current - value} health")
            
    def print_actions(self, context):
        post_output("- Attack with 'attack [enemy]'")
        
    def gain_experience(self, value):
        self.experience += value
        
class NPC(Entity):
    pass

class Enemy(Entity):
    def battle_logic(self, battle):
        """This method implement the behavior of enemies during battle. A basic logic is aready implemented which just attacks the player. 
        For boss battles this method is overwritten to implement more complex logic.
        This method takes the entire battle instance as the argument and therefore has full unrestricted access to the entire context
        of the battle, make full use of that."""
        self.do_attack(battle.player)
