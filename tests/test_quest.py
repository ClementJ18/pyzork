import unittest
import pyzork

class TestQuest(unittest.TestCase):
    def setUp(self):
        pyzork.QM.clear()
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def test_standard_events(self):
        @pyzork.QM.add(id="OnDeath")
        class Quest1(pyzork.Quest):
            def on_death(self, entity):
                return True
        
        self.assertEqual(len(pyzork.QM.quests), 1)
        self.assertEqual(len(pyzork.QM.active_quests), 0)
        
        pyzork.QM.start_quest("OnDeath")
        
        self.assertEqual(len(pyzork.QM.active_quests), 1)
        
        pyzork.QM.progress_quests("on_death", None)
        
        self.assertEqual(len(pyzork.QM.active_quests), 0)
        self.assertEqual(pyzork.QM.finished_quests["OnDeath"], 1)
        
    def test_custom_events(self):
        @pyzork.QM.add(id="OnCustom")
        class Quest1(pyzork.Quest):
            def on_custom(self):
                return True
        
        self.assertEqual(len(pyzork.QM.quests), 1)
        self.assertEqual(len(pyzork.QM.active_quests), 0)
        
        pyzork.QM.start_quest("OnCustom")
        
        self.assertEqual(len(pyzork.QM.active_quests), 1)
        
        pyzork.QM.progress_quests("on_custom")
        
        self.assertEqual(len(pyzork.QM.active_quests), 0)
        self.assertEqual(pyzork.QM.finished_quests["OnCustom"], 1)
        
    def test_pause(self):
        @pyzork.QM.add(id="OnDeath")
        class Quest1(pyzork.Quest):
            def on_death(self, entity):
                return True
        
        self.assertEqual(len(pyzork.QM.quests), 1)
        self.assertEqual(len(pyzork.QM.active_quests), 0)
        
        pyzork.QM.start_quest("OnDeath")
        
        self.assertEqual(len(pyzork.QM.active_quests), 1)
        
        pyzork.QM.pause_quest("OnDeath")
        pyzork.QM.progress_quests("on_death", None)
        self.assertEqual(len(pyzork.QM.active_quests), 1)
        
        pyzork.QM.unpause_quest("OnDeath")
        pyzork.QM.progress_quests("on_death", None)
        
        self.assertEqual(len(pyzork.QM.active_quests), 0)
        self.assertEqual(pyzork.QM.finished_quests["OnDeath"], 1)
