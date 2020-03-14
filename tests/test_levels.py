import unittest
import pyzork

class TestLevels(unittest.TestCase):
    def setUp(self):
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def test_hardcoded_req(self):
        req = [2, 33, 56, 23, 78]
        
        basic = pyzork.ExperienceLevels(requirements=req)
      
        for i in range(basic.max_level):
            self.assertEqual(basic.level, i)
            basic += req[i]
        
    def test_flexible_req(self):
        basic = pyzork.ExperienceLevels(requirement=100, modifier=1.2, max_level=10)
        
        req = 100
        level = 1
        
        for _ in range(basic.max_level):
            basic += req
            self.assertEqual(basic.level, level)
            level += 1
            req *= 1.2            
        
    def test_flexible_reward(self):
        def basic_reward(levels):
            levels.entity.base_attack *= 1.2

        basic = pyzork.ExperienceLevels(
            requirement=100,
            modifier=1.2,
            max_level=10,
            reward=basic_reward
        )
        
        p = pyzork.Player(experience=basic, attack=4)
        
        for _ in range(basic.max_level):
            attack  = p.attack * 1.2
            basic += basic.remaining
            
            # self.assertEqual(p.health, health)
            self.assertEqual(p.attack, attack)
