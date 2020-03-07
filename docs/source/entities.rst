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

