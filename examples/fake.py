from pyzork.core import BasicAdventure
from pyzork.classes import BasicRogue, BasicMage

from myadventure import BarbarianClass


adventure = BasicAdventure("The Legend of Zork")
adventure.set_class(BasicRogue, BasicMage, BarbarianClass)

if __name__ == '__main__':
    adventure.start()
