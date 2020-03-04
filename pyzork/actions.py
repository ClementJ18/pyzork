from .enums import Direction

import nltk

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))
ACCEPTABLE_MOVEMENTS = ["go", "walk", "run", "enter", "exit", "move", "leave"]
ACCEPTABLE_INTERACTS = ["talk", "interact", "check", "look", "approach"]
ACCEPTABLE_ATTACKS = ["attack", "strike", "target"]
ACCEPTABLE_EQUIP = ["equip", "put"]
ACCEPTABLE_USE = ["use", "drink", "eat", "throw"]
ACCEPTABLE_CAST = ["use", "cast"]

ALIASES_VIEW = {
    "inventory": ["inv", "inventory", "items"],
    "stats": ["stats", "health", "energy", "attack", "damage", "hitpoints"]
}

ALIASES_SHOP = {
    "sell" : ["sell"],
    "buy": ["buy", "purchase"]
}

PLAYER = ["me", "myself", "i", "player"]
YES = ["yes", "y", "true"]
NO = ["no", "n", "false"]

POSITIONS = [["left"], ["center", "middle"], ["right"]]
    
def clean(raw):
    return raw.lower().strip()
    
def filter_stopword(text):
    return [x for x in clean(text).split() if x not in STOPWORDS]

def direction_parser(choice, current_location : "Location") -> Direction:
    """A bit more robust parser for picking a direction you want to go in. This parser works in the
    following way:
    
    #. Clean up user input and remove Stopwords.
    
    #. Check if the text contains any of the acceptable movement words such as "go", "walk", etc... If no matches are detected then the parser returns.
        
    #. If only one exit is possible then the direction of that exit is returned, else the parser continues below. (Could potentially be an issue if there are overlapping keywords)
        
    #. If one of the words is a cardinal direction or a number equivalent to one of the cardinal directions then return that, else the parser continues below
        
    #. Compare every location and pick the one where the most words of the user input match the name
        
    Possible Improvements
    ======================
    * Find a larger list of ACCEPTABLE_MOVEMENTS words
    * Take into consideration each exit's `print_interaction`  
    """
    choice = filter_stopword(choice)
    exits = [x for x in current_location.exits.items() if x[1] is not None]
    if any(x for x in choice if x in ACCEPTABLE_MOVEMENTS):
        if len(exits) == 1:
            return exits[0][0]
            
        acceptable_directions = [x.name for x in Direction] + [str(x.value) for x in Direction]
        for word in choice:
            if word in acceptable_directions:
                return Direction(int(word)) if word.isdigit() else Direction[word]
        
        best_dir = (None, 0)
        for direction, exit in exits:
            if exit is None:
                continue
                
            new_dir = len([x for x in choice if x in exit.name.lower()])
            if new_dir > best_dir[1]:
                best_dir = (direction, new_dir)
        
        return best_dir[0]

def interact_parser(choice : str, location : "Location") -> "Entity":
    """A bit more robust parser for picking a npc to interact with. This parser works in the
    following way:
    
    #. Clean up user input and remove Stopwords.
    
    #. Check if the text contains any of the acceptable interaction words such as "talk", "interact", etc... If no matches are detected then the parser returns.
    
    #. If only one interaction is possible then the npc of that interaction is returned, else the parser continues below. (Could potentially be an issue if there are overlapping keywords)
    
    #. Compare every npc and pick the one where the most words of the user input match the name
        
    Possible Improvements
    ======================
    * Find a larger list of ACCEPTABLE_INTERACTS words
    * Take into consideration each npc's `print_interaction`  
    """
    choice = filter_stopword(choice)
    if any(x for x in choice if x in ACCEPTABLE_INTERACTS):
        if len(location.npcs) == 1:
            return location.npcs[0]
            
        best_interaction = (None, 0)
        for npc in location.npcs:
            new_interaction = len([x for x in choice if x in npc.name.lower()])
            if new_interaction > best_interaction[1]:
                best_interaction = (npc, new_interaction)
              
        return best_interaction[0]
        

def view_parser(choice : str, player : "Player") -> str:
    """A simple parser for picking a player property to view. This parser works in the
    following way:
    
    #. Clean up user input and remove Stopwords.
    
    #. For each possible alias in ALIASES_VIEW check if the user input contains any, if it does then return that alias 
    """
    choice = filter_stopword(choice)
    for word, aliases in ALIASES_VIEW.items():
        if any(x for x in choice if x in aliases):
            return word
            
def shop_parser(choice : str, shop : "Shop") -> "Tuple[str, Item]":
    """A more robust parser for handling a player's responses within the context of a shop. This parser
    works in the following way:
    
    #. Check if the player desires to exit the shop by checking if the input is a valid direction or parsable direction
    
    #. Clean up user input and remove Stopwords.
    
    #. For each possible alias in ALIASES_SHOP check if the user input contains, if it does then continue
    
    #. Compare every item and pick the one where the most words of the user input match the name
    
    """
    if leave := direction_parser(choice, shop):
        return "exit", None
    
    choice = filter_stopword(choice)
    for word, aliases in ALIASES_SHOP.items():
        if any(x for x in choice if x in aliases):
            best_item = (None, 0)
            for item in shop.items:
                new_item = len([x for x in choice if x in item.item.name.lower()])
                if new_item > best_item[1]:
                    best_item = (item, new_item)
            
            if best_item[0]:     
                return word, best_item[0]
                
    return None, None
    
def target_parser(choice : str, targets : "List[Enemy]", player : "Player" = None) -> "Enemy":
    """This checks if the user input contains enough keywords that can be considered to target an enemy. This
    parser assumes that the input has already been cleaned up and that another parser has already validated the
    primary action. The parser works as follows:
    
    #. If the there is only one enemy then return that enemy
    
    #. Compare every enemy and pick the one where the most words of the user input match the name
    
    #. If there are multiple possible targets check for for position context from POSITIONS
    
    Possible Improvements
    ======================
    * Check if the user input includes index-based context for the target they wish to attack. e.g 3rd golbin
    * Check if the user input includes contextual clues such as "lowest health", "weakest", ect...
    * Allow the player as a valid attack target (Done, to be tested)
    
    """
    if any(x for x in choice if x in PLAYER) and player is not None:
        return player
    
    if len(targets) == 1:
        return targets[0]
    
    best_enemy = 0
    enemies = []
    for enemy in targets:
        new_enemy = len([x for x in choice if x in enemy.name.lower()])
        if new_enemy > best_enemy:
            best_enemy = new_enemy
            enemies = []
        elif new_enemy == best_enemy:
            enemies.append(enemy)
            
    if len(enemies) == 1:
        return enemies[0]
    elif len(enemies) == 3:
        for index, position in enumerate(POSITIONS):
            if any(x for x in choice if x in position):
                return enemies[index]
    
def attack_parser(choice : str, battle : "Battle") -> "Enemy":
    """A robust system to handle the user attacking an enemy during battle. This performs a simple
    check to see if the user desire to perform a simple attack and who they desire to attack. The
    parser proceeds in a very short process:
    
    #. Check if the player desires to attack by checking it against the list of ACCEPTABLE_ATTACKS words and the name of the player's weapon
    
    #. If a match a found then the parser seeks to find a target by passing the user input and context to :method:target_parser
    
    """
    choice = filter_stopword(choice)
    
    if any(x for x in choice if x in [*ACCEPTABLE_ATTACKS, battle.player.weapon.name]):
        return target_parser(choice, battle.alive, battle.player)
        
def yes_or_no_parser(choice):
    """A simple parser to check for a yes or no answer, based on basic boolean checks, this is used
    within the yes_or_no utils function. The parser works as follow:
        
    #. Clean up user input and remove Stopwords.
    
    #. Check if any of the word match any of the YES or NO words, if they do return True or False respectively, if not return None
    """
    choice = clean(choice).split()
    
    if any(x for x in choice if x in YES):
        return True
    elif any(x for x in choice if x in NO):
        return False
        
    return None
    
def equip_item_parser(choice : str, player : "Player") -> "Equipment":
    """A more robust filter for deciphering what item the player desires to equip, wether
    it be Armor or Weapon. It works as follows:
    
    #. Clean up user input and remove Stopwords
    
    #. Check if any of the words in the user input match an acceptable word for equipping
    
    #. Compare every item and pick the one where the most words of the user input match the name
    """
    choice = filter_stopword(choice)
    
    if any(x for x in choice if x in ACCEPTABLE_EQUIP):
        best_equip = (None, 0)
        for item in player.inventory.equipement:
            new_equip = len([x for x in choice if x in item.name.lower()])
            if new_equip > best_equip[1]:
                best_equip =  (item, new_equip)
                
        return best_equip[0]            

def use_item_parser(choice : str, ctx : "Union[World, Battle]") -> "Tuple[Union[Enemy, Player], Consumable]":
    """A more robust parser for picking an item to use and a target for that item. The parser proceeds in the
    following way:
    
    #. Clean up user input and remove Stopwords.
    
    #. Check if any of the words in the user input match an acceptable word for using an item
    
    #. Compare every item and pick the one where the most words of the user input match the name
    
    #. Hand the context over to :method:target_parser to look for a target
    
    #. If both an item and a target have been parsed then return them
    """
    choice = filter_stopword(choice)
    
    if any(x for x in choice if x in ACCEPTABLE_USE):
        best_item = (None, 0)
        for item in ctx.player.inventory.consumables:
            new_time = len([x for x in choice if x in item.name.lower()])
            if new_item > best_item[1]:
                best_item = (item, new_item)
                
        if hasattr(ctx, "alive"):
            target = target_parser(choice, ctx.alive, ctx.player)
        else:
            target = target_parser(choice, [], ctx.player)
            
        if best_item[0] is not None and target is not None:
            return target, best_item[0]
    
def use_ability_parser(choice, ctx : "Union[World, Battle]") -> "Tuple[Union[Enemy, Player], Ability]":
    """A more robust parser for picking an ability to use and a target for that ability. The parser proceeds in the
    following way:
    
    #. Clean up user input and remove Stopwords.
    
    #. Check if any of the words in the user input match an acceptable word for casting an ability
    
    #. Compare every ability and pick the one where the most words of the user input match the name
    
    #. Hand the context over to :method:target_parser to look for a target
    
    #. If both an ability and a target have been parsed then return them
    """
    choice = filter_stopword(choice)
    
    if any(x for x in choice if x in ACCEPTABLE_CAST):
        best_ability = (None, 0)
        for ability in ctx.player.abilities:
            new_ability = len([x for x in choice if x in ability.name.lower()])
            if new_ability > best_ability[1]:
                best_ability = (ability, new_ability)
                
        if hasattr(ctx, "alive"):
            target = target_parser(choice, ctx.alive, ctx.player)
        else:
            target = target_parser(choice, [], ctx.player)
            
        if best_ability[0] is not None and target is not None:
            return target, best_ability[0]
