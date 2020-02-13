class ZorkError(Exception):
    pass

class EndGame(ZorkError):
    def __init__(self, message, victory, reason):
        self.msg = message
        self.victory = victory
        self.reason = reason
        
class QuestStarted(ZorkError):
    """Quest is already started"""
    pass
    
class QuestNonRepeatable(ZorkError):
    pass

class EquipError(ZorkError):
    pass

class NoEnergy(ZorkError):
    pass
