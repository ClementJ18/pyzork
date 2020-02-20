.. currentmodule:: pyzork.abilities

Abilities
==========
Abilities are special powers or skills that can be used in combat (and sometimes out of combat) to gain an edge, either dealing damage, gaining increased stats for a while or impeding the enemy's ability to fight. Abilities usually have a cost of energy, by default that cost is taken from the entity's `energy` attribute, however subclasses of `Entity` can easily implement their own additional energy types. 

.. autoclass:: pyzork.abilities.Ability
    :members: cost, effect
    

Examples
---------
There are many ways to create abilities, the simplest being to use the decorator but you can also subclass the Ability parent class as a whole or anything in between. Below are three examples going over some of the possibilities. 

Decorator
##########
Decorating a function with @Ability.add() will transform it into a subclass of Ability of the same name as the function. Here we will be creating a simple ability that costs 4 energy and applies the WarRoar modifier (an hypothetical modifiers) to the entity that used the ability.::
    
    from pyzork import Ability
    
    from my_adventure import WarRoarModifier
    
    @Ability.add(cost=4, name="War Scream", description="A loud scream")
    def WarRoar(ability, user, target):
        user.add_modifier(WarRoarModifier())

The `cost` parameter can also take a callable, if you desire for the costing of the ability to be dynamic. In this case the cost of the ability is 10% of the user's energy.::

    from pyzork import Ability
    
    from my_adventure import WarRoarModifier
    
    def callable_cost(ability, user, target):
        return int(user.energy * 0.1)
        
    @Ability.add(cost=callable_cost)
    def WarRoar(ability, user, target):
        user.add_modifier(WarRoarModifier())

Subclassing
############
You can also subclass Ability and overwrite the methods you want. Here we create a simple ability that costs 4 energy and applies the WarRoarModifier to the user::

    from pyzork import Ability
    
    from my_adventure import WarRoarModifier
    
    class WarRoar(Ability):
        def cost(self, user, target):
            return 4
            
        def effect(self, user, target):
            user.add_modifier(WarRoarModifier())

