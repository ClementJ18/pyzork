import unittest
import pyzork

import sys

class TestAbilityDecorator(unittest.TestCase):
    def setUp(self):
        self.player = pyzork.Player(
            max_energy = 6,
            max_health = 5    
        )
        
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def test_fixed_cost(self):
        cost = 6
        damage = 4
        
        @pyzork.Ability.add(cost=cost, name="War Roar")    
        def WarRoarSpell(ability, user, target):
            """A terrible war cry that envigorates you"""
            target.take_pure_damage(damage)
            
        a = WarRoarSpell()
        
        self.assertEqual(a.name, "War Roar")
        self.assertEqual(a.description, "A terrible war cry that envigorates you")
        self.assertEqual(a.calculate_cost(self.player, self.player), cost)
        
        energy = self.player.energy
        health = self.player.health
        a.cast(self.player, self.player)
        
        self.assertEqual(self.player.energy, energy - cost)
        self.assertEqual(self.player.health, health - damage)
        
        a.cast(self.player, self.player)
        
        self.assertEqual(self.player.energy, energy - cost)
        self.assertEqual(self.player.health, health - damage)
        
    def test_callable_cost(self):    
        def callable_cost(ability, user, target):
            return user.max_energy * 0.75
            
        damage = 4
        cost = int(callable_cost(None, self.player, None))
            
        @pyzork.Ability.add(cost=callable_cost, description="Very loud yelling")    
        def WarRoarSpell(ability, user, target):
            target.take_pure_damage(damage)
            
        a = WarRoarSpell()
        
        self.assertEqual(a.name, "WarRoarSpell")
        self.assertEqual(a.description, "Very loud yelling")
        self.assertEqual(a.calculate_cost(self.player, self.player), cost)
        
        energy = self.player.energy
        health = self.player.health
        a.cast(self.player, self.player)
        
        self.assertEqual(self.player.energy, energy - cost)
        self.assertEqual(self.player.health, health - damage)
        
        a.cast(self.player, self.player)
        
        self.assertEqual(self.player.energy, energy - cost)
        self.assertEqual(self.player.health, health - damage)
        
class TestAbilitySubclass(unittest.TestCase):
    def setUp(self):
        self.player = pyzork.Player(
            max_energy = 6,
            max_health = 5    
        )
        
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def test_sublcass(self):
        cost = 6
        damage = 2
        
        class WarRoarSpell(Ability):
            """War Roar"""
            def cost(self, user, target):
                return cost
                
            def effect(self, user, target):
                """Yes"""
                target.take_pure_damage(damage)
                
        a = WarRoarSpell()
        
        self.assertEqual(a.name, "War Roar")
        self.assertEqual(a.description, "Yes")
        self.assertEqual(a.calculate_cost(self.player, self.player), cost)
        
        energy = self.player.energy
        health = self.player.health
        a.cast(self.player, self.player)
        
        self.assertEqual(self.player.energy, energy - cost)
        self.assertEqual(self.player.health, health - damage)
        
        a.cast(self.player, self.player)
        
        self.assertEqual(self.player.energy, energy - cost)
        self.assertEqual(self.player.health, health - damage)
