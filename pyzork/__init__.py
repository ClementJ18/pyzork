from .abilities import Ability
from .modifiers import Modifier
from .actions import *
from .base import QM, Quest
from .battle import Battle
from .entities import Player, NPC
from .enums import StatEnum, Direction
from .equipment import QuestItem, Consumable, Weapon, Armor
from .levels import ExperienceLevels
from .world import World

def print_function(text):
    print(text)

def user_input():
    return input(">>>>> ")
