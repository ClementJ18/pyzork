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
