import random

def checkInput(inputprompt, allowed, errormsg):
    while True:
        input_ = int(input(str(inputprompt)))
        if input_ in allowed:
            return input_
            break
        else:
            print(str(errormsg)+"\n")

class Item:
    def __init__(self, world, itemname):
        self.itemname = itemname
        self.world = world

class Weapon(Item):
    def __init__(self, world, itemname, weapontype):
        Item.__init__(self,world, itemname)
        self.weapontype = weapontype

class Sword(Weapon):
    def __init__(self, world, itemname, mindam, maxdam):
        Weapon.__init__(self, world, itemname, weapontype="Sword")
        self.mindam = mindam
        self.maxdam = maxdam
        self.abilities = [["Slash", True, 3, self.mindam, self.maxdam],["Stab", True, 2, self.mindam-4, self.maxdam-6], ["Overhead", True, 3, self.mindam-4, self.maxdam+5]]
    def attack(self):
        return random.randrange(self.mindam, self.maxdam)

class Axe(Weapon):
    def __init__(self, world, itemname, mindam, maxdam):
        Weapon.__init__(self, world, itemname, weapontype="Axe")
        self.mindam = mindam
        self.maxdam = maxdam
        self.abilities = [["Slash", True, 3, 22, 28],["Axeblade", True, 3, 25, 26]]
