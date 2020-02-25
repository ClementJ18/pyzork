from .utils import post_output
from .errors import *

class QuestManager:
    def __init__(self, **kwargs):
        """The QuestManager is a module wide instance which is used to manage quests in your adventure. To use
        it you can import it like so: `from pyzork import QM`.
        
        Attributes
        -----------
        quests : Dict[str : Quest]
            A dictionnary of quest ids and Quest classes (non-instantiated), this represents all the quests
            that can be started.
        active_quests : Dict[str : Quest]
            A dictionnary of quest ids and Quest instances, representing quests that are currently active, quests
            in this dict can be either paused or unpaused.
        finished_quests : Dict[str : int]
            A dictionnary of quest ids and int, representing each quests and how many times they have been 
            completed
        pending_rewards : List[Quest]
            A list of completed quests from which the rewards have not yet been claimed, this list is
            processed by `progress_rewards`.
        """
        self.quests = kwargs.pop("quests", {})
        self.active_quests = {}
        self.finished_quests = {x : 0 for x in self.quests}
        self.pending_rewards = []
        
    def add(self, **kwargs):
        """Decorator method for adding quests to the QuestManager instance. This adds the quest to the list
        of possible quests but does not start it. This leaves the quest sublcass itself untouched but adds 
        it to the list.
        
        Parameters
        ------------
        id : str
            The unique identifier for the quest, used whenever you want to manipulate a specific quest
        name : Optional[str]
            The user name of the quest, the library will fall back to the class doc and then the class
            name if none are provided
        description : Optional[str]
            The user friendly description of the quest. If none are provided the library will fallback
            to the doc of the `reward` function of that quest
        repeatable : Optional[int]
            How many times the quest can be done, defaults to 1    
        """
        def wrapper(quest):
            name = kwargs.pop("name", quest.get_class_name())
            repeat_int = kwargs.pop("repeatable", 1)
            
            def repeatable(self):
                return repeat_int
                
            quest.repeatable = repeatable
            quest.name = name
            quest.id = kwargs.pop("id")
            quest.description = kwargs.pop("description", quest.reward.__doc__)
            self.add_quest(quest)
            
            return quest 
                   
        return wrapper
        
    def add_quest(self, quest):
        if quest.id in self.quests:
            raise KeyError("Duplicate quest id")
            
        self.quests[quest.id] = quest
        self.finished_quests[quest.id] = 0
        
    def remove_quest(self, quest_id):
        del self.quests[quest_id]
        del self.finished_quests[quest_id]
        
    def print_quests(self):
        """Print all the currently active quests."""
        for quest in self.active_quests:
            post_output(f"{self.quest.name}\n{self.quest.description}\n")
            
    def start_quest(self, quest_id):
        """Start a specific quest, this will create an instance of the class and allow the player's
        action to contribute to its progression.
        
        Parameters
        -----------
        quest_id : str
            The unique identifier for the quest you wish to start
        """
        if quest_id in self.active_quests:
            raise QuestStarted("This quest has already started")
            
        quest = self.quests[quest_id]()
        total = quest.repeatable()
        if self.finished_quests[quest_id] >= total:
            raise QuestNonRepeatable(f"This quest cannot be done more than {total} time(s)") 
            
        self.active_quests[quest_id] = quest
        
    def stop_quest(self, quest_id):
        """Stop a quest, discarding current progress and stopping player's actions from contributing to its
        progression. A new instance of that quest can now be started.
        
        Parameters
        -----------
        quest_id : str
            The unique identifier for the quest you wish to stop
        """
        del self.active_quests[quest_id]
        
    def pause_quest(self, quest_id):
        """Pause a quest, the quest's current progress remains stored and a new instance of the quest cannot
        be started but the player's actions will no longer contribute to the quest's progression.
        
        Parameters
        -----------
        quest_id : str
            The unique identifier for the quest you wish to pause
        """
        self.active_quests[quest_id].pause(True)
    
    def unpause_quest(self, quest_id):
        """Unpause a paused quest, this will allow a player's actions to contribute to the quest's
        progression. Unpausing 
        
        Parameters
        -----------
        quest_id : str
            The unique identifier for the quest you wih to unpause
        """
        self.active_quests[quest_id].pause(False)
        
    def progress_quests(self, event, *args, **kwargs):
        """This is the heart of the quest system, this is the method that needs to be called in order to
        propogate events to all the quests that can handle it. If are only relying on built-in events in
        their default states you do not need to call this funtion, you'll only needto call this functin
        if you create your own events.
        
        Parameters
        -----------
        event : str
            The event that has happened, this is merely the name of the function but should
            follow the on_XXX name convention such as `on_death`, `on_pickup`, etc...
        *args : List
            List of args that will be passed to the quests that have this event
        **kwargs : Dict
            Dictionnary of kwargs that will be passed to the quests that have this event
        """
        rewards = []
        for quest_id, quest in list(self.active_quests.items()):
            if quest.paused:
                continue
            
            try:
                done = getattr(quest, event)(*args, **kwargs)
            except AttributeError:
                continue
                
            if done:
                self.stop_quest(quest_id)
                self.finished_quests[quest_id] += 1
                self.pending_rewards.append(quest)
                post_output(f"finished {quest.name} ({quest.id})")
                
    def get_finished(self, quest_id : str) -> int:
        """Returns the number of time a quest was finished.
        
        Parameters
        -----------
        quest_id : str
            The unique identifier for the quest
        
        Returns
        --------
        int
            The number of time the quest was completed.
        """
        return self.finished_quests[quest_id] 
        
    def proccess_rewards(self, player : "Player", world : "World"):
        """This processes all the current rewards that have not yet been claimed. This is called by default in
        the world loop, you can call this manually to force requests to be processed if the player is out
        of the world loop for a particularly long time.
        
        Parameters
        -----------
        player : Player
            The player to reward, this will be passed straight on the the quest's `reward` function.
        world : World
            The world where the quest happened, this will be passed straight to the quest's reward function.
        """
        while self.pending_rewards:
            quest = self.pending_rewards.pop(0)
            quest.reward(player, world)
                            
QM = QuestManager()
        
class Quest:
    """
    Quests are missions within the world you create for the player, they are there to guide the player, give
    a directive. They can also be used to allow the player to gain additional power through side missions, which
    don't necessarily affect the main story. 
    
    Quests come by default with a certain numbers of event that are triggered by the library when certain things
    happen. However, these events are by no means hardcoded, you can freely create your own events which can be
    propageted using pyzork.qm.progress_quests and will then be applied to any quests which has that event.
    
    Attributes
    -----------
    name : str
        The name of the quest, if none is given during init then the library falls back first to the docstring
        of the class and then to the class name.
    description : str
        The description of the quest, if none is given the library falls back to the docstring of the reward
        method
    id : str
        The unique identifier for the quests which are used for things like `qm.start_quest` and `qm.stop_quest`
        
    """
    def __init__(self, **kwargs):
        if not getattr(self, "name", False):
            if "name" in kwargs:
                self.name = kwargs.pop("name")
            else:
                self.name = self.__doc__ if self.__doc__ else self.__class__.__name__
        
        if not getattr(self, "description", False):
            self.description = kwargs.pop("description", self.reward.__doc__)
            
        if not getattr(self, "id", False):
            self.id = kwargs.pop("id")
            
        self.paused = False
        self.setup(**kwargs)
        
    def __repr__(self):
        return f"<{self.name}>"
        
    def setup(self, **kwargs):
        """Function called when the quest is started, kinda like __init__. You have access to the kwargs
        passed to __init__.
        
        Parameters
        -----------
        kwargs : dict
            The kwargs passed to the __init__ function
        """
        pass
        
    def on_death(self, entity : "Entity"):
        """This even is triggered everytime an entity's health reaches 0. The event makes the instance of that 
        entity available to you.
        
        Parameters
        -----------
        entity : Entity
            The entity that has died
            
        Returns
        --------
        bool
            Whether or not the quest is done, if True the quest is considered completed, if it is False
            or None the quest is considered still in progress.
        """
        pass
        
    def on_pickup(self, item : "Item"):
        """Happens everytime an item is picked up.
        
        Parameters
        -----------
        
        Returns
        --------
        bool
            Whether or not the quest is done, if True the quest is considered completed, if it is False
            or None the quest is considered still in progress.
        """
        #TODO: Figure if I wanna make the entity picking up the item available too
        pass
        
    def on_discover(self, location : "Location"):
        """Happens everytime a location is discovered for the first time. This makes the location itself
        available to you.
        
        Parameters
        -----------
        location : Location
            The location that was discovered
            
        Returns
        --------
        bool
            Whether or not the quest is done, if True the quest is considered completed, if it is False
            or None the quest is considered still in progress.
        """
        pass
        
        
    def on_interact(self, entity : "Entity", world : "World"):
        """Happens everytime an Entity is talked to.
        
        Parameters
        -----------
        entity : Entity
            The entity that is being interacted with.
        world : World
            The world instance where the interaction is happening.
        
        Returns
        --------
        bool
            Whether or not the quest is done, if True the quest is considered completed, if it is False
            or None the quest is considered still in progress.
        """
        pass
        
    def on_level(self, levels : "ExperienceLevels"):
        """Happens everytime an entity levels up
        
        Parameters
        ----------
        levels : ExperienceLevels
            The instance which just leveled up.
        
        Returns
        --------
        bool
            Whether or not the quest is done, if True the quest is considered completed, if it is False
            or None the quest is considered still in progress.
        """
        pass
        
    def reward(self, player : "Player"):
        """Function that grants the player a certain reward, this make the player instance available to
        you. Quest rewards are only processed in the world loop by default, if you want or need to forcibly
        check if any new rewards have been made available you can use pyzork.qm.process_rewards
        
        Parameters
        -----------
        player : Player
            The player instance of the adventure
        """
        pass
        
    def repeatable(self) -> int:
        """Function that defines how many times you can do this quest, 1 by default. Must return an int"""
        return 1
        
    def pause(self, value):
        self.paused = value
        
    @classmethod
    def get_class_name(cls):
        return cls.__name__
    
def game_loop(world):
    try:
        world.world_loop()
    except EndGame as e:
        world.end_game(e)
    except Exception as e:
        world.error_handler(e)
    