from .abilities import Ability
from .modifiers import Modifier
from .base import QM, Quest
from .battle import Battle
from .entities import Player, NPC
from .enums import StatEnum, Direction
from .equipment import QuestItem, Consumable, Weapon, Armor, ShopItem, Inventory
from .levels import ExperienceLevels
from .world import World, Location, Shop

def print_function(text):
    print(text)

def user_input():
    return input(">>>>> ")
    
__version__ = '0.1'
