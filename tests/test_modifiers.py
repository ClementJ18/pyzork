import unittest
import pyzork

class TestModifier(unittest.TestCase):
    def setUp(self):
        self.player = pyzork.Player(
            max_energy = 6,
            max_health = 10,
            damage = 6,
            defense = 6    
        )
        self.stat = pyzork.StatEnum.null
        self.duration = 0
        self.buff = 0
        self.damage = 0
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def check_modifier(self):
        stat = getattr(self.player, self.stat.name, 0)
        self.player.add_modifier(self.modifier)
        
        self.assertIn(hash(self.modifier), self.player.modifiers)
        self.assertEqual(getattr(self.player, self.stat.name, 0), stat + self.buff)
                    
        health = self.player.health
        for _ in range(self.duration + 1):
            self.player.end_turn()            
        
        self.assertEqual(self.player.health, health - (self.damage * self.duration))
        self.assertNotIn(hash(self.modifier), self.player.modifiers)
        self.assertEqual(getattr(self.player, self.stat.name, 0), stat)
        
    def test_buff(self):
        self.stat = pyzork.StatEnum.defense
        self.duration = 3
        self.buff = -3
        
        @pyzork.Modifier.add_buff(stat_type=self.stat, duration=self.duration)
        def InsultDebuff(debuff, target):
            """You feel insulted and as a result the target's defense is lowered."""
            return self.buff
            
        self.modifier = InsultDebuff()
        
        self.assertEqual(self.modifier.name, "InsultDebuff")
        self.assertEqual(self.modifier.description, "You feel insulted and as a result the target's defense is lowered.")    
        
        self.check_modifier()

    def test_effect(self):
        self.duration = 3
        self.damage = 3
        
        @pyzork.Modifier.add_effect(duration=self.duration, name="Poisoned")
        def PoisonDamage(effect, target):
            """Lose 3 health every turn."""
            target.take_pure_damage(self.damage)
            
        self.modifier = PoisonDamage()
            
        self.assertEqual(self.modifier.name, "Poisoned")
        self.assertEqual(self.modifier.description, "Lose 3 health every turn.")    
        
        self.check_modifier()        
        
    def test_buff_and_effect(self):
        self.duration = 3
        self.damage = 3
        self.stat = pyzork.StatEnum.defense
        self.buff = -3
        
        @pyzork.Modifier.add_buff(stat_type=self.stat, duration=self.duration, name="A Toxic Insult")
        def InsultDebuff(debuff, target):
            """You feel insulted and as a result the target's defense is lowered."""
            return self.buff
            
        @InsultDebuff.add_effect(duration=5)
        def add_effect_insult(effect, target):
            """Lose 3 health every turn."""
            target.take_pure_damage(self.damage)
            
        self.modifier = InsultDebuff()
            
        self.assertEqual(self.modifier.name, "A Toxic Insult")
        self.assertEqual(self.modifier.description, "You feel insulted and as a result the target's defense is lowered. Lose 3 health every turn.")
        
        self.check_modifier()

    def test_subclass(self):
        self.duration = 3
        self.damage = 3
        self.stat = pyzork.StatEnum.defense
        self.buff = -3
        
        class InsultDebuff(pyzork.Modifier):
            """A very toxi insult"""
            def __init__(thing):
                super().__init__(stat_type=self.stat, duration=self.duration)

            def effect(effect, target):
                """Lose 3 health every turn because of this."""
                target.take_pure_damage(self.damage)
                
            def buff(buff, target):
                """You feel insulted and as a result the target's defense is lowered."""
                return self.buff
                
        self.modifier = InsultDebuff()
        
        self.assertEqual(self.modifier.name, "A very toxi insult")
        self.assertEqual(self.modifier.description, "You feel insulted and as a result the target's defense is lowered. Lose 3 health every turn because of this.")
        
        self.check_modifier()
