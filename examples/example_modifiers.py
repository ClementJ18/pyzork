from pyzork.modifiers import Modifier
from pyzork.enums import StatEnum

class WarRoarBuff(Modifier):
    """War Roar of War"""
    def __init__(self):
        super().__init__(stat_type=StatEnum.attack, duration=5)

    def buff(self, target):
        """You are entranced by the roar and your attack is increased for a short time"""
        return 2

@Modifier.add_buff(stat_type=StatEnum.defense, duration=3)
def InsultDebuff(self, target):
    """You feel insulted and as a result the target's defense is lowered."""
    return -3

class InsultBuff(Modifier):
    """Insult"""
    def __init__(self):
        super().__init__(stat_type=StatEnum.attack, duration=5)

    def buff(self, target):
        """You feel insulted and as a result the target's attack is increased."""
        return 1

class FireDebuff(Modifier):
    """Burnt"""

    def __init__(self):
        super().__init__(stat_type=StatEnum.max_health, duration=5)

    def buff(self, target):
        """The burns leaves a scar, reducing the target's maximum health."""
        return -5

class PoisonEffect(Modifier):
    """Poison"""
    def __init__(self):
        super().__init__(duration=5)

    def effect(self, player):
        """Lose 3 health every turn."""
        self.player.take_pure_damage(3)

class BurntEffect(Modifier):
    """Burnt"""

    def __init__(self):
        super().__init__(duration=5, stat_type=StatEnum.attack)
        
    def buff(self, player):
        """The burn makes it hard to fight"""
        return -2

    def effect(self, player):
        """Lose 2 health every turn"""
        self.player.take_pure_damage(2)
