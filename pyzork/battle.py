from .utils import get_user_input, post_output

class Battle:
    def __init__(self, player, enemies, area):
        self.player = player
        self.alive = enemies
        self.area = area

        self.turn = 0
        self.dead = []

    def battle(self):
        while self.player.is_alive() and self.alive:
            self.player_turn()
            for enemy in self.alive:
                self.enemy_turn(enemy)

            self.end_turn()
            
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
                self.dead.append(self.alive.pop(enemy_index))
        
        if split[0] == "cast":
            if len(split) == 3:
                enemy_index = int(split[2])
                self.player.use_ability(self.player.abilities[int(split[1])], self.alive[enemy_index])
                if not self.alive[enemy_index].is_alive():
                    self.dead.append(self.alive.pop(enemy_index))
            else:
                self.player.use_ability(self.player.abilities[int(split[1])])
    