import enum

class StatEnum(enum.Enum):
    attack = enum.auto()
    defense = enum.auto()
    max_health = enum.auto()
    health = enum.auto()

class EndgameReason(enum.Enum):
    zero_health = enum.auto()
