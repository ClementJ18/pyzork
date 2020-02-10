
class Action:
    def __init__(self, keywords=[]):
        self.keywords = keywords
        
    def check(self, string):
        return string in self.keywords
        
    def action(self):
        raise NotImplementedError
        
    def text_parse(self, string):
        raise NotImplementedError
        
    def add(self, func, keywords):
        self.keywords = keywords
        self.action = func
        
class SystemMove(Action):
    keywords = ["go", "walk", "move", "run", "enter", "exit"]
    
    def text_parse(self, string):
        
    
class SystemAttack(Action):
    pass 
    
class SystemAbility(Action):
    pass
    
class SystemItem(Action):
    pass
    
class SystemEquipment(Action):
    pass
    
class SystemMenu(Action):
    pass
    
