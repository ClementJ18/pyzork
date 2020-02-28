from .enums import Direction

import nltk

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words("english"))

def direction_parser(choice, world : "World") -> Direction:
    acceptable_words = ["go", "walk", "run", "enter", "exit", "move"]
    choice = [x for x in choice.split() if x not in STOPWORDS]
    if any(x for x in choice if x in acceptable_words):
        exits = [x for x in world.current_location.exits.items() if x[1] is not None]
        if len(exits) == 1:
            return exits[0][0]
            
        acceptable_directions = [x.name for x in Direction]
        for word in choice:
            if word in acceptable_directions:
                return Direction[word]
                
        for direction, exit in exits:
            if exit is None:
                continue
                
            if any(x for x in choice if x in exit.name.lower()):
                return direction
    
def view_parser(choice, player):
    pass
    
def use_item_parser(choice, player):
    pass
    
def equip_item_parser(choice, player):
    pass
    
def use_ability_parser(choice, player):
    pass
    
def interact_parser(choice, location):
    pass

def shop_parser(choice, player, shop):
    pass
    
def clean(raw):
    return raw.lower().strip()