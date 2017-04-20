from player import Player
import random
def checkInput(inputprompt, allowed, errormsg):
    while True:
        input_ = int(input(str(inputprompt)))
        if input_ in allowed:
            return input_
            break
        else:
            print(str(errormsg)+"\n")


class Enemy:
    def __init__(self, world, name, health, description):
        self.name = name
        self.world = world
        self.health = health
        self.desc = description
        self.damage = None
    
    def damaged(self, dam):
        self.health -= dam

    def getDesc(self):
        print(str(self.desc))

class Human(Player):
    def __init__(self, world, wep, name, stn, agi, inc, luck, ten, description1, description2):
        Player.__init__(self, world, wep, stn, agi, inc, luck, ten)
        self.isPlayer = False
        self.name = name
        self.abilities = [["Kick", True, 1, 0, 2], ["Dodge", False, 1]]
        self.equipped = wep
        self.equip(self.equipped)
        self.description1 = description1
        self.description2 = description2
        # Humans, enemy or friendly, are naturally quite similar to the player. Therefore, I made humans generally inherit
        # from the player class. The major differences are in equip() and getattacks(): obviously, it makes no sense for
        # the player to have a choice in what other humans decide to do, so getattacks() now just chooses a random ability
        # from the ability list. Similarly, instead of giving the player a prompt when equipping, equip now takes as input
        # the weapon to equip, and equips it durint initialization. Everything else is pretty much the same (so far). 

    def damageEnemy(self):
        if self.world.p.dodging:
            print("You have dodged the attack.")
            self.world.p.dodging = False
        else:
            self.world.p.health -= self.damage
            print("You have taken "+str(self.damage)+" damage.")
            print("Your health: "+str(self.world.p.health)+ " HP.")

    def equip(self, weapon):
        for ability in weapon.abilities:
            self.abilities.append(ability)


    def getattacks(self):
        self.ability = random.randrange(0, len(self.abilities)-1)
        print(str(self.name)+" prepares to use "+self.abilities[self.ability][0]+" in "+str(self.abilities[self.ability][2])+" turns."+"\n")
        if self.abilities[self.ability][0] == "Dodge":
            print(str(self.name)+" will dodge next turn."+"\n")
            self.dodging = True
        self.attackturn = self.world.turn + self.abilities[self.ability][2]
        if self.abilities[self.ability][1]:
            self.targetlimb = random.randrange(0, len(self.world.p.limbs)-1)
            crit = random.randrange(0,100)
            if crit < self.critChance:
                self.damage = int(self.abilities[self.ability][4]*(self.stn/10))*2
                self.critical = True
            else:
                self.damage = int(random.randrange(self.abilities[self.ability][3], self.abilities[self.ability][4])*(self.stn/10))
            self.world.edamagedealt = True

    def attack(self):
        if self.dodging:
            self.dodging = False
            # In case enemy/player uses dodge last turn when the other was not attacking (essentially making sure "dodging" will last one turn).
        if self.world.turn == 1 or self.world.turn == self.attackturn:
            self.world.edamagedealt = False
            self.getattacks()
        else:
            print(str(self.name)+" is preparing to use "+str(self.abilities[self.ability][0]+" in "+str(self.attackturn-self.world.turn)+"."+"\n"))
    