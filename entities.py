from enums import StatEnum
from errors import EndgameReason, EndGame


class Entity:
    """Abstract class representing an entity, can be an NPC, a player or an enemy."""
    def __init__(self, **stats):
        self.base_max_health = stats.get("base_max_health", 0)
        self._health = stats.get("base_health", self.base_max_health)

        self.base_damage = stats.get("base_damage", 0)
        self.base_defense = stats.get("base_defense", 0)

        self.base_max_energy = stats.get("base_max_energy", 0)
        self._energy = stats.get("base_energy", self.base_max_energy)

        self.limbs = stats.get("limbs", [])

        self.name = self.__doc__
        self.description = self.__init__.__doc__

        self.buffs = []

    def interact(self):
        """Abstract method for interacting with this entity, give a quest, open a shop or fight."""
        raise NotImplementedError

    def _big_calc(self, player, stat):
        """Calculate all the modifiers for a stat"""
        return sum([x.calc(self) for x in self.buffs if x.type == stat]) 
            + sum([x.calc(self) for x in self.limbs if x.current.buff_type == stat])

    @property
    def attack(self):
        """This method compiles all the buffs, equipment, attributes to generate the attack stat of a unit."""
        return self.base_damage + self._big_calc(self, StatEnum.attack)
        
    @property
    def defense(self):
        """This method compiles all the buffs, equipment, attributes to generate the defense stat of a unit."""
        return self.base_defense + self._big_calc(self, StatEnum.defense)

    @property
    def max_health(self):
        """This method compiles all the buffs, equipment, attributes to generate the max health stat of a unit."""
        return self.base_max_health + self._big_calc(self, StatEnum.max_health)

    @property
    def max_energy(self):
        """This method compiles all the buffs, equipment, attributes to generate the max health stat of a unit."""
        return self.base_max_energy + self._big_calc(self, StatEnum.max_energy)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value <= 0:
            self._health = 0
        elif value > self.max_health:
            self._health = self.max_health
        else:
            self._health = value

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        if value <= 0:
            self._energy = 0
        elif value > self.max_energy:
            self._energy = self.max__energy
        else:
            self._energy = value

    def is_alive(self):
        return self.health > 0

    def can_cast(self, value):
        return value >= self.energy

    def do_attack(self, target):
        target.health -= max(1, self.attack - target.defense)

class Player(Entity):
    """You"""
    def __init__(self):
        """A normal person with an extrodinary destiny... probably."""
        super().__init__(
            base_max_health=100,
            base_damage=5,
            base_defense=0,
            base_max_energy=25,
        )

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value <= 0:
            self._health = 0
            raise EndGame("Look like you've died, better luck next time.", victory=False, reason=EndgameReason.zero_health)
        elif value > self.max_health:
            self._health = self.max_health
        else:
            self._health = value

class Enemy(Entity):
    def battle_logic(self, battle):
        """This method implement the behavior of enemies during battle. A basic logic is aready implemented which just attacks the player. 
        For boss battles this method is overwritten to implement more complex logic.
        This method takes the entire battle instance as the argument and therefore has full unrestricted access to the entire context
        of the battle, make full use of that."""
        self.do_attack(battle.player)
