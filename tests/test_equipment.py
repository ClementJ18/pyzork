import unittest
import pyzork

class TestConsumable(unittest.TestCase):
    def setUp(self):
        self.player = pyzork.Player(max_health=100, health=0)
        self.charges = 0
        self.heal = 0
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def check_item(self):
        self.assertEqual(self.item.charges, self.charges)
        
        for x in range(self.item.charges):
            health = self.player.health + self.heal
            charges = self.charges - (x + 1)
            self.item.use(self.player)
            self.assertEqual(self.player.health, health)
            self.assertEqual(self.item.charges, charges)
        
        self.item.use(self.player)
        self.assertEqual(self.player.health, health)
        self.assertEqual(self.item.charges, 0)
        
        self.item.effect(self.player)
        
        self.assertEqual(self.player.health, health + self.heal)
        
    def test_subclass(self):
        self.charges = 3
        self.heal = 5
        
        class HealthPotion(pyzork.Consumable):
            """Health potion"""
            def __init__(item):
                super().__init__(charges=self.charges)
                
            def effect(item, target):
                """Restores five health of the target"""
                target.restore_health(self.heal)
                
        self.item = HealthPotion()
                
        self.assertEqual(self.item.name, "Health potion")
        self.assertEqual(self.item.description, "Restores five health of the target")    
        
        self.check_item()
        
    def test_decorator(self):
        self.charges = 1
        self.heal = 3
        
        @pyzork.Consumable.add(charges=self.charges, name="HEALTH POTION", description="Regnerates 5 health")
        def HealthPotion(item, target):
            target.restore_health(self.heal)
        
        self.item = HealthPotion()
                
        self.assertEqual(self.item.name, "HEALTH POTION")
        self.assertEqual(self.item.description, "Regnerates 5 health")    
        
        self.check_item()

class TestQuestItem(unittest.TestCase):
    def test(self):
        ImportantKey = pyzork.QuestItem.from_dict(name="An Important Key", description="A key that opens something")
        
        self.item = ImportantKey()
        
        self.assertEqual(self.item.name, "An Important Key")
        self.assertEqual(self.item.description, "A key that opens something") 
        
class TestEquipment(unittest.TestCase):
    def setUp(self):
        self.damage = 0
        self.buff = 0
        self.stat = pyzork.StatEnum.attack
        self.p = pyzork.Player(max_health=10)
        
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def check_item(self):
        self.p.inventory.add_item(self.item)
        self.p.inventory.equip_item(self.item)
        
        self.assertEqual(self.p.attack, self.buff)
        
        health = self.p.health - (self.damage + self.buff)
        self.p.do_attack(self.p)
        
        self.assertEqual(self.p.health, health)
    
    def test_effect(self):
        self.damage = 4
        
        @pyzork.Weapon.add_effect(name="Rusty Sword", description="A rusty sword that deals extra damage")
        def PoisonedSword(weapon, target):
            target.take_pure_damage(self.damage)
            
        self.item = PoisonedSword()
        
        self.assertEqual(self.item.name, "Rusty Sword")
        self.assertEqual(self.item.description, "A rusty sword that deals extra damage")
        
        self.check_item()
        
    def test_buff(self):
        self.buff = 5
        
        @pyzork.Weapon.add_buff(name="Big Sword")
        def BigSword(weapon, user):
            """A big sword that increases your damage by 5"""
            return [(self.stat, self.buff)]
            
        self.item = BigSword()
            
        self.assertEqual(self.item.name, "Big Sword")
        self.assertEqual(self.item.description, "A big sword that increases your damage by 5")
        
        self.check_item()
        
    def test_buff_and_effect(self):
        @pyzork.Armor.add_buff()
        def Armor(armor, user):
            """Some thick armor."""
            return [(self.stat, self.buff)]
            
        @Armor.add_effect()
        def effect(armor, target):
            """Poisoned thick armor"""
            target.take_pure_damage(self.damage)
            
        self.item = Armor()
        
        self.assertEqual(self.item.name, "Armor")
        self.assertEqual(self.item.description, "Some thick armor. Poisoned thick armor")
        
        self.check_item()
        
    def test_subclass(self):
        class Armor(pyzork.Armor):
            def buff(armor, user):
                """Some thick armor."""
                return [(self.stat, self.buff)]
                
            def effect(armor, target):
                """Poisoned thick armor"""
                target.take_pure_damage(self.damage)
                
        self.item = Armor()
        
        self.assertEqual(self.item.name, "Armor")
        self.assertEqual(self.item.description, "Some thick armor. Poisoned thick armor")
        
        self.check_item()
    
class TestShopItem(unittest.TestCase):
    def setUp(self):
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
    
    def test(self):
        class Sword(pyzork.Weapon):
            pass
        
        self.player = pyzork.Player(money=500)
        sword = pyzork.ShopItem(item=Sword, price=25, amount=1)
        
        money = self.player.money
        sword.buy(self.player)
        
        self.assertEqual(self.player.money, money - sword.price)
        self.assertEqual(len(self.player.inventory.equipment), 1)
        
        sword.buy(self.player)
        
        self.assertEqual(self.player.money, money - sword.price)
        self.assertEqual(len(self.player.inventory.equipment), 1)
        
        sword.sell(self.player, 1)
        
        self.assertEqual(self.player.money, money)
        self.assertEqual(len(self.player.inventory.equipment), 0)
                

class TestInventory(unittest.TestCase):
    def setUp(self):
        pyzork.utils.update_output(lambda text: None)

    def tearDown(self):
        pyzork.utils.update_output(lambda text: print(text))
        
    def test(self):
        class Sword(pyzork.Weapon):
            pass
            
        class Shield(pyzork.Weapon):
            pass
            
        class BigArmor(pyzork.Armor):
            pass
            
        class HealthPotion(pyzork.Consumable):
            def __init__(self):
                super().__init__(charges=1)
            
        class HealingOnguent(pyzork.Consumable):
            def __init__(self):
                super().__init__(charges=1)
            
        class ImportantKey(pyzork.QuestItem):
            pass
            
        
        class Spear(pyzork.Weapon):
            pass
            
        class SpearThingy(pyzork.Consumable):
            def __init__(self):
                super().__init__(charges=1)
                
        class OldSpear(pyzork.QuestItem):
            pass

        inventory = pyzork.Inventory(items=[Sword(), Shield(), HealthPotion(), BigArmor(), HealingOnguent(), ImportantKey()])
        
        player = pyzork.Player()
        
        inventory.add_item(OldSpear())
        inventory.add_item(SpearThingy())
        inventory.add_item(Spear())
        
        item = inventory.get_consumable(name="HealingOnguent")
        
        inventory.use_item(item, player)
        
        item = inventory.get_consumable(name="HealingOnguent")
        self.assertIs(item, None)
        
        item = inventory.get_equipment(name="Spear")
        
        inventory.equip_item(item)
        self.assertIs(inventory.weapon, item)
        
        item = inventory.get_equipment(name="Spear")
        self.assertIs(item, None)
        
        item = inventory.get_quest(name="OldSpear")
        inventory.remove_item(item)
        
        item = inventory.get_quest(name="OldSpear")
        self.assertIs(item, None)
        
        inventory.print()
        
        item = inventory.get_item(name="BigArmor")
        self.assertIsNot(item, None)
        
        
