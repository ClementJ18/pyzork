from enums import EndGameReason

class EndGame(Exception):
    def __init__(self, message, victory, reason):
        self.msg = message
        self.victory = victory
        self.reason = reason

class EquipError(Exception):
    pass

class NoEnergy(Exception):
    pass
