from pyzork.levels import ExperienceLevels
from pyzork.entities import Player
from pyzork.utils import post_output

from .example_equipment import Sword

def reward(levels):
    levels.player.add_to_inventory(Sword())
    post_output(f"You are now level {levels.level}")
    
def special_level5_reward(levels):
    post_output(f"Your power grows! You have reached level 5")
    levels.player.base_damage *= 1.5
    levels.player.base_defense *= 1.5

e = ExperienceLevels(requirement=100, modifier=1.2, max_level=10, reward=reward, l5=special_level5_reward)
p = Player(experience=e)
