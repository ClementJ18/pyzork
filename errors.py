from enums import EndGameReason

class EndGame(Exception):
    def __init__(self, message, victory):
        self.msg = message
        self.victory = victory

class EquipError(Exception):
    pass
