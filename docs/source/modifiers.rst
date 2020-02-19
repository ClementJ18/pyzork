.. currentmodule:: pyzork.modifiers

Modifiers
==========
A Modifier is the way the library refers to object that cause a change to an entity over a certain period of time. This distinction is important as while abilities can apply modifiers to change stats such as the player's current health they can also simply change it directly from the ability.

.. autoclass:: pyzork.modifiers.Modifier
    :members: is_expired, buff, effect, add_buff, add_effect


Examples
---------
There are few different ways to create a modifier. The most common is to use the builtin class method `add_effect` or `add_buff`. This allows you to add either a buff or an effect, these can be chained to add both a buff and effect to the Modifier. Using the decorator will transform the function into a Modifier subclass.

Basic Buff
###########
This shows you how to create a basic debuff using the decorator that will reduce the entity's attack by 3 for 5 turns.::

    from pyzork import Modifier, StatEnum
    
    @Modifier.add_buff(stat_type=StatEnum.attack, duration=5)
    def Debuff(modifier, entity):
        return -3

Calling `Debuff` will now return an instance of the class Debuff which is a sublcass of the Modifier class. Since you have access to the entity instance you can of course do some more complex changes, for example you could make a debuff which reduces the entity's attack by 25%::

    from pyzork import Modifier, StatEnum
    
    @Modifier.add_buff(stat_type=StatEnum.attack, duration=5)
    def Debuff(modifier, entity):
        return player.base_damage * 0.25
        

When using modifiers in such a manner remember you only have access to the base stats, if you try and modify the calculated stats you will create an endless loop which will crash your adventure when you reach the recursion limit.

Basic Effect
#############
This shows you how to create a basic effect using the decorator that will deal 2 damage per turn to the entity for 4 turns.::

    from pyzork import Modifier
    
    @Modifier.add_effect(duration=4)
    def Poison(modifier, entity):
        entity.take_pure_damage(2)

Calling `Debuff` will now return an instance of the class Debuff which is a sublcass of the Modifier class.

Combining
##########
You can combine both the decorators to add a buff or effect to an existing modifier. Here we'll show how to do this, combining the effect and buff from the previous examples. The finished product will deal 2 damage and reduce the attack of the entity by 3 for 5 turns:: 

    from pyzork import Modifier, StatEnum
    
    Modifier.add_effect(duration=5)
    def Poison(modifier, entity):
        entity.take_pure_damage(2)
        
    @Poison.add_buff(stat_type=StatEnum.attack)
    def poison_buff(modifier, entity):
        return -3

Since Poison is already a subclass of the Modifier, the function poison_buff will remain untouched.

Subclassing
############
Of course, if you don't feel like messing around with decorators you can simply subclass modifiers and overwrite either `buff`, `effect` or both. Retaking our example from Combining:: 

    from pyzork import Modifier, StatEnum
    
    class Poison(Modifier):
        def __init__(self):
            super().__init__(duration=5, stat_type=StatEnum.attack)
        
        def effect(self, entity):
            entity.take_pure_damage(2)
            
        def buff(self, entity):
            return -3

There, it has the exact same result. You will now have access to a class Poison to allow you to create an instance of the modifier.

