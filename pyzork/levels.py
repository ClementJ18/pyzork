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
        
        if "reward" in kwargs:
            self.standard_reward = kwargs.get("reward")
            
        self.rewards = [self.standard_reward for x in range(self.max_level)]
        
        if "rewards" in kwargs:
            rewards = kwargs.get("rewards")
            for req, reward in rewards.items():
                self.rewards[req-1] = reward
                
    def __repr__(self):
        return f"<ExperienceLevels exp={self.experience} req={self.requirement} level={self.level}>"
            
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
        self.level += 1
        self.rewards[self.level](self)
        
    def standard_reward(self, player):
        post_output(f"You leveled up! You are now level {self.level}")
        
    def __add__(self, value):
        self.experience += value
        return self            
    