from pyzork.levels import ExperienceLevels
from pyzork.utils import post_output

from .example_equipement import Sword

basic = ExperienceLevels(requirement=100, modifier=1.2, max_level=10)

def l5_reward(levels, player):
    post_output("You leveled up to 5!")
    player.add_to_inventory(Sword())

basic_l5_reward = ExperienceLevels(requirement=100, modifier=1.2, max_level=10, l5=l5_reward)
