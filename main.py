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

        for buff, effect in zip(self.player.buffs, self.player.effects):
            buff.end_turn()
            effect.end_turn(self.player)

        for enemy in self.enemies:
            for buff, effect in zip(enemy.buffs, enemy.effects):
                buff.end_turn(enemy)
                effect.end_turn(self.player)

    def player_turn(self):
        pass

    def enemy_turn(self, enemy):
        enemy.battle_logic(self)
    