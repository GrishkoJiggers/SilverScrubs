from player import Player
import random

def checkInput(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    print(template.format(" or ".join((", ".join(map(str,
                                                                     range_[:-1])),
                                                       str(range_[-1])))))
        else:
            return ui


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
        Player.__init__(self, world, stn, agi, inc, luck, ten, startInv=None)
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

    def loot(self):
        droplist = []
        droplist.append([self.equipped.itemname, self.equipped])
        droplist.append(["Coins", int(random.randrange(0,30))])
        specialdrop = random.randrange(0,100)+10
        if self.world.p.luck >= specialdrop:
            droplist.append(random.choice[[serum.itemname, serum], [salve.itemname, salve], [luckrock.itemname, luckrock]])
        while True:
            for item in droplist:
                if item[0] == "Coins":
                    print(str(droplist.index(item))+": "+str(item[1])+" coins.")
                else:
                    print(str(droplist.index(item))+": "+str(item[0]))
            print(str(len(droplist))+": Leave.")
            take = checkInput("Take an item? ", type_=int, min_=0, max_=len(droplist))
            if take < len(droplist):
                if droplist[take][0] != "Coins":
                    self.world.p.pickup(droplist[take][1])
                    print("You have taken "+str(droplist[take][0]+"."+"\n"))
                    droplist.remove(droplist[take])
                    continue
                else:
                    self.world.p.money += droplist[take][1]
                    print(str(droplist[take][1])+" coins added."+"\n")
                    droplist.remove(droplist[take])
                    continue
            elif take == len(droplist):
                break

    
