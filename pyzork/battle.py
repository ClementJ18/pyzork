from .utils import get_user_input, post_output
from .actions import *

class Battle:
    """
    The battle class does need to be subclassed unless you need a very fine grained control over how battles
    go. For most users, simply using this and the various parameters it makes available to you should be enough.
    
    Once you instantiated a Battle all you need to do is to call `game_loop` method to start the battle, the method
    will return if the player wins, if not it will raise EndGame.
    
    Parameters
    ------------
    player : Player
        The player fighting
    enemies : List[Enemy]
        The list of enemies for the player to fight
    location : Optional[Location]
        Where the player is fighting, this is optional in the case that the list of enemies is form
        this location and it needs to be updated once they get killed off.
    priorities : Optional[Callable[[Battle], Callable[]]:
        Optional callable which determines in what order all the entities in the battle
        take turn.
    """
    def __init__(self, player, enemies, location = None, **kwargs):
        self.player = player
        self.alive = [x for x in enemies if x.is_alive()]
        self.location = location
        self.priorities = kwargs.get("priorities", self.priorities)

        self.turn = 0
        self.deads = [x for x in enemies if not x.is_alive()]
        
    def remove_dead(self, index : int):
        """Remove a dead enemy from the list of living enemies and grant experience to the player
        
        Parameters
        -----------
        index : int
            Index of the enemy to remove
        """
        dead = self.alive.pop(index)
        self.player.gain_experience(dead.experience(player))
        self.deads.append(dead)
        
    def priorities(self):
        """Overwritable method to determine in what order all the entities involved in this
        battle go. This function must return a list of callables that don't take any arguments.
        Once that list is exauhsted this will be considered a full turn. There are no limits on how
        many times an entity can go in the same turn. By default the player goes first and then every
        enemy goes after.
        
        Returns
        ---------
        List[Callable[]]
            The list of turn functions to be called.
        """
        return [self.player_turn, *[self.enemy_turn_factory(enemy) for enemy in self.alive]]
        
    def enemy_turn_factory(self, enemy : "Enemy"):
        """Factory method for use in `priorities`, returns a callable that is valid callable for `enemy` to
        make an action.
        
        Parameters
        -----------
        enemy : Enemy
            The enemy to make the callable for
            
        Returns
        --------
        Callable[]
        """
        return lambda: self.enemy_turn(enemy)    
    
    def battle_loop(self):
        """Heart of the battle system. Call this to start the battle"""
        while self.player.is_alive() and self.alive:
            post_output(f"You are attacked by {self.alive}")
            for turn in self.priorities():
                turn()

            self.end_turn()
        
        if not self.location is None:
            self.location.update_alive()
        
        post_output("You've killed all the enemies!")

    def end_turn(self):
        """Increments the turns, remove dead stuff and decrement duration of modifiers"""
        self.turn += 1

        self.player.end_turn()
        
        for index, enemy in list(enumerate(self.alive)):
            if not enemy.is_alive():
                self.remove_dead(index)
            
        for enemy in self.alive:
            enemy.end_turn()

    def player_turn(self):
        """Print possible options and let the user pick one through `battle_parser`"""
        post_output(f"- Attack an enemy with your {self.player.weapon}")
        post_output("- Cast an ability")
        post_output("- View your stats")
        post_output("- View your inventory")
        
        while self.battle_parser():
            pass

    def enemy_turn(self, enemy : "Enemy"):
        """Call the enemy's battle_logic function.
        
        Parameters
        -----------
        enemy : Enemy
            The enemy who's taking their turn
        """
        enemy.battle_logic(self)
        
    def battle_parser(self) -> bool:
        """Take input of the user and parse it against a set of possible actions
        
        Returns
        --------
        bool
            Whether this actions counts as taking a turn. If the action counts as
            taking a turn then performing it will end the player's turn and move onto
            the rest of the priorities.
        """
        choice = get_user_input().lower()
        if target := attack_parser(choice, self):
            self.player.do_attack(target)
            return False
        elif reply := use_ability_parser(choice, self):
            self.player.use_ability(reply[1], reply[0])
            return False
        elif reply := use_item_parser(choice, self):
            self.player.use_item_on(reply[1], reply[0])
            return False
        elif reply := view_parser(choice):
            getattr(self.player, f"print_{reply}")()
            return True
            
        return False      
    