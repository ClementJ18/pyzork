import unittest
import pyzork

class Sword(pyzork.Weapon):
    pass
            
class HealthPotion(pyzork.Consumable):
    """Health Potion"""
    def __init__(self):
        super().__init__(charges=3)
    
class HealingOnguent(pyzork.Consumable):
    """Healing Onguent"""
    def __init__(self):
        super().__init__(charges=3)
    
class SwordAndShield(pyzork.Weapon):
    """Sword and Shield"""
    pass
    
class Cuirass(pyzork.Armor):
    pass
    
class MagicPowder(pyzork.Consumable):
    """Magic Powder"""
    def __init__(self):
        super().__init__(charges=3)
    
class Spear(pyzork.Consumable):
    def __init__(self):
        super().__init__(charges=3)
    
goblin = pyzork.NPC(name="Fat Goblin", max_health=1)
wizard = pyzork.NPC(name="Enemy wizard", max_health=1)
goblin2 = pyzork.NPC(name="Goblin", max_health=1)

class TestDirectionParser(unittest.TestCase):
    def test(self):
        shop = pyzork.Location(name="Shop")
        market = pyzork.Location(name="Market")
        tavern = pyzork.Location(name="Tavern")
        
        market.two_way_connect(pyzork.Direction.east, shop)
        market.two_way_connect(pyzork.Direction.south, tavern)
        
        strings = [
            ("go south", pyzork.Direction.south),
            ("go to the tavern", pyzork.Direction.south),
            ("stay here", None),
            ("enter the shop", pyzork.Direction.east),
            ("ENTER THE TAVERN", pyzork.Direction.south),
            ("go west", pyzork.Direction.west),
            ("go north", pyzork.Direction.north)
        ]
        
        for string, direction in strings:
            reply = pyzork.actions.direction_parser(string, market)
            self.assertIs(reply, direction, msg=string)

class TestInteractionParser(unittest.TestCase):
    def test(self):
        table = pyzork.NPC.from_dict(name="Old Table")
        old = pyzork.NPC.from_dict(name="Old")
        man = pyzork.NPC.from_dict(name="Old Man")
        princess = pyzork.NPC.from_dict(name="Princess of the Kingdom")
        
        market = pyzork.Location(name="Market", npcs=[table, old, man, princess])
        
        strings = [
            ("talk to the old man", man),
            ("check out the table", table),
            ("interact with old", old),
            ("approach the princess", princess),
        ]
        
        for string, npc in strings:
                reply = pyzork.actions.interact_parser(string, market)
                self.assertIsInstance(reply, npc, msg=string)
        
class TestViewParser(unittest.TestCase):
    def test(self):
        strings = [
            ("view my items", "inventory"),
            ("view my inventory", "inventory"),
            ("check my quests", "inventory"),
            ("see my abilities", "inventory"),
            ("view my consumables", "inventory"),
            ("view my quest items", "inventory"),
            ("view my stats", "stats"),
            ("view my health", "stats"),
            ("look at my health", "stats"),
            ("check my energy", "stats"),
            ("see my attack", "stats"),
            ("view my defense", "stats"),
            ("view my armor", "stats"),
            ("view my weapon", "stats"),
        ]
        
        for string, reply in strings:
            view = pyzork.actions.view_parser(string)
            self.assertEqual(view, reply, msg=string)
        
class TestShopParser(unittest.TestCase):
    def test(self):        
        sword = pyzork.ShopItem(item=Sword, price=25, amount=1)
        potion = pyzork.ShopItem(item=HealthPotion, amount=5, price=10)
        onguent = pyzork.ShopItem(item=HealingOnguent, amount=3, price=5)
        ss = pyzork.ShopItem(item=SwordAndShield, price=30)
        
        shop = pyzork.Shop(name="A Big Shop", resell=0.25, items=[sword, potion, onguent, ss])
        
        strings = [
            ("buy a sword", ("buy", sword)),
            ("purchase a potion", ("buy", potion)),
            ("sell the healing ongeunt", ("sell", onguent)),
            ("buy the sword and shield", ("buy", ss))
        ]
        
        for string, item in strings:
            reply = pyzork.actions.shop_parser(string, shop)
            self.assertIsNot(reply, None, msg=string)
            self.assertEqual(reply[0], item[0], msg=string)
            self.assertIs(reply[1], item[1], msg=string)        
        
class TestAttackParser(unittest.TestCase):
    def test(self):
        player = pyzork.Player()
        battle = pyzork.Battle(player=player, enemies=[goblin, wizard, goblin2])
        
        strings = [
            ("attack the goblin", goblin2),
            ("punch the wizard with my hands", wizard),
            ("strike the fat goblin", goblin),
            ("target the enemy wizard", wizard),
            ("hit myself", player),
            ("strike me", player)
        ]
        
        for string, target in strings:
            reply = pyzork.actions.attack_parser(string, battle)
            self.assertIs(reply, target, msg=string)
        
class TestYesNoParser(unittest.TestCase):
    def test(self):
        strings = [
            ("yes", True),
            ("y", True),
            ("true", True),
            ("yeah", True),
            ("no", False),
            ("nah", False),
            ("false", False),
            ("n", False),
        ]
        
        for string, boolean in strings:
            reply = pyzork.actions.yes_or_no_parser(string)
            self.assertIs(boolean, reply, msg=string)
        
class TestEquipItemParser(unittest.TestCase):
    def test(self):
        inv = pyzork.Inventory(items=[Sword(), Cuirass(), SwordAndShield()])
        p = pyzork.Player(inventory=inv)
        
        strings = [
            ("equip my sword and shield", SwordAndShield),
            ("take the sword", Sword),
            ("put on the cuirass", Cuirass),
        ]
        
        for string, item in strings:
            reply = pyzork.actions.equip_item_parser(string, p)
            self.assertIsInstance(reply, item, msg=string)
        
class TestUseItemParser(unittest.TestCase):
    def test(self):
        inv = pyzork.Inventory(items=[HealingOnguent(), HealthPotion(), MagicPowder(), Spear()])
        player = pyzork.Player(inventory=inv)
        battle = pyzork.Battle(player=player, enemies=[goblin, wizard, goblin2])
        
        strings = [
            ("use the potion on me", (player, HealthPotion)),
            ("use the onguent on me", (player, HealingOnguent)),
            ("throw the spear at the wizard", (wizard, Spear)),
            ("eat the magic powder", (player, MagicPowder)), #NO TARGET
            ("throw the potion at the fat goblin", (goblin, HealthPotion)),       
        ]
        
        for string, enemy in strings:
            reply = pyzork.actions.use_item_parser(string, battle)
            self.assertIsNot(reply, None, msg=string)
            self.assertIs(reply[0], enemy[0], msg=string)
            self.assertIsInstance(reply[1], enemy[1], msg=string)
        
class TestUseAbilityParser(unittest.TestCase):
    def test(self):
        class InsultSpell(pyzork.Ability):
            """Insult"""
            pass
            
        class Fireball(pyzork.Ability):
            pass
            
        class LightningNova(pyzork.Ability):
            """Lightning Nova"""
            pass
            
        class WarRoar(pyzork.Ability):
            """War Roar"""
            pass
            
        player = pyzork.Player(abilities=[InsultSpell(), Fireball(), LightningNova(), WarRoar()])
        battle = pyzork.Battle(player=player, enemies=[goblin, wizard, goblin2])
        
        strings = [
            ("cast insult on the wizard", (wizard, InsultSpell)),
            ("use fireball on the goblin", (goblin2, Fireball)),
            ("cast War Roar on the myself", (player, WarRoar))
        ]
        
        for string, enemy in strings:
            reply = pyzork.actions.use_ability_parser(string, battle)
            self.assertIsNot(reply, None, msg=string)
            self.assertIs(reply[0], enemy[0], msg=string)
            self.assertIsInstance(reply[1], enemy[1], msg=string)
