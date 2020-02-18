from pyzork.levels import ExperienceLevels
from pyzork.entities import Player
from pyzork.utils import post_output

from .example_equipment import Sword

def reward(levels):
    levels.player.add_to_inventory(Sword())
    post_output(f"You are now level {levels.level}")

e = ExperienceLevels(requirement=100, modifier=1.2, max_level=10, reward=reward)
p = Player(experience=e)
