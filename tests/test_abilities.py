import unittest
import pyzork

class TestAbility(unittest.TestCase):
    def setUp(self):
        self.player = pyzork.Player(
            max_energy = 6,
            max_health = 5    
        )
        
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def check_spell(self):
        self.assertEqual(self.spell.calculate_cost(self.player, self.player), self.cost)
        
        energy = self.player.energy - self.cost
        health = self.player.health - self.damage
        self.spell.cast(self.player, self.player)
        
        self.assertEqual(self.player.energy, energy)
        self.assertEqual(self.player.health, health)
        
        self.spell.cast(self.player, self.player)
        
        self.assertEqual(self.player.energy, energy)
        self.assertEqual(self.player.health, health)
        
    def test_fixed_cost(self):
        self.cost = 6
        self.damage = 4
        
        @pyzork.Ability.add(cost=self.cost, name="War Roar")    
        def WarRoarSpell(ability, user, target):
            """A terrible war cry that envigorates you"""
            target.take_pure_damage(self.damage)
            
        self.spell = WarRoarSpell()
        
        self.assertEqual(self.spell.name, "War Roar")
        self.assertEqual(self.spell.description, "A terrible war cry that envigorates you")
        self.check_spell()
    
    def test_callable_cost(self):    
        def callable_cost(ability, user, target):
            return user.max_energy * 0.75
            
        self.damage = 4
        self.cost = int(callable_cost(None, self.player, None))
            
        @pyzork.Ability.add(cost=callable_cost, description="Very loud yelling")    
        def WarRoarSpell(ability, user, target):
            target.take_pure_damage(self.damage)
            
        self.spell = WarRoarSpell()
        
        self.assertEqual(self.spell.name, "WarRoarSpell")
        self.assertEqual(self.spell.description, "Very loud yelling")
        
        self.check_spell()
        
    def test_sublcass(self):
        self.cost = 6
        self.damage = 2
        
        class WarRoarSpell(pyzork.Ability):
            """War Roar"""
            def cost(ability, user, target):
                return self.cost
                
            def effect(ability, user, target):
                """Yes"""
                target.take_pure_damage(self.damage)
                
        self.spell = WarRoarSpell()
        
        self.assertEqual(self.spell.name, "War Roar")
        self.assertEqual(self.spell.description, "Yes")
        
        self.check_spell()
        
    def test_blank_description(self):
        cost = 6
        damage = 4
        
        @pyzork.Ability.add(cost=cost)    
        def WarRoarSpell(ability, user, target):
            target.take_pure_damage(damage)
        
        a = WarRoarSpell()
        
        self.assertEqual(a.name, "WarRoarSpell")
        self.assertEqual(a.description, None)
