import pyzork

from pyzork.utils import post_output

class EnemyWithShield(pyzork.NPC):
    """This NPC has a regenerative shield which heals by a small amount every turn, any
    damage taken is first dealt to the shield and than to the health. This showcases some
    of the more advanced stuff you can do with this library. The shield benefits partially
    from healing effects"""
    
    def __init__(self, **kwargs):
        self.max_shield = kwargs.get("max_shield", 0)
        self._shield = kwargs.get("shield", self.max_shield)
        
        super().__init__(**kwargs)
        
    @property
    def shield(self):
        max_shield = self.max_shield
        if self._shield > max_shield:
            self._shield = max_shield
            return self._shield
        
        return self._shield

    @shield.setter
    def shield(self, value):
        current = self._shield
        if value <= 0:
            self._shield = 0
        elif value > self.max_shield:
            self._shield = self.max_shield
        else:
            self._shield = int(value)
            
        if current < value:
            post_output(f"{self.name} gains {value - current} shield")
        else:
            post_output(f"{self.name} loses {current - value} shield")
    
    def take_pure_damage(self, value):
        if self.shield >= value:
            self.shield-= value
        elif self.shield > 0:
            value -= self.shield
            self.shield = 0
            self.health -= value
        else:
            self.health -= value
        
    def restore_health(self, value):
        self.health += value
        self.shield += int(value * 0.1)
        
    def restore_shield(self, value):
        self.shield += value
        
    def end_turn(self):
        """End this entity's turn, decrementing all the modifier's durations and removing the expired ones."""
        for name in list(self.modifiers.keys()):
            modifier = self.modifiers[name]
            modifier.end_turn(self)
            if modifier.is_expired():
                del self.modifiers[name]
                
        self.shield += self.max_shield * 0.1

class BigGoblin(EnemyWithShield):
    def __init__(self):
        super().__init__(
            max_health=10,
            max_shield=10,
            attack=3
        )
        
e = BigGoblin()
p = pyzork.Player(max_health=25, attack=4)
