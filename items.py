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

class Item:
    def __init__(self, world, itemname, description, itemtype):
        self.itemname = itemname
        self.world = world
        self.description = description
        self.itemtype = itemtype

    # All items, when viewed from the inventory, can be examined or dropped. Drop calls the drop function from the player on this item.
    # Examine will print the description of the item.

class Consumable(Item):
    def __init__(self, world, itemname, description, type_, heal=None, stat=None, statnum=None):
        Item.__init__(self, world, itemname, description, itemtype="Consumable")
        self.heal = heal
        self.stat = stat
        self.type_ = type_
        self.statnum = statnum


class Armor(Item):
    def __init__(self, world, itemname, description, damreduction, slot):
        Item.__init__(self, world, itemname, description, itemtype="Armor")
        self.damreduction = damreduction 
        self.slot = slot
        # Armor slots are: helmet, body, leggings, gauntlets, and boots.

class Weapon(Item):
    def __init__(self, world, itemname, description, weapontype):
        Item.__init__(self, world, itemname, description, itemtype="Weapon")
        self.weapontype = weapontype

class Sword(Weapon):
    def __init__(self, world, itemname, description, mindam, maxdam):
        Weapon.__init__(self, world, itemname, description, weapontype="Sword")
        self.mindam = mindam
        self.maxdam = maxdam
        self.abilities = [["Slash", True, 3, self.mindam, self.maxdam],["Stab", True, 2, self.mindam-4, self.maxdam-3], ["Overhead", True, 3, self.mindam-4, self.maxdam+5]]
    def attack(self):
        return random.randrange(self.mindam, self.maxdam)

class Axe(Weapon):
    def __init__(self, world, itemname, description, mindam, maxdam):
        Weapon.__init__(self, world, itemname, description, weapontype="Axe")
        self.mindam = mindam
        self.maxdam = maxdam
        self.abilities = [["Slash", True, 3, self.mindam, self.maxdam],["Axeblade", True, 3, self.mindam-2, self.maxdam+4]]
