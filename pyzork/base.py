from .utils import post_output
from .errors import QuestStarted, QuestNonRepeatable

class QuestManager:
    def __init__(self, **kwargs):
        self._quests = kwargs.get("quests", {})
        self.active_quests = {}
        self.finished_quests = {x : 0 for x in self._quests}
        
    def add_quest(self, name, quest):
        if name in self._quests:
            raise KeyError("Duplicate quest name")
            
        self._quests[name] = quest
        self.finished_quests[name] = 0
        
    def remove_quest(self, name):
        del self._quests[name]
        del self.finished_quests[name]
        
    def print_quests(self):
        for quest in self.active_quests:
            post_output(f"{self.quest.name}\n{self.quest.description}\n")
            
    def start_quest(self, name):
        if name in self.active_quests:
            raise QuestStarted("This quest has already started")
            
        quest = self.finished_quests[name]()
        total = quest.repeatable()
        if self.finished_quests[name] >= total:
            raise QuestNonRepeatable(f"This quest cannot be done more than {total} time(s)") 
            
        self.active_quests[name] = quest
        
    def progress_quests(self, event, *args, **kwargs):
        rewards = []
                
        for name, quest in self.active_quests.items():
            try:
                done = getattr(quest, event)(*args, **kwargs)
            except AttributeError:
                continue
                
            if done:
                del self.active_quests[name]
                self.finished_quests[name] += 1
                # rewards.append(quest.reward)
                print(f"finished {name}")
                        
qm = QuestManager()
        
class Quest:
    def __init__(self):
        self.setup()
        
    def setup(self):
        pass
        
    def on_die(self, entity):
        pass
        
    def on_pickup(self, item):
        pass
        
    def on_discover(self, location):
        pass
        
    def reward(self, player):
        pass
        
    @classmethod
    def repeatable(cls):
        return 1

class QuestObject:
    pass