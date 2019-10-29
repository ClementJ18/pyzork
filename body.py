from enums import LimbTypes
from equipments import NullType
from errors import EquipError
from enums import LimbTypes

class Limb:
    def __init__(self, **kwargs):
        self.limb_types = kwargs.get("limb_types")

        self.current = NullType()

        self.name = self.__doc__
        self.description = ""

    def equip(self, piece):
        if any(x in self.limb_types for x in piece.acceptable_limbs):
            self.current = piece
        else:
            raise EquipError(f"{piece.name} cannot be equipped on this limb")

    def unequip(self):
        if isinstance(self.current, NullType):
            raise EquipError(f"This limb doesn't have anything equipped")

        self.current_equipment = NullType()


class Hand(Limb):
    """Hand"""
    def __init__(self):
        super().__init__(
            limb_types=[LimbTypes.hands]
        )

