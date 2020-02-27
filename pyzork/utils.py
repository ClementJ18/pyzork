def get_user_input():
    return input(">>>>> ")

def post_output(string):
    print(string)
    
def yes_or_no():
    while True:
        raw = get_user_input()
        if "yes" in raw.lower():
            return True
        
        if "no" in raw.lower():
            return False
        
        post_output("I didn't quite get that")
        
def concat_docs(cls):
    """Does it look like I'm enjoying this?"""
    attributes = []

    def get_docs(parent):
        nonlocal attributes
        if parent.__name__ == 'object':
            return

        docs = parent.__doc__.splitlines()
        if "    Attributes" in docs:
            attributes = docs[docs.index("    Attributes") + 2:] + attributes

        source = inspect.getsource(parent.__init__)
        source = source[source.index('):'):]

        if 'super().__init__' in source:
            get_docs(parent.__base__)
        elif '__init__' in source:
            get_docs(parent.__base__.__base__)            

    get_docs(cls)
    original = cls.__doc__.splitlines()
    if not "    Attributes" in original:
        original.append("    Attributes")
        original.append("    -----------")

    final = original[:original.index("    Attributes") + 2]
    final.extend([x for x in attributes if x.strip()])
    cls.__doc__ = "\n".join(final)

    return cls
    
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
