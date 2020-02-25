.. currentmodule:: pyzork.base

Quests
=======

.. autoclass:: pyzork.base.QuestManager
    :members: get_finished, start_quest, print_quests, add, pause_quest, unpause_quest, progress_quests, get_finished, process_rewards
    

.. autoclass:: pyzork.base.Quest
    :exclude-members: repeatable
    :members:
    

Example
---------
Creating quests and managing quests use two different classes and can be created with a great amount of granularity.

Quests
#######
Quests are composed of two parts the first part is one or more event based functions which serve the purpose of progressing the quest and a reward which is the entire goal for completing the quest in the first place. For example, a simple quest which only requires you kill a goblin:: 

        from pyzork import QM, Quest, post_output
        
        from my_adventure import Goblin
        
        QM.add(id="KillGob", name="Kill a Goblin")
        class KillGolbin(Quest):
            def on_death(self, entity):
                if isinstance(entity, Goblin):
                    return True
                    
            def reward(self, player):
                post_ouptut("You did it! Well done you killed a goblin!")

Managing Quest
###############
Quests have to be started manually using the QuestManager made available to you by the library, this ensures that you maintain complete control over the quests and their uses. The quest manager is instantiated for you, you only have to import the QuestManager instance which has the name `QM`. When handling quests you'll be using strictly their id. To start a quest you only need to::

    from pyzork import QM
    
    QM.start_quest("KillGob")

You can also pause, stop, unpause quests using the many methods documented for QuestManager. If you create any custom events within quests you will have to propogate them yourself using progress_quests. 

