from .enums import StatEnum, EndgameReason
from .errors import EndGame
from .equipment import NullWeapon, NullArmor, Inventory
from .levels import ExperienceLevels
from .utils import post_output
from .base import QM

import math

class Entity:
    """Abstract class representing an entity. The player should need to call this, instead rely or either the
    Player or NPC class. A lot of the parameters of this class are optional, depending on which kind of adventure
    you want to make.
    
    Parameters
    -----------
    max_health : int
        The maximum amount of health the entity can have, 0 by default
    health : int
        The entity's current health. Same as `max_health` by default
        
    damage : int
        How much damage a entity deals with empty hands, 0 by default
    defense : int
        How much an entity reduces damage with no extra armor, 0 by default.
        
    max_energy : int
        The maximum amount of energy an entity can have, 0 by default
    energy : int
        The entity's current energy. Same as max_energy by default.
        
    inventory : Inventory
        The entity's inventory
    experience : ExperienceLevels
        This entity's experience and levels
    abilities : List[Ability]
        A list of abilities the entity has at the start
    
    money : int
        This is entity's current money
    
    name : str
        The entity's name
    description : str
        Flavour text about the entity
        
    Attributes
    -----------
    max_health : int
        The maximum amount of health the entity can have.
    health : int
        The entity's current health.
        
    damage : int
        How much damage a entity deals with empty hands.
    defense : int
        How much an entity reduces damage with no extra armor.
        
    max_energy : int
        The maximum amount of energy an entity can have.
    energy : int
        The entity's current energy.
        
    inventory : Inventory
        The entity's inventory
    experience : ExperienceLevels
        This entity's experience and levels
    
    money : int
        This is entity's current money
    
    name : str
        The entity's name
    description : str
        Flavour text about the entity      
    """
    def __init__(self, **kwargs):
        self.base_max_health = kwargs.get("max_health", 0)
        self._health = kwargs.get("health", self.base_max_health)

        self.base_damage = kwargs.get("damage", 0)
        self.base_defense = kwargs.get("defense", 0)

        self.base_max_energy = kwargs.get("max_energy", 0)
        self._energy = kwargs.get("energy", self.base_max_energy)

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
        
        for ability in kwargs.get("abilities", []):
            self.add_ability(ability)
        
    def __repr__(self):
        return f'<{self.name} health={self.health}/{self.max_health} energy={self.energy}/{self.max_energy}>'
        
    def __str__(self):
        return self.name

    #==================================
    #============ Stats ===============
    #==================================
    
    def _big_calc(self, stat):
        """Calculate all the modifiers for a stat"""
        total = 0
        #modifiers
        for modifier in self.modifiers.values():
            if modifier.stat_type == stat:
                total += modifier.calc(self)
                
        #weapons
        for modifier in [*self.inventory.weapon.calc(self), *self.inventory.armor.calc(self)]:
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
            
    #==================================
    #============ Checks ==============
    #==================================

    def is_alive(self):
        """Check if this entity is alive.
        
        Returns
        --------
        bool
            True if the entity is alive
        """
        return self.health > 0

    def can_cast(self, value):
        """Check if this entity can cast 
        
        Parameters
        -----------
        ???
        
        Returns
        --------
        bool
            True if they can cast 
        """
        return self.energy >= value
        
    #==================================
    #============ Displays ============
    #==================================
        
    def print_abilities(self):
        """Print all the abilities of an entity"""
        post_output(self.abilities)
        
    def print_inventory(self):
        """Print all the inventory of entity"""
        self.inventory.print()
        self.print_abilities()
        
    def print_stats(self):
        """Print all the stats of the entity"""
        post_output(f"{self.name}: LV {self.experience.level}")
        post_output(f"Health: {self.health}/{self.max_health}")
        post_output(f"Energy: {self.energy}/{self.max_energy}")
        post_output(f"Attack/Defense: {self.attack}/{self.defense}")
        post_output(f"Weapon/Armor: {self.inventory.weapon}/{self.inventory.armor}")
        post_output(f"Money: {self.money}")
        post_output(f"Modifiers: {self.modifiers}")
        
    #==================================
    #========= Stat Changes ===========
    #==================================

    def do_attack(self, target):
        """Perform an attack on target, the entity attacks with their weapon and the target takes damage.
        This method applies the weapon effect to the target and the armor effect of the target to the attacking
        entity.
        
        Parameters
        -----------
        target : Entity
            The target to attack
        """
        post_output(f"{self.name} attacks {target.name} with their {self.inventory.weapon.name}")
        target.take_damage(self.attack)
        self.inventory.weapon.effect(target)
        target.inventory.armor.effect(self)
        
    def take_damage(self, value):
        """Deal damage to this entity, the entity's defense is substracted from this damage, but this
        can deal no less than 1 damage.
        
        Parameters
        -----------
        value : int
            The amount of damage to take
        """
        if value < 1:
            return
        
        self.take_pure_damage(max(1, value - self.defense))
        
    def take_pure_damage(self, value):
        """Deal pure damage to this entity. Pure damage cannot be reduced by the entity's defense
        
        Parameters
        -----------
        value : in
            The amount of damage to take
        """
        self.health -= value
        
    def restore_health(self, value):
        """Restore some of this entity's health
        
        Parameters
        -----------
        value : int
            The amount of value to restore
        """
        self.health += value
        
    def use_energy(self, value):
        """Use some energy
        
        Parameters
        -----------
        value : int
            The amount of energy to use
        """
        self.energy -= value
        
    def gain_energy(self, value):
        """Gain some energy
        
        Parameters
        -----------
        value : int
            The amount of energy to gain
        """
        self.energy += value
        
    def use_ability(self, ability, target):
        """Use an ability on an entity
        
        Parameters
        -----------
        ability : Ability
            The ability to cast
        target : Entity
            The target to cast the ability on
        """
        return ability.cast(self, target)
        
    def end_turn(self):
        """End this entity's turn, decrementing all the modifier's durations and removing the expired ones."""
        for name in list(self.modifiers.keys()):
            modifier = self.modifiers[name]
            modifier.end_turn(self)
            if modifier.is_expired():
                del self.modifiers[name]
        
    def add_modifier(self, modifier):
        """Add a modifier to the entity, if the modifier already exists it will refresh the duration.
        
        Parameters
        -----------
        modifier : Modifier
            The modifier to add
        """
        if hash(modifier) in self.modifiers:
            self.modifiers[hash(modifier)] = modifier if modifier.duration > self.modifiers[hash(modifier)] else self.modifiers[hash(modifier)]
        else:
            self.modifiers[hash(modifier)] = modifier
            
    def remove_modifier(self, modifer):
        """Remove a modifier from the entity. The argument doesn't need to be the exact same instance, it just
        needs to hash to the same as your intended target.
        
        Parameters
        -----------
        modifier : Modifier
            The modifier to remove
        """
        
        del self.modifiers[hash(modifier)]
    
    def add_ability(self, ability):
        """Add an ability to the entity, making it available for casting
        
        Parameters
        -----------
        ability : Ability
            The ability to add
        """
        self.abilities[hash(ability)] = ability
        
    def remove_ability(self, ability):
        """Remove an ability from the list of available abilities for this entity. The argument does not need
        to be the exact same instance, it just needs to hash to the same as your intended target..
        
        Parameters
        -----------
        ability : Ability
            The ability to remove
        """
        del self.abilities[hash(ability)]
        
    def gain_experience(self, value):
        """Increase the experience of the entity by a certain amount, this amount is affect by the entity
        experience_gain modifier.
        
        Parameters
        -----------
        value : int
            The amount of exp to gain
        """
        self.experience += (value * self.experience.experience_gain)
        
    def lose_experience(self, value):
        """Reduce the experience of the entity by certain amount, this number is not affected by anything.
        
        Parameters
        -----------
        value : int
            The amount of exp to remove
        """
        self.experience -= value
        
    def use_item_on_me(self, item):
        """Use an item on this entity
        
        Parameters
        -----------
        item : Item
            The item to use
        """
        self.use_item_on(item, self)
        
    def use_item_on(self, item, target):
        """Use an item on a target
        
        Parameters
        -----------
        item : Item
            The item to use
        target : Entity
            The entity to use this item on
        """
        self.inventory.use_item(item, target)
        
    def remove_money(self, value):
        """Remove some money from the entity
        
        Parameters
        -----------
        value : int
            The amount of money to remove
        """
        self.money -= value
        
    def add_money(self, value):
        """Add some money to the entity
        
        Parameters
        ------------
        value : int
            The amount of money to add
        """
        self.money += value
        
    @property
    def string(self):
        return f"{self.description} They are wearing {self.inventory.armor.string} and wield {self.inventory.weapon.string}"      

class Player(Entity):
    """The player, this implents some changes from the base entity class such as the player dying raising an
    error and ending the game.
    
    Parameters
    -----------
    max_health : int
        The maximum amount of health the entity can have, 0 by default
    health : int
        The entity's current health. Same as `max_health` by default
        
    damage : int
        How much damage a entity deals with empty hands, 0 by default
    defense : int
        How much an entity reduces damage with no extra armor, 0 by default.
        
    max_energy : int
        The maximum amount of energy an entity can have, 0 by default
    energy : int
        The entity's current energy. Same as max_energy by default.
        
    inventory : Inventory
        The entity's inventory
    experience : ExperienceLevels
        This entity's experience and levels
    
    money : int
        This is entity's current money
    
    name : str
        The entity's name
    description : str
        Flavour text about the entity
        
    Attributes
    -----------
    max_health : int
        The maximum amount of health the entity can have.
    health : int
        The entity's current health.
        
    damage : int
        How much damage a entity deals with empty hands.
    defense : int
        How much an entity reduces damage with no extra armor.
        
    max_energy : int
        The maximum amount of energy an entity can have.
    energy : int
        The entity's current energy.
        
    inventory : Inventory
        The entity's inventory
    experience : ExperienceLevels
        This entity's experience and levels
    
    money : int
        This is entity's current money
    
    name : str
        The entity's name
    description : str
        Flavour text about the entity      
        
    world : World
        The world the player is interacting with, this is not set until the method set_world is called,
        which normally the World you pass the player to will take care.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.world = None
        self.name = "You"
        self.description = "A normal person with an extrodinary destiny... probably."
        
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
        """You must call this if you made changes to the World class' init so that the player has access to
        the world they are interacting in.
        
        Parameters
        -----------
        world : World
            The world instance to link the player to
        """
        self.world = world
        
    def print_inventory(self):
        """Print the inventory, abilities and quests of the player."""
        self.inventory.print()
        self.print_abilities()
        post_output(QM.active_quests)
        
    def battle_logic(self, battle):
        battle.player_turn()

class NPC(Entity):
    """Any interactable entity that isn't the Player
    
    Parameters
    -----------
    max_health : int
        The maximum amount of health the entity can have, 0 by default
    health : int
        The entity's current health. Same as `max_health` by default
        
    damage : int
        How much damage a entity deals with empty hands, 0 by default
    defense : int
        How much an entity reduces damage with no extra armor, 0 by default.
        
    max_energy : int
        The maximum amount of energy an entity can have, 0 by default
    energy : int
        The entity's current energy. Same as max_energy by default.
        
    inventory : Inventory
        The entity's inventory
    experience : ExperienceLevels
        This entity's experience and levels
    
    money : int
        This is entity's current money
    
    name : str
        The entity's name
    description : str
        Flavour text about the entity
        
    experience_points : Optiona[int]
        How much experience this entity grants when defeated in battle, zero by default
        
    Attributes
    -----------
    max_health : int
        The maximum amount of health the entity can have.
    health : int
        The entity's current health.
        
    damage : int
        How much damage a entity deals with empty hands.
    defense : int
        How much an entity reduces damage with no extra armor.
        
    max_energy : int
        The maximum amount of energy an entity can have.
    energy : int
        The entity's current energy.
        
    inventory : Inventory
        The entity's inventory
    experience : ExperienceLevels
        This entity's experience and levels
    
    money : int
        This is entity's current money
    
    name : str
        The entity's name
    description : str
        Flavour text about the entity   
        
    experience_points : int
        How much experience this entity grants when defeated in battle
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.experience_points = kwargs.get("experience", 0)
    
    @classmethod
    def from_dict(cls, **kwargs):
        """Create an enemy from a dictionnary, takes the same paramters as the class"""
        new_class = type(kwargs.get("name"), (cls,), kwargs)
        return new_class
        
    def experience(self, player):
        """Overwritable method which determines how experience is granted to the player when the
        entity is deafeted, by default this simply returns the entity's `experience_points`
        
        Parameters
        -----------
        player : Player
            The player that defeated the entity
            
        Returns
        --------
        int
            The amount of experience to gratn in response
        """
        return self.experience_points
    
    def battle_logic(self, battle):
        """This method implement the behavior of enemies during battle. A basic logic is aready implemented which just attacks the player. 
        For boss battles this method is overwritten to implement more complex logic.
        This method takes the entire battle instance as the argument and therefore has full unrestricted access to the entire context
        of the battle, make full use of that.
        
        Parameters
        -----------
        battle : Battle
            The battle where this entity is taking place
        """
        self.do_attack(battle.player)
        
    def interact(self, world):
        QM.progress_quests("on_interact", self, world)
        self.interaction(world)
        self.interacted = True
        
    def print_interaction(self, world):
        """Abstract method to be implemented, notifies the player that they can interact with this
        NPC.
        
        Parameters
        -----------
        world : World
            The world where this entity lives
        """
        post_output(f"- Interact with {self.name}")
        
    def interaction(self, world):
        """Abstract method for interacting with this entity, give a quest or fight
        
        Parameters
        -----------
        world : World
            The world where this entity lives
        """
        pass
