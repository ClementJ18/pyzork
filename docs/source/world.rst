.. currentmodule:: pyzork.world

World
======

The world is where your adventure lives, this is the root of you entire story and where all the events happen. To create the basis of a World you use and subclass the two classes described bellow:

.. autoclass:: pyzork.world.Location
    :members: one_way_connect, two_way_connect, enter, exit, print_interaction, can_move_to, directional_move, from_dict, print_exits, print_npcs, 

.. autoclass:: pyzork.world.Shop
    :members:
    :inherited-members:


.. autoclass:: pyzork.world.World
    :members:

Examples
=========
