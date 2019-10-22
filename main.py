from errors import EndgameReason, EndGame, EquipError
from utils import get_user_input
from enums import StatEnum

class Equipment:
    """Parent class for any piece of equipment. These are made to be equipped on bodies. Every piece of equipment: armor, weapon, shield, 
    ect... needs to inherit from this."""

    def __init__(self, **kwargs):
        pass

class Body:
    """Abstract class representing the body (and equipment) of an entity"""
    def equip(self, piece):
        try:
            limb = getattr(self, piece.limb)
        except AttributeError:
            raise EquipError(f"{piece.name} cannot be equipped on this character")

        limb = piece
        return f"Successfully equipped {piece.name}"

class Entity:
    """Abstract class representing an entity, can be an NPC, a player or an enemy."""
    def __init__(self, **stats):
        self.base_max_health = stats.get("base_max_health")
        self.base_damage = stats.get("base_damage")
        self.base_defense = stats.get("base_defense")

        self._health = stats.get("base_health", self.base_max_health)

        self.name = self.__doc__
        self.description = self.__init__.__doc__
        self.body = stats.get("body")

        self.buffs = []

    def interact(self):
        """Abstract method for interacting with this entity, give a quest, open a shop or fight."""
        raise NotImplementedError

    @property
    def attack(self):
        """This method compiles all the buffs, equipment, attributes to generate the attack stat of a unit."""
        return self.base_damage + sum([x.calc(self) for x in self.buffs if x.type == StatEnum.attack])
        
    @property
    def defense(self):
        """This method compiles all the buffs, equipment, attributes to generate the defense stat of a unit."""
        return self.base_defense + sum([x.calc(self) for x in self.buffs if x.type == StatEnum.defense])

    @property
    def max_health(self):
        """This method compiles all the buffs, equipment, attributes to generate the max health stat of a unit."""
        return self.base_max_health + sum([x.calc(self) for x in self.buffs if x.type == StatEnum.max_health])

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

    def is_alive(self):
        return self.health > 0

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
            base_health=100,
            body=Body()
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
    def __init__(self, **stats):
        super().__init__(**stats)

    def battle_logic(self, battle):
        """This method implement the behavior of enemies during battle. A basic logic is aready implemented which just attacks the player. 
        For boss battles this method is overwritten to implement more complex logic.
        This method takes the entire battle instance as the argument and therefore has full unrestricted access to the entire context
        of the battle, make full use of that."""
        self.do_attack(battle.player)

class Battle:
    def __init__(self, player, enemies, area):
        self.player = player
        self.enemies = enemies
        self.area = area

        self.turn = 0

    def battle(self):
        while player.is_alive():
            self.player_turn()
            for enemy in enemies:
                self.enemy_turn(enemy)

            self.end_turn()

    def end_turn(self):
        self.turn += 1

        buffs = [self.player.buffs, *[enemy.buffs for enemy in self.enemies]]
        for buff in buffs:
            buff.end_turn()

    def player_turn(self):
        pass

    def enemy_turn(self, enemy):
        enemy.battle_logic(self)
    