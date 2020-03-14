import unittest
import pyzork

Goblin = pyzork.NPC.from_dict(name="Goblin", max_health=10, attack=2)
BigGoblin = pyzork.NPC.from_dict(name="BigGoblin", max_health=15, attack=3)

player = pyzork.Player(max_health=50, attack=5, defense=1)
BattleField = pyzork.Location.from_dict(name="BattleField", enemies=[Goblin, BigGoblin])

class TestBattle(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_full(self):                
        bf = BattleField()
        battle = pyzork.Battle(player=player, enemies=bf.enemies, location=bf)
        
        strings = [
            "attack the goblin",
            "attack the big goblin",
            "attack the goblin",
            "attack the big goblin",
            "attack the big goblin",
        ]
        
        self.index = 0
        
        def new_input():
            i = strings[self.index]
            self.index += 1
            
            return i
        
        pyzork.utils.update_input(new_input)
        pyzork.utils.update_output(lambda x: None)
        battle.battle_loop()
        
        self.assertFalse(bf.enemies)
        self.assertFalse(battle.alive)
        self.assertEqual(len(battle.dead), 2)
        
    def test_priorities(self):
        def custom_priorities(battle):
            turns = []
            for enemy in battle.alive:
                turns.append(battle.player)
                turns.append(enemy)
        
        bf = BattleField()
        battle = pyzork.Battle(player=player, enemies=bf.enemies, location=bf, priorities=custom_priorities)
        
        self.assertEqual(len(battle.priorities()), 4)
 