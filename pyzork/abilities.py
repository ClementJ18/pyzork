from .utils import post_output

class Ability:
    """Super class for all abilitis. Most abilities have two uses, they either have a direct effect or add
    a Modifier to either an entity or the user of the ability. But really, you have full control over the effect
    of the ability and you have access to the user casting and its target so go nuts. Similarly to modifiers, entities
    can have an unlimited number of abilities but they can never have the same abiltiy twice.
    
    Parameters
    -----------
    name : Optional[str]
        A name for the ability, if none is provided the library will fallback to the docstring of the class and
        then to the name of the class itself.
    description : Optional[str]
        A description for the ability, if none is provided the library will fall back to the default of the docstring
        of the effect function
    cost : Optional[Union[Callable[[Entity, Entity], int], int]]
        An optional cost for using the ability, this can be a function that returns and int or it can simply be an
        int. By default, the ability will cost 0 energy.
        
    Attributes
    -----------
    name : str
        Name of the ability
    description : Optional[str]
        Optional description of the ability    
    """
    def __init__(self, **kwargs):
        if not hasattr(self, "name"):
            if "name" in kwargs:
                self.name = kwargs.get("name")
            else:
                self.name = self.__doc__ if self.__doc__ else self.__class__.__name__

        if not hasattr(self, "description"):
            self.description = kwargs.get("description", self.effect.__doc__)
        
        if "cost" in kwargs:
            self.cost = kwargs.get("cost", 0)
        
    def __hash__(self):
        return hash(self.__class__.__name__)
        
    def __eq__(self, other : "Ability"):
        if not isinstance(other, type(self)): 
            return NotImplemented
            
        return self.__class__.__name__ == other.__class__.__name__
        
    def __repr__(self):
        return f"<{self.__class__.__name__}>"
        
    def __str__(self):
        return self.name

    def cast(self, user : "Entity", target : "Entity"):
        """Method that verifies if all conditions have been met."""
        if not self.costing(user, target):
            return
        
        post_output(f"{user.name} casts {self.name} on {target.name}")
        self.effect(user, target)
        
    def calculate_cost(self, user : "Entity", target : "Entity"):
        """Private method to calculate the cost
        
        Parameters
        -----------
        user : Entity
            The Entity that used the ability.
        target : Entity
            This is the Entity the ability is aimed at, if the ability is self-cast (user uses ability on
            himself) then it will be the same entity as the `user`.
        """
        if callable(self.cost):
            int_cost = self.cost(user, target)
        else:
            int_cost = self.cost
            
        return int(int_cost)

    def costing(self, user : "Entity", target : "Entity") -> bool:
        """Abstract method that does the logic part of the cost. This allow for flexibility on how you want your 
        cost system to work wether it rage or mana or whatever other custom cost system you may create your 
        class with. This method must return true if the user has enough resource and false if it doesn't.
        
        Parameters
        -----------
        user : Entity
            The Entity that used the ability.
        target : Entity
            This is the Entity the ability is aimed at, if the ability is self-cast (user uses ability on
            himself) then it will be the same entity as the `user`.
        """
        int_cost = self.calculate_cost(user, target)
        if user.can_cast(int_cost):
            user.energy -= int_cost
            return True

        return False

    def effect(self, user : "Entity", target : "Entity"):
        """The method that defines what happens to the target when the ability is cast on it. This can range from
        directly affecting things like health or energy but it can also do more complex things like add a modifier.
        
        Parameters
        -----------
        user : Entity
            The Entity that used the ability. This is made available to allow you to make changes to the user in
            the cases of a successful cast. For example if you want to restore health for damage dealt or 
            restore energy of the ability successfully lands.
        target : Entity
            This is the Entity the ability is aimed at, if the ability is self-cast (user uses ability on
            himself) then it will be the same entity as the `user`.
        """
        raise NotImplementedError
        
    def cost(self, user : "Entity", target : "Entity") -> int:
        """Method to implement if you want to give your ability a dynamic costing.
        
        Parameters
        -----------
        user : Entity
            The Entity that used the ability. This is made available to allow you to create a dynamic cost
            the is based on certain items or stats of the user.
        target : Entity
            This is the Entity the ability is aimed at, if the ability is self-cast (user uses ability on
            himself) then it will be the same entity as the `user`.
            
        Returns
        --------
        int
            The final, calculated cost of casting this ability
        """
        return 0
            
    @classmethod
    def add(cls, **kwargs):
        """Decorator function to allow you to decorate a function in order to transform it into an Ability
        subclass. Takes the same arguments as the class itself."""
        def decorator(func):
            new_class = type(func.__name__, (cls,), {
                "cost": kwargs.get("cost", 0), 
                "effect": func,
                "name": kwargs.get("name", func.__name__),
                "description": kwargs.get("description", func.__doc__)
            })
            
            return new_class
            
        return decorator
