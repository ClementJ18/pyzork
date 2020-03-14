from .actions import yes_or_no_parser
from .errors import ZorkError, EndGame

import sys

def get_user_input():
    """Method called by the library to gather user input, by default this simply calls input()"""
    return sys.modules["pyzork"].user_input()
    
def update_input(func):
    sys.modules["pyzork"].user_input = func

def post_output(string):
    sys.modules["pyzork"].print_function(string)
    
def update_output(func):
    sys.modules["pyzork"].print_function = func
    
def game_loop(world):
    while True:
        try:
            world.world_loop()
        except Exception as e:
            if isinstance(e, EndGame):
                world.end_game(e)
            else:
                world.error_handler(e)
    
def yes_or_no():
    while True:
        raw = get_user_input()
        reply = yes_or_no_parser(raw)
        if reply is True:
            return True
        
        if reply is False:
            return False
                    
        post_output("I didn't quite get that")
    
def find(predicate, seq):
    for element in seq:
        if predicate(element):
            return element
    return None
    
def get(iterable, **kwargs):
    def predicate(elem):
        for attr, val in kwargs.items():
            nested = attr.split('__')
            obj = elem
            for attribute in nested:
                obj = getattr(obj, attribute)

            if obj != val:
                return False
        return True

    return find(predicate, iterable)
