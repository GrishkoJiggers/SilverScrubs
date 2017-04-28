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

class Player:
    def __init__(self, world, stn, agi, inc, luck, ten, startInv):
        self.isAlive = True
        self.inv = startInv
        self.money = 30
        self.stn = stn
        self.agi = agi
        self.inc = inc
        self.luck = luck
        self.ten = ten
        self.armor = [None, None, None, None]
        # Here, entries in the list correspond to armor objects. Where they are located in the list matters. Upon equipping, pieces of armor are put
        # in the correct slot based on the number that corresponds to slot in the armor item.

        self.dodgeChance = (self.agi/10)*100//1
        self.hitChance = int((self.inc/20)*100)+65
        self.health = int(self.ten*20)
        self.critChance = int(100/self.luck)
        self.world = world
        self.equipped = None
        self.attacking = False
        self.critical = False
        self.attackturn = None
        self.damage = None
        self.ability = None
        self.dodging = False
        self.currentaction = "Nothing"
        self.abilities = [["Kick", True, 1, 2, 3], ["Dodge", False, 1], ["Observe", False, 1], ["Switch weapon", False, 1]]
        self.equipQueue = None
        self.canequip = True
        # These are the starting abilities which the player can use regardless of equipped weapon. When a weapon is equipped, its abilities are appended to this list.
        # When unequipped, those abilities are taken off.

        self.Luparm = ["Left upper arm", int((self.ten/10)*200), 0.85, 0, 3]
        self.Ruparm = ["Right upper arm", int((self.ten/10)*200), 0.85, 0, 3]
        self.Llowarm = ["Left lower arm", int((self.ten/10)*200), 0.70, 0, 3]
        self.Rlowarm = ["Right lower arm", int((self.ten/10)*200), 0.70, 0, 3]
        self.head = ["Head", int((self.ten/10)*200), 1.50, 0, 0]
        self.upbody = ["Upper body", int((self.ten/10)*200), 1, 0, 1]
        self.lowbody = ["Lower body", int((self.ten/10)*200), 1.25, 0, 1]
        self.Rleg = ["Right leg", int((self.ten/10)*200), 0.85, 0, 2]
        self.Lleg = ["Left leg", int((self.ten/10)*200), 0.85, 0, 2]

        # These are the players (and generally all humans') limbs. The first item is the name of the body part, the second is the health of that limb (which scales with tenacity), and the third 
        # item is the "quality factor." Basically, when damage is taken to a limb, the damage multiplied by the quality factor is how much the person's total health is reduced by. So, damage taken
        # to the head is 50% more damaging to the player as damage taken to the upper body, for instance. <<WORK IN PROGRESS>> The last item is the condition it the limb: 0 is fine, 1 is weakened, 2 is crippled, and 3
        # is severed. As a limb's condition deteriorates, certain status effects are applied. The head, for example, if weakened, results in intelligence and accuracy loss. Damage to the legs results
        # in agility loss. Damage to the upper arms affects melee damage. Damage to the lower arms may make you drop your weapon. <<WORK IN PROGRESS>>. The last item in these

        self.limbs = [self.Luparm, self.Ruparm, self.Llowarm, self.Rlowarm, self.head, self.upbody, self.lowbody, self.Rleg, self.Lleg]
        self.targetlimb = None
        self.coords = [0, 5]
        self.proximity = [[0,4], [0,6], [1,4], [1,5],[1,6]]
        self.bearings = []
        



    def stats(self):
        print("Strength: "+str(self.stn)+"\n"+"Agility: "+str(self.agi)+"\n"+"Intelligence: "+str(self.inc)+"\n"+"Luck: "+str(self.luck)+"\n"+"Tenacity: "+str(self.ten))


    def pickup(self, itemObject):
        self.inv[itemObject.itemname] = itemObject
    


    def inventory(self):   
        while True:
            invlist=[]
            actionlist = []
            for obj in self.inv:
                invlist.append(obj)
                if self.inv[obj] == self.equipped or self.inv[obj] in self.armor:
                    print(str(invlist.index(obj))+": "+str(obj)+" (Equipped)")
                else:
                    print(str(invlist.index(obj))+": "+str(obj))
            print(str(len(invlist))+": Back")
            use = checkInput("Select an item: ", type_=int, min_=0, max_=len(invlist))
            if use != len(invlist):
                chosenitem = invlist[use]
            else:
                break
            realitem = self.inv[chosenitem]
            # Chosenitem is the string corresponding to an item that you choose from the inventory LIST. This string corresponds to an item object
            # only when referenced in the self.inv dictionary, hence "realitem," which is just the dictionary value of the list placeholder.
            if realitem.itemtype == "Weapon" or realitem.itemtype == "Armor":
                actionlist = [[self.equip, "Equip"], [self.drop, "Drop"], [self.examine, "Examine"], ["Placeholder", "Back"]]
                if realitem == self.equipped:
                    actionlist.append([self.dequip, "Unequip"])
            elif realitem.itemtype == "Consumable":
                actionlist = [[self.use, "Use"], [self.drop, "Drop"], [self.examine, "Examine"], ["Placeholder", "Back"]]
            else:
                actionlist = [[self.drop, "Drop"], [self.examine, "Examine"], ["Placeholder", "Back"]]
                # actionlist describes what you can do with the item you've selected. The functions in these pairs correspond to the actual method
                # that is called when the player chooses something.

            for action in actionlist:
                print(str(actionlist.index(action))+" : "+action[1])
            itemaction = checkInput("What would you like to do with "+str(realitem.itemname)+"? ",type_=int, min_=0, max_=len(actionlist)-1)
            if actionlist[itemaction][1] == "Back":
                return None
                # Essentially, if the player selects "back," inventory will return None, returning to the main loop. The "placeholder" string is
                # Just there to make sure the index for "Back" remains [1].
            else:
                actionlist[itemaction][0](realitem)
            # If the player does not select back, then the function corresponding to what the player chose (defined below) will be applied to the item in question.


    def examine(self, itemObject):
        print(itemObject.description)
        # Prints the description of whatever item is examined. 

    def use(self, itemObject):
        if itemObject.type_ == "Healing":
            self.health += itemObject.heal
            print("You have healed for "+str(itemObject.heal)+" health."+"\n")
            if self.health > int(self.ten*20):
                self.health = int(self.ten*20)
            # Ensures the player can only heal to max HP.

        elif itemObject.type_ == "Stat":
            if itemObject.stat == "Strength":
                self.stn += itemObject.statnum
            elif itemObject.stat == "Agility":
                self.agi += itemObject.statnum
            elif itemObject.stat == "Intelligence":
                self.inc += itemObject.statnum
            elif itemObject.stat == "Luck":
                self.luck += itemObject.statnum
            elif itemObject.stat == "Tenacity":
                self.ten += itemObject.statnum
            print("Your "+itemObject.stat+" has increased by "+str(itemObject.statnum)+"!")
        del self.inv[itemObject.itemname]
        # Checks the type of consumable that has been used. If the item is a "Healing" type item, it will heal the player for however much health is specified.
        # If it is a "Stat" item, it will increase a certain stat by a certain amount (statnum)



    def equip(self, itemObject):
        if itemObject.itemtype == "Weapon":
            if self.equipped == None:
                for ability in itemObject.abilities:
                    self.abilities.append(ability)
                self.equipped = itemObject
            else:
                for ability in self.equipped.abilities:
                    self.abilities.remove(ability)
                print("You have unequipped "+str(self.equipped.itemname)+".")
                for ability in itemObject.abilities:
                    self.abilities.append(ability)
                self.equipped = itemObject
            print("You have equipped "+str(itemObject.itemname)+"."+"\n")
        elif itemObject.itemtype == "Armor":
            if self.armor[itemObject.slot] != None:
                print("You have unequipped "+str(self.armor[itemObject.slot].itemname)+".")
            self.armor[itemObject.slot] = itemObject
            print("You have equipped "+str(itemObject.itemname)+"."+"\n")

        # When an item is equipped, it sets that item to the self.equipped attribute, and systematically adds its abilities to the player's combat abilities. If another
        # item is equipped when the player equips an item, it unequips that item first.

    def drop(self, itemObject):
        if itemObject == self.equipped:
            self.dequip(itemObject)
        del self.inv[itemObject.itemname]
        print("You have dropped "+str(itemObject.itemname)+".")
        # If you drop an item, it is removed from the player's inventory. If that item is equipped, it is unequipped first.

    def act(self):
        while True:
            actions = [[self.inventory, "Inventory"]]
            for action in actions:
                print(str(actions.index(action))+": "+str(action[1]))
            do = checkInput("What will you do? "+"\n", type_=int, min_=0, max_=len(actions)-1)
            actions[do][0]()
            if actions[do][1] == "Travel":
                break
 

    def dequip(self, itemObject):
        for item in self.equipped.abilities:
            self.abilities.remove(item)
        self.equipped = None

    
    # COMBAT METHODS
    ######################################################################################################################################################################################################
    # As shown in the world object, combat is turn based. Assuming the player is not in the middle of attacking, the player will be given a number of options depending on available abilities.

    def swap(self):
        weplist = []
        for obj in self.inv:
            if self.inv[obj].itemtype == "Weapon" and self.inv[obj] != self.equipped:
                weplist.append(obj)
                print(str(weplist.index(obj))+": "+str(obj))
        if len(weplist) == 0:
            print("You have no other weapons."+"\n")
            self.getattacks()
        elif self.canequip == False:
            print("You cannot equip any weapons (your hand is missing!)"+"\n")
            self.getattacks()
        else:
            switch = checkInput("Select a weapon to equip: ", type_=int, min_=0, max_=len(weplist)-1)
            self.equipQueue = self.inv[weplist[switch]]
            print("You begin to switch weapons."+"\n")
        # For switching weapons in combat. 

    def getattacks(self):
    
        for item in self.abilities:
            if item[1] == True:
                print(str(self.abilities.index(item))+": "+str(item[0])+": "+str(int(item[3]*self.stn/6))+" to "+str(int(item[4]*self.stn/6))+" damage. "+str(item[2])+" turns.")
            elif item[1] == False:
                print(str(self.abilities.index(item))+": "+str(item[0])+": "+str(item[2])+" turns.")
        # Above displays the available abilities, giving numbers to press for each one.

        self.ability = checkInput("Choose an ability: "+"\n", type_=int, min_=0, max_=len(self.abilities)-1) 
        if self.abilities[self.ability][1]:
            for limb in self.world.currenemy.limbs:
                print(str(self.world.currenemy.limbs.index(limb))+": "+str(limb[0])+": "+str(limb[1])+" HP.")
            self.targetlimb = checkInput("Where to attack: "+"\n", type_=int, min_=0, max_=len(self.world.currenemy.limbs)-1)
        # The ability is checked for the "damaging" attribute, where 1 means that the ability is an attack, and then prompts the player to choose where to direct the attack.

        if self.abilities[self.ability][0] == "Observe":
            print("You closely examine the enemy..."+"\n")
        # If the player chooses to observe, then it will tell this to the player, and when it's the player's attack turn, a description will be given.

        elif self.abilities[self.ability][0] == "Switch weapon":
            self.swap()
            

        elif self.abilities[self.ability][0] != "Dodge":
            print("You prepare to "+self.abilities[self.ability][0]+"."+"\n")
        # With the exception of dodging, this message is displayed when you use an ability.

        else:
            self.dodging = True
            print("You prepare to dodge any oncoming attack (next turn)"+"\n")
        # If the player is in a dodging state, then this message is displayed to indicate that they will dodge next turn's attack.

        self.attackturn = self.world.turn + self.abilities[self.ability][2]
        if self.abilities[self.ability][1]:
            crit = random.randrange(0,100)
            if crit < self.critChance:
                self.damage = int(self.abilities[self.ability][4]*(self.stn/6))*2
                self.critical = True
            else:
                self.damage = int(random.randrange(self.abilities[self.ability][3], self.abilities[self.ability][4])*(self.stn/6))
            self.world.pdamagedealt = True
                
    def takeDamage(self, amount, limb):
        damagetaken = None
        if self.armor[self.limbs[limb][4]] != None:
            damagetaken = int(amount*self.armor[self.limbs[limb][4]].damreduction*self.limbs[limb][2])
            self.health -= damagetaken
            self.limbs[limb][1] -= int(damagetaken/self.limbs[limb][2])
        else:
            damagetaken = int(amount*self.limbs[limb][2])
            self.health -= damagetaken
            self.limbs[limb][1] -= int(damagetaken/self.limbs[limb][2])
        return damagetaken



    def attack(self):
        self.critical = False
        if self.equipQueue != None:
            self.equip(self.equipQueue)
            self.equipQueue = None
        if self.dodging:
            self.dodging = False
            # In case enemy/player uses dodge last turn when the other was not attacking (essentially making sure "dodging" will last one turn).
        if self.world.turn == 1 or self.world.turn == self.attackturn:
            self.world.pdamagedealt = False
            self.getattacks()
        else:
            print("You are preparing to use "+str(self.abilities[self.ability][0]+" in "+str(self.attackturn-self.world.turn)+"."+"\n"))
            # Controls what is displayed when it is not the player's turn to attack.



