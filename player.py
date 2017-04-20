import random
def checkInput(inputprompt, allowed, errormsg):
    while True:
        input_ = int(input(str(inputprompt)))
        if input_ in allowed:
            return input_
            break
        else:
            print(str(errormsg)+"\n")

class Player:
    def __init__(self, world, wep, stn, agi, inc, luck, ten):
        self.isPlayer = True
        self.inv = {wep.itemname:wep}
        self.startWep = wep
        self.stn = stn
        self.agi = agi
        self.inc = inc
        self.luck = luck
        self.ten = ten
        self.dodgeChance = (self.agi/10)*100//1
        self.hitChance = int((self.inc/20)*100)+65
        self.health = int(self.ten*20)
        self.critChance = int(100/self.luck)
        self.world = world
        self.equipped = self.startWep
        self.attacking = False
        self.critical = False
        self.attackturn = None
        self.damage = None
        self.ability = None
        self.dodging = False
        self.currentaction = "Nothing"
        self.abilities = [["Kick", True, 1, 2, 3], ["Dodge", False, 1], ["Observe", False, 1]]
        self.autoEquip()
        
        # Wepabilities is a list that belongs to the player, which defines abilities depending on equipped weapon.
        # Every item in the ability list corresponds to name, whether it is a damaging ability, min damage, max damage if it is, and turn cost. ORDER MUST BE THE SAME FOR EVERY ENTRY.

        self.Luparm = ["Left upper arm", int((self.ten/10)*200), 0.85, 0]
        self.Ruparm = ["Right upper arm", int((self.ten/10)*200), 0.85, 0]
        self.Llowarm = ["Left lower arm", int((self.ten/10)*200), 0.70, 0]
        self.Rlowarm = ["Right lower arm", int((self.ten/10)*200), 0.70, 0]
        self.head = ["Head", int((self.ten/10)*200), 1.50, 0]
        self.upbody = ["Upper body", int((self.ten/10)*200), 1, 0]
        self.lowbody = ["Lower body", int((self.ten/10)*200), 1.25, 0]
        self.Rleg = ["Right leg", int((self.ten/10)*200), 0.85, 0]
        self.Lleg = ["Left leg", int((self.ten/10)*200), 0.85, 0]

        # These are the players (and generally all humans') limbs. The first item is the name of the body part, the second is the health of that limb (which scales with tenacity), and the third 
        # item is the "quality factor." Basically, when damage is taken to a limb, the damage multiplied by the quality factor is how much the person's total health is reduced by. So, damage taken
        # to the head is 50% more damaging to the player as damage taken to the upper body, for instance. <<WORK IN PROGRESS>> The last item is the condition it the limb: 0 is fine, 1 is weakened, 2 is crippled, and 3
        # is severed. As a limb's condition deteriorates, certain status effects are applied. The head, for example, if weakened, results in intelligence and accuracy loss. Damage to the legs results
        # in agility loss. Damage to the upper arms affects melee damage. Damage to the lower arms may make you drop your weapon. <<WORK IN PROGRESS>>

        self.limbs = [self.Luparm, self.Ruparm, self.Llowarm, self.Rlowarm, self.head, self.upbody, self.lowbody, self.Rleg, self.Lleg]
        self.targetlimb = None
        self.coords = [0, 5]
        self.bearings = []
        

        

    def getBearings(self):
        self.bearings = ["W","SW","S","SE","E","NE","N","NW"]
        if self.coords[1] == 0:
            self.bearings.remove("SW")
            self.bearings.remove("NW")
            self.bearings.remove("W")
        if self.coords[1] == 10:
            self.bearings.remove("SE")
            self.bearings.remove("NE")
            self.bearings.remove("E")
        if self.coords[0] == 0:
            self.bearings.remove("N")
            self.bearings.remove("NE")
            self.bearings.remove("NW")
        if self.coords[0] == 9:
            self.bearings.remove("SW")
            self.bearings.remove("SE")
        for direction in self.bearings:
            print(str(self.bearings.index(direction))+": "+ str(direction))

    # Every time getBearings() is called, it makes the list of all possible directions, then narrows it down based on where you are. If you're in the last row,
    # you can still go south, thus progressing to the next region.

    def move(self):
        self.getBearings()
        go = checkInput("Choose your bearings: "+"\n", list(range(0,len(self.bearings))), "Invalid direction. Choose a number corresponding to a direction: "+"\n")
        direction = self.bearings[go]
        if direction == "W":
            self.coords[1] -= 1
        elif direction == "SW":
            self.coords[0] += 1
            self.coords[1] -= 1
        elif direction == "S":
            self.coords[0] += 1
        elif direction == "SE":
            self.coords[0] += 1
            self.coords[1] += 1
        elif direction == "E":
            self.coords[1] += 1
        elif direction == "NE":
            self.coords[0] -= 1
            self.coords[1] += 1
        elif direction == "N":
            self.coords[0] -= 1
        elif direction == "NW":
            self.coords[0] -= 1
            self.coords[1] -= 1



    def stats(self):
        print("Strength: "+str(self.stn)+"\n"+"Agility: "+str(self.agi)+"\n"+"Intelligence: "+str(self.inc)+"\n"+"Luck: "+str(self.luck)+"\n"+"Tenacity: "+str(self.ten))


    def pickup(self, itemObject):
        self.inv[itemObject.itemname] = itemObject
   
    def drop(self, itemObject):
        del self.inv[itemObject]
        # Note: I may change this to pop later so that things can be dropped into their surroundings, instead of being removed completely

    def inventory(self):   
        self.invlist=[]
        for item in self.inv:
            self.invlist.append(item)
            print(str(self.invlist.index(item))+": "+str(item))
        use = checkInput("Use an item? "+"\n", list(range(0,len(self.inv))), "No such item. Choose a number to use an item: "+"\n")


    def act(self):
        while True:
            actions = [[self.move, "Travel"], [self.inventory, "Inventory"]]
            for action in actions:
                print(str(actions.index(action))+": "+str(action[1]))
            do = checkInput("What will you do? "+"\n", list(range(0,len(actions))),"You cannot do that. Choose a number corresponding to an action: "+"\n")
            actions[do][0]()
            if actions[do][1] == "Travel":
                break
    # Note: add more inventory options. Allow equipping from inventory instead of using the equip function, or allow it to be used within the inventory menu.
    # Also have individual numbers that correspond to items. If the item's number is pressed, give options on what can be done with them (i.e. drop, examine, use)

    def autoEquip(self):
        for item in self.equipped.abilities:
            self.abilities.append(item)

    def equip(self):
        invlist = self.inventory()
        print("Your inventory: "+str(invlist))
        if self.equipped == None:
            self.equipped = self.inv[str(input("Choose an item to equip: "))]
            for item in self.equipped.abilities:
                self.abilities.append(item)


    def dequip(self):
        for item in self.equipped.abilities:
            self.abilities.remove(item)
        self.equipped = None

    
    def getattacks(self):
    
        for item in self.abilities:
            if item[1] == True:
                print(str(self.abilities.index(item))+": "+str(item[0])+": "+str(item[3])+" to "+str(item[4])+" damage. "+str(item[2])+" turns.")
            elif item[1] == False:
                print(str(self.abilities.index(item))+": "+str(item[0])+": "+str(item[2])+" turns.")
        # Above displays the available abilities, giving numbers to press for each one.
        self.ability = checkInput("Choose an ability: "+"\n", list(range(0,len(self.abilities))), "No such ability. Choose a number corresponding to an ability: "+"\n") 
        if self.abilities[self.ability][1]:
            for limb in self.world.currenemy.limbs:
                print(str(self.world.currenemy.limbs.index(limb))+": "+str(limb[0])+": "+str(limb[1])+" HP.")
            self.targetlimb = checkInput("Where to attack: "+"\n", list(range(0,len(self.world.currenemy.limbs))), "No such location. Choose a number to target a location: "+"\n")


        if self.abilities[self.ability][0] == "Observe":
            print("You closely examine the enemy..."+"\n")
        elif self.abilities[self.ability][0] != "Dodge":
            print("You prepare to "+self.abilities[self.ability][0]+"."+"\n")
        else:
            self.dodging = True
            print("You prepare to dodge any oncoming attack (next turn)"+"\n")
        self.attackturn = self.world.turn + self.abilities[self.ability][2]
        if self.abilities[self.ability][1]:
            crit = random.randrange(0,100)
            if crit < self.critChance:
                self.damage = int(self.abilities[self.ability][4]*(self.stn/10))*2
                self.critical = True
            else:
                self.damage = int(random.randrange(self.abilities[self.ability][3], self.abilities[self.ability][4])*(self.stn/10))
            self.world.pdamagedealt = True
                

    def attack(self):
        self.critical = False
        if self.dodging:
            self.dodging = False
            # In case enemy/player uses dodge last turn when the other was not attacking (essentially making sure "dodging" will last one turn).
        if self.world.turn == 1 or self.world.turn == self.attackturn:
            self.world.pdamagedealt = False
            self.getattacks()
        else:
            print("You are preparing to use "+str(self.abilities[self.ability][0]+" in "+str(self.attackturn-self.world.turn)+"."+"\n"))
            # Controls what is displayed when it is not the player's turn to attack.

#    def attack(self):
#        self.getattacks()
#        self.attackturn = self.world.turn + self.abilities[self.ability][2]

    def damageEnemy(self):
        if self.world.currenemy.dodging:
            print(str(self.world.currenemy.name)+" has dodged your attack."+"\n")
            self.world.currenemy.dodging = False
        else:
            self.world.currenemy.health -= self.damage
            print(str(self.world.currenemy.name)+" has taken "+str(self.damage)+" damage."+"\n")
            print(str(self.world.currenemy.name)+": "+str(self.world.currenemy.health)+ " HP."+"\n")

    def damaged(self, locname, loch, locq, damage):
        loch -= damage
        self.health -= locq*damage
        if loch < 66:
            print("Your "+str(locname)+" has been injured.")
        elif loch < 33:
            print("Your "+str(locname)+" has been crippled.")
        elif loch <= 0:
            if locname != "Upper body" and locname != "Lower body":
                if self.world.fighting:
                    print("Your "+str(locname)+" has been severed!")