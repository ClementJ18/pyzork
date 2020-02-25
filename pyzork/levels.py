from .utils import post_output
from .base import QM

import math

class ExperienceLevels:
    """ExperienceLevels are handlers for an entity's epxerience and rank. You can pass a hardcoded list of 
    experience requirements and rewards or you can generate those  automatically using certain parameters.
    
    Parameters
    -----------
    requirements : Optional[List[int]]
        A list of int meant to represent the amount of xp it takes to get from one rank to the next. The first
        representing the amount it takes to go from level 0 to level 1. If this parameter is provided you won't
        need to provide either of the `max_level`, `requirement` or `modifier` arguments.
    requirement : Optional[int]
        A single int, representing the xp it takes to get from level 0 to level 1. All further requirements will
        be derived from this one and the modifier. If this argument is provided then `modifier` and `max_level`
        must also be provided.
    max_level : Optional[int]
        A single int, meant to represent the maximum leve that can be reached, once that level is reached
        experience can still be acumulated but no level up event will occur and no extra rewards will be granted.
    modifier : Optional[float]
        A float which defines by how much the next requirement is increased by. For example, with a starting
        requirement of 100 and a modifier of 1.2, from level 0 to 1 you'll need a 100 exp, from 1 to 2 you'll
        need 120, from 2 to 3 you'll need 144 and so on.
    rXX : Optional[int]
        An abstract keyword argument, there is not literal rXX argument, rather the XX can be replaced with 
        the level of the requirement you wish to change, this allows you automatically generate the requirements
        but still have some control over the system.
    rewards : Optional[List[Callable[[ExperienceLevels], None]]]
        A list of functions to be called when a user levels up, with the first element being when the user
        goes from level 0 to level 1. This allows you complete control over the rewards. If you provide this
        parameter you do not have to provide `reward`.
    reward : Optional[Callable[[ExperienceLevels], None]]
        A single reward, which will be used as the default for every level up. If you provide this argument you
        do not have to provide `rewards`. You can then further customise individual level up rewards using the
        `lXX` keywords where XX is the level they need to reach to get the reward.
    lXX : Optional[Callable[[ExperienceLevels], None]]
        This is an abstract keyword argument, there is no literal lXX argument, rather you can replace XX with
        the level of the reward you wish to change. This argument takes a standard reward callable.
        
    Attributes
    -----------
    max_level : int
        The max level the class (and by extension the attached entity) can reach.
    experience : int
        The current experience the entity has
    requirement : int
        How much experience the entity needs to have total to reach the next level
    remaining : int
        How much experience the entity still needs to reach the next level
    level : int
        The entity's current level (starts at 0)
    
    """
    def __init__(self, **kwargs):
        if "requirements" in kwargs:
            self.requirements = kwargs.pop("requirements")
            self.max_level = len(self.requirements)
        else:
            modifier = kwargs.pop("modifier")
            requirement = kwargs.pop("requirement")
            
            self.max_level = kwargs.pop("max_level")
            self.generate_levels(requirement, modifier)
            
        self.level = kwargs.pop("level", 0)
        self._experience = kwargs.pop("experience", 0)
        self.entity = None
        
        self.standard_reward = kwargs.pop("reward", self.standard_reward)    
        self.rewards = kwargs.pop("rewards", [self.standard_reward for x in range(self.max_level)])
        
        for kwarg in kwargs:
            if kwarg.startswith(("l", "r")):
                level = kwarg[1:]
                if not level.isdigit() or 0 > int(level) > self.max_level:
                    return
                    
                index = int(level) - 1
                if kwarg.startswith("l"):
                    self.rewards[index] = kwargs.pop(kwarg)
                else:
                    self.requirements[index] = kwargs.pop(kwarg)
                
    def __repr__(self):
        return f"<ExperienceLevels exp={self.experience}/{self.requirement} level={self.level}>"
            
    def generate_levels(self, requirement, modifier):
        self.requirements = [requirement]
        for _ in range(self.max_level - 1):
            requirement = int(requirement * modifier)
            self.requirements.append(requirement)   
    
    def set_entity(self, entity : "Entity"):
        self.entity = entity     
            
    @property
    def requirement(self):
        if self.level == self.max_level:
            return math.inf
        
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
            QM.progress_quests("on_level", self)
            
        self._experience = value
        
    def level_up(self):
        self.level += 1
        self.rewards[self.level - 1]()
        
    def standard_reward(self):
        post_output(f"You leveled up! You are now level {self.level}")
        
    def __add__(self, value):
        self.experience += value
        return self            
    