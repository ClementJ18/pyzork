from .utils import post_output
from .errors import QuestStarted, QuestNonRepeatable

class QuestManager:
    def __init__(self, **kwargs):
        self.quests = kwargs.get("quests", {})
        self.active_quests = {}
        self.finished_quests = {x : 0 for x in self.quests}
        self.pending_rewards = []
        
    def add(self, **kwargs):
        def wrapper(quest):
            name = kwargs.get("name", quest.get_name())
            repeat_int = kwargs.get("repeatable", 1)
            
            def repeatable(self):
                return repeat_int
                
            quest.repeatable = repeatable
            qm.add_quest(name, quest)
            
            return quest 
                   
        return wrapper
        
    def add_quest(self, name, quest):
        if name in self.quests:
            raise KeyError("Duplicate quest name")
            
        self.quests[name] = quest
        self.finished_quests[name] = 0
        
    def remove_quest(self, name):
        del self.quests[name]
        del self.finished_quests[name]
        
    def print_quests(self):
        for quest in self.active_quests:
            post_output(f"{self.quest.name}\n{self.quest.description}\n")
            
    def start_quest(self, name):
        if name in self.active_quests:
            raise QuestStarted("This quest has already started")
            
        quest = self.quests[name]()
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
                self.pending_rewards.append(quest)
                print(f"finished {name}")
                
    def get_finished(self, name):
        return self.finished_quests[name] 
        
    def process_rewards(self, player, world):
        while self.pending_rewards:
            quest = self.pending_rewards.pop(0)
            quest.reward(player, world)
           
                        
qm = QuestManager()
        
class Quest:
    def __init__(self):
        self.setup()
        
    def setup(self):
        pass
        
    def on_kill(self, entity):
        pass
        
    def on_pickup(self, item):
        pass
        
    def on_discover(self, location):
        pass
        
    def on_interact(self, entity):
        pass
        
    def reward(self, player):
        pass
        
    def repeatable(self):
        return 1
        
    @classmethod
    def get_name(cls):
        return cls.__name__

class QuestObject:
    pass