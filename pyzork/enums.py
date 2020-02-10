from enum import IntEnum, auto

class StatEnum(IntEnum):
    null = auto()
    attack = auto()
    defense = auto()
    max_health = auto()
    health = auto()
    max_energy = auto()
    energy = auto()

class EndgameReason(IntEnum):
    zero_health = auto()
    failed_objecive = auto()

class Direction(IntEnum):
    north = auto()
    south = auto()
    west = auto()
    east = auto()
    
    @classmethod
    def opposite(cls, direction):
        v = direction.value
        return cls(v-1) if v % 2 == 0 else cls(v+1)
