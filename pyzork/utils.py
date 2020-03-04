from .actions import yes_or_no_parser

def get_user_input():
    """Method called by the library to gather user input, by default this simply calls input()"""
    return input(">>>>> ")

def post_output(string):
    print(string)
    
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
