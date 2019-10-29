from enums import LimbTypes, StatEnum

class Equipment:
    def __init__(self, buff_type):
        self.name = self.__doc__
        self.description = self.calc.__doc__

        self.buff_type
        self.acceptable_limb_types

    def calc(self, player):
        """Abstract method that must be implemented by every piece of equipment, this is the method called by the battle logic
        to calculate the buff that the equipment provides to the user."""
        raise NotImplementedError


class Sword(Equipment):
    """Simple Sword"""
    buff_type = StatEnum.attack
    acceptable_limb_types = [LimbTypes.hands]

    def calc(self, player):
        """This simple bronze sword gives you a small bonus to your attack."""

        return 2

