import entities
import abilities
import battle

p = entities.Player()
s = abilities.WarRoarSpell()
p.abilities.append(s)
b = battle.Battle(p, [entities.Goblin()], "Bork")
