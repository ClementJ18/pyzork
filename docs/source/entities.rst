.. currentmodule:: pyzork.entities

Entities
=========
Entities are anything that exist within your world that is either the player or that the player can interact with in some way. Things like enemies, other people, animals, etc... They can also be inanimate object, for example a table that the player needs to grab a key from. 

.. autoclass:: pyzork.entities.Player
    :members: is_alive, can_cast, print_abilities, print_inventory, print_stats, do_attack, take_damage, take_pure_damage, restore_health, use_energy, gain_energy, use_ability, end_turn, add_ability, remove_ability, add_modifier, remove_modifier, gain_experience, lose_experience, use_item_on_me, use_item_on, remove_money, add_money, set_world

.. autoclass:: pyzork.entities.NPC
    :members: is_alive, can_cast, print_abilities, print_inventory, print_stats, do_attack, take_damage, take_pure_damage, restore_health, use_energy, gain_energy, use_ability, end_turn, add_ability, remove_ability, add_modifier, remove_modifier, gain_experience, lose_experience, use_item_on_me, use_item_on, remove_money, add_money, experience, battle_logic, print_interaction, interaction

Examples
---------
There are many ways of making entities, for most cases you'll only need the from_dict method but you can always subclass the Player or NPC classes for further edits

Basic
######
::
    import pyzork
    
    Goblin = pyzork.Goblin.from_dict(name="Goblin", max_health=20, attack=3, description="A lowly goblin")


