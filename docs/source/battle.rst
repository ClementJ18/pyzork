.. currentmodule:: pyzork.battle

Battles
========
Battles are the most basic form of conflict in an adventure, the player is confronted by enemies of various strengths with the promise that once defeated the story may progress. The simple way to initiate a battle is to call World.initate_battle but you can start your own battle by instancing the Battle and then calling Battle.game_loop.

.. autoclass:: pyzork.battle.Battle
    :members:

Examples
---------
There are lots of customization option in the Battle class.

Changing priorities
#####################
By default, in every battle the player goes first and then every enemy goes after in turn. However, if you want to for example to have the player take their turn after each enemy you could do something like there::

    from pyzork import Player
    
    from my_adventure.enemies import Goblin
    
    def better_priorities(battle):
        priorities = []
        for enemy in battle.alive:
            priorities.append(battle.player_turn)
            priorities.append(battle.enemy_turn_factory(enemy))
            
        return priorities
        
    battle = Battle(enemies=[Goblin(), Goblin(), Goblin()], player=Player(), priorities=better_priorities)
    battle.battle_loop()
