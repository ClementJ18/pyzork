from .utils import get_user_input, post_output

class Battle:
    def __init__(self, player, enemies, location):
        self.player = player
        self.alive = [x for x in enemies if x.is_alive()]
        self.location = location

        self.turn = 0
        self.dead = []
        
    def remove_dead(self, enemy):
        dead = self.alive.pop(enemy_index)
        self.player.gain_experience(dead.experience(player))
        self.dead.append()
        

    def battle_loop(self):
        while self.player.is_alive() and self.alive:
            post_output(f"You are attacked by {self.alive}")
            self.player_turn()
            for enemy in self.alive:
                self.enemy_turn(enemy)

            self.end_turn()
        
        self.location.update_alive()
        post_output("You've killed all the enemies!")

    def end_turn(self):
        self.turn += 1

        self.player.end_turn()
        for enemy in self.alive:
            enemy.end_turn()

    def player_turn(self):
        self.player.print_actions(self)
        self.battle_parser()

    def enemy_turn(self, enemy):
        enemy.battle_logic(self)
        
    def battle_parser(self):
        choice = get_user_input().lower()
        split = choice.split()
        if split[0] == "attack":
            enemy_index = int(split[1])
            self.player.do_attack(self.alive[enemy_index])
            if not self.alive[enemy_index].is_alive():
                self.remove_dead(enemy_index)
        
        if split[0] == "cast":
            if len(split) == 3:
                enemy_index = int(split[2])
                self.player.use_ability(self.player.abilities[int(split[1])], self.alive[enemy_index])
                if not self.alive[enemy_index].is_alive():
                    self.remove_dead(enemy_index)
            else:
                self.player.use_ability(self.player.abilities[int(split[1])])
    