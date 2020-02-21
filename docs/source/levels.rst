.. currentmodule:: pyzork.levels

Levels
=======
Levels are one of the few objects in pyzork that do not need to be subclassed or used as decorators in order to fully function. The `ExperienceLevels` class handles both the current experience of the entity it is attached to and its level.

Whenever an entity defeats another entity (by default) they gain some amount of experience, when they reach a certain treshold they level up. When an entity levels up, the treshold is substracted from their total experience, their level increments by one and they gain a reward. In the case of this library a reward is attributed through a function being called. By default this function simply prints "You leveled up! You are now level [entity.level]" and does nothing else but it provides you access to the entity that leveled up, which means you can do anything to that entity. In addition, leveling up also sends out a `on_level` event to the Quest Manager

.. autoclass:: pyzork.levels.ExperienceLevels
    :members:

Examples
---------
The ExperienceLevels class gives you a lot of flexibility on if you want to hardcode every level and every reward or if you just want to generate those with some base parameters. For example, here's a basic example that just makes use
of the default reward (which is just a message saying you leveled up):: 

    from pyzork.levels import ExperienceLevels
    
    basic = ExperienceLevels(requirement=100, modifier=1.2, max_level=10)

This basic can then be passed to the `Entity` class. The requirement from level 0 to 1 is 100 and then any
requirement after that is multiplied by 1.2 with the final requirement being level 9 to 10. You can also hardcode everything, if you want to have complete control over the way the experience is distributed. Still using the default reward:: 

    from pyzork.levels import ExperienceLevels
    
    basic = ExperienceLevels(requirements=[2, 33, 56, 23, 78])

In this case, the max level is 5 because there are 5 requirements. Finally, you can also mix and match automatically generated and hardcoded using the abstract keyword argument. For example, here we take our first example, but change the level 5 requirement so it's 500::

    from pyzork.levels import ExperienceLevels
    
    basic = ExperienceLevels(
        requirement=100, 
        modifier=1.2, 
        max_level=10, 
        r5=500
    )

You can apply a similar process for rewards, a reward can be the same for every level. In this case our reward is that the entity health, damage and max health is increased by 10% every level::

    from pyzork.levels import ExperienceLevels
    
    def basic_reward(levels):
        levels.entity.base_damage *= 0.1
        levels.entity.base_defense *= 0.1
        levels.entity.health += levels.entity.base_max_health * 0.1
        levels.entity.base_max_health *= 0.1
        
    basic = ExperienceLevels(
        requirement=100, 
        modifier=1.2, 
        max_level=10, 
        reward=basic_reward
    )

Similarly, we can hardcode every reward. Note that while you don't have to provide a reward system in order to create a valid ExperienceLevels instance you must provide requirements in one form or another::

    from pyzork.levels import ExperienceLevels
    
    def basic_reward_1(levels):
        levels.entity.base_damage *= 0.1
        levels.entity.base_defense *= 0.1
        levels.entity.health += levels.entity.base_max_health * 0.1
        levels.entity.base_max_health *= 0.1
        
    def basic_reward_2(levels):
        levels.entity.base_damage *= 0.2
        levels.entity.base_defense *= 0.2
        levels.entity.health += levels.entity.base_max_health * 0.2
        levels.entity.base_max_health *= 0.2
        
    basic = ExperienceLevels(
        requirement=100, 
        modifier=1.2, 
        max_level=2, 
        rewards=[basic_reward_1, basic_reward_2]
    )

Finally, as with requirements, you have complete control and can mix and match reward generation. For example, standard 10% increase in stats for all levels apart from level 5 where we get a 20% increase in stats::

    from pyzork.levels import ExperienceLevels
    
    def basic_reward(levels):
        levels.entity.base_damage *= 0.1
        levels.entity.base_defense *= 0.1
        levels.entity.health += levels.entity.base_max_health * 0.1
        levels.entity.base_max_health *= 0.1
        
    def l5_reward(levels):
        levels.entity.base_damage *= 0.2
        levels.entity.base_defense *= 0.2
        levels.entity.health += levels.entity.base_max_health * 0.2
        levels.entity.base_max_health *= 0.2
        
    basic = ExperienceLevels(
        requirement=100, 
        modifier=1.2, 
        max_level=2, 
        reward=basic_reward, 
        l5=l5_reward
    )

