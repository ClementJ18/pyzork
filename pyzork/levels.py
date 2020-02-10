from .utils import post_output

class ExperienceLevels:
    def __init__(self, **kwargs):
        if "requirements" in kwargs:
            self.requirements = kwargs.get("requirements")
            self.max_level = len(self.requirements)
        else:
            modifier = kwargs.get("modifier")
            requirement = kwargs.get("requirement")
            
            self.max_level = kwargs.get("max_level")
            self.generate_levels(requirement, modifier)
            
        self.level = 0
        self._experience = 0
        self.current_rewards = []
        self.player = None
        self.rewards = [[] for x in range(self.max_level)]
        
        if "rewards" in kwargs:
            rewards = kwargs.get("rewards")
            for req, reward in rewards.items():
                self.rewards[req-1].extend(reward)
            
    def generate_levels(self, requirement, modifier):
        self.requirements = [requirement]
        for level in range(self.max_level):
            requirement = int(requirement * modifier)
            self.requirements.append(requirement)        
            
    def set_player(self, player):
        self.player = player
            
    @property
    def requirement(self):
        return self.requirements[self.level]
        
    @property
    def remaining(self):
        return self.requirement - self.experience
            
    @property
    def experience(self):
        return self._experience
        
    @experience.setter
    def experience(self, value):
        if value < 0:
            value = 0
        
        while value >= self.requirement:
            value -= self.requirement
            self.level_up()
            
        self._experience = value
        
    def level_up(self):
        self.player.process_rewards(self.rewards[self.level])
        self.level += 1
        post_output(f"You leveled up! You are now level {self.level}")
        
    def __add__(self, value):
        self.experience += value
        return self
        
    
basic = ExperienceLevels(requirement=100, modifier=1.2, max_level=10)
            
    