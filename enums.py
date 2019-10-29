import enum

class StatEnum(enum.Enum):
    null = enum.auto()
    attack = enum.auto()
    defense = enum.auto()
    max_health = enum.auto()
    health = enum.auto()
    max_energy = enum.auto()
    energy = enum.auto()

class EndgameReason(enum.Enum):
    zero_health = enum.auto()

class LimbTypes(enum.Enum):
    arms = auto()
    legs = auto()
    head = auto()
    torso = auto()
    fingers = auto()
    neck = auto()
    body = auto()
    hands = auto()
