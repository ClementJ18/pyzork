from .utils import get_user_input, post_output
from .actions import *

class Battle:
    def __init__(self, player, enemies, location):
        self.player = player
        self.alive = [x for x in enemies if x.is_alive()]
        self.location = location

        self.turn = 0
        self.dead = []
        
    def remove_dead(self, enemy_index):
        dead = self.alive.pop(enemy_index)
        self.player.gain_experience(dead.experience(player))
        self.dead.append()
        
    def priorities(self):
        return [self.player_turn, *[lambda: self.enemy_turn(enemy) for enemy in self.alive]]
        
    def battle_loop(self):
        while self.player.is_alive() and self.alive:
            post_output(f"You are attacked by {self.alive}")
            for turn in self.priorities():
                turn()

            self.end_turn()
        
        self.location.update_alive()
        post_output("You've killed all the enemies!")

    def end_turn(self):
        self.turn += 1

        self.player.end_turn()
        self.alive = [x for x in self.alive if x.is_alive()]
        for enemy in self.alive:
            enemy.end_turn()

    def player_turn(self):
        post_output(f"- Attack an enemy with your {self.player.weapon}")
        post_output("- Cast an ability")
        post_output("- View your stats")
        post_output("- View your inventory")
        
        while self.battle_parser():
            pass

    def enemy_turn(self, enemy):
        enemy.battle_logic(self)
        
    def battle_parser(self):
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
        elif reply := view_parser(choice, self.player):
            getattr(self.player, f"print_{reply}")()
            return True
            
        return False
            
    