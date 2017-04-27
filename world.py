from tkinter import *
import os
import random
import inspect
from player import *
from enemies import *
from items import *
from encounter import *


         

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
            #print(str(errormsg)+"\n")

# This function is what I use throughout the program to check whether an input falls within a set of expected values.
# If an invalid input is given, a message specific to the context is returned.


def createChar():
    print("Background: "+"\n")
    for item in starts:
        print(str(starts.index(item))+": "+item[0]+": ")
        print(item[6])
        print("************************************************************************************************")
        print("     Strength: "+str(item[1])+".")
        print("     Agility: "+str(item[2])+".")
        print("     Intelligence: "+str(item[3])+".")
        print("     Luck: "+str(item[4])+".")
        print("     Tenacity: "+str(item[5])+"."+"\n")
    global character, startDesc
    character = checkInput("Choose a background: "+"\n", type_=int, min_=0, max_=len(starts)-1)
    player = Player(w, starts[character][1], starts[character][2], starts[character][3], starts[character][4], starts[character][5], starts[character][8])
    startDesc = starts[character][7]
    return player

class World:
    def __init__(self):
        self.p = None
        self.turn = 0
        self.playerturn = 0
        self.enemyturn = 0
        self.fighting = False
        self.pdamagedealt = False
        self.edamagedealt = False
        self.currenemy = None
        self.day = 1
       
    def update(self, enemy):
        if self.p.abilities[self.p.ability][0] == "Observe":
            if self.p.inc >= 8:
                print(str(enemy.name)+" is wielding "+str(enemy.equipped.itemname)+".")
                print(str(enemy.description2))
                print(str(enemy.name)+" stats:")
                print("Strength: "+str(enemy.stn))
                print("Agility: "+str(enemy.agi))
                print("Intelligence: "+str(enemy.inc))
                print("Luck: "+str(enemy.luck))
                print("Tenacity: "+str(enemy.ten))
                print("You're sure it must have a weak spot..."+"\n")
            elif self.p.inc >= 5:
                print(str(enemy.name)+" is wielding "+str(enemy.equipped.itemname)+"."+"\n")
                print(str(enemy.description2)+"\n")
            elif self.p.inc < 5:
                print(str(enemy.name)+" is wielding "+str(enemy.equipped.itemname)+"."+"\n")
                print(str(enemy.description1)+"\n")
        # If the player uses observe, the level of specificity reached by observe depends on intelligence. High (>= 8) intelligence allows a detailed description,
        # gives enemy stats, and shows weak points.
        # Medium tier intelligence gives the detailed description.
        # Lowest tier intelligence gives crappy description.

        if enemy.dodging and (not self.pdamagedealt or self.p.attackturn != self.turn):
            print(str(enemy.name)+" has dodged nothing!"+"\n")
        if self.p.dodging and (not self.edamagedealt or enemy.attackturn != self.turn):
            print("You have dodged nothing!"+"\n")
        # The above conditions are checked in case the player/enemy either dodge a non-damaging ability or dodge when it is not the other's turn to attack.

        if self.p.attackturn == self.turn and enemy.attackturn == self.turn and self.edamagedealt and self.pdamagedealt:
            self.p.health -= self.p.limbs[enemy.targetlimb][2]*enemy.damage
            self.p.limbs[enemy.targetlimb][1] -= enemy.damage
            self.p.health = int(self.p.health)


            enemy.limbs[self.p.targetlimb][1] -= self.p.damage
            enemy.health -= enemy.limbs[self.p.targetlimb][2]*self.p.damage
            enemy.health = int(enemy.health)
            if not self.p.critical and not enemy.critical:
                print(str(enemy.name)+" has used "+str(enemy.abilities[enemy.ability][0])+" for "+str(enemy.damage)+" damage to the "+str(self.p.limbs[enemy.targetlimb][0])+", and you have used "+str(self.p.abilities[self.p.ability][0])+" on "+str(enemy.name)+" for "+str(self.p.damage)+" damage to the "+enemy.limbs[self.p.targetlimb][0]+"."+"\n")
            
            elif self.p.critical and enemy.critical:
                print(str(enemy.name)+" has critically struck with "+str(enemy.abilities[enemy.ability][0])+" for "+str(enemy.damage)+" damage to the "+str(self.p.limbs[enemy.targetlimb][0])+", and you critically struck with "+str(self.p.abilities[self.p.ability][0])+" on "+str(enemy.name)+" for "+str(self.p.damage)+" damage to the "+enemy.limbs[self.p.targetlimb][0]+"."+"\n")
            
            elif self.p.critical and not enemy.critical:
                print(str(enemy.name)+" has used "+str(enemy.abilities[enemy.ability][0])+" for "+str(enemy.damage)+" damage to the "+str(self.p.limbs[enemy.targetlimb][0])+", and you critically struck "+str(self.p.abilities[self.p.ability][0])+" on "+str(enemy.name)+" for "+str(self.p.damage)+" damage to the "+enemy.limbs[self.p.targetlimb][0]+"."+"\n")                
            
            elif not self.p.critical and enemy.critical:
                print(str(enemy.name)+" has critically struck with "+str(enemy.abilities[enemy.ability][0])+" for "+str(enemy.damage)+" damage to the "+str(self.p.limbs[enemy.targetlimb][0])+", and you used "+str(self.p.abilities[self.p.ability][0])+" on "+str(enemy.name)+" for "+str(self.p.damage)+" damage to the "+enemy.limbs[self.p.targetlimb][0]+"."+"\n")
            
            self.condition(enemy)
            # These conditions are for when the enemy and player attack at the same time, or "exchange."

        elif self.p.attackturn == self.turn and self.pdamagedealt and enemy.dodging:
            dodge = random.randrange(0,100)
            if dodge < enemy.dodgeChance:
                print(str(enemy.name)+" has dodged your "+str(self.p.abilities[self.p.ability][0])+"."+"\n")
            else:
                if self.miss(self.p):
                    print("You have missed."+"\n")
                elif self.p.critical:
                    print(str(enemy.name)+" failed to dodge your "+str(self.p.abilities[self.p.ability][0])+" and took "+str(self.p.damage)+" damage to the "+enemy.limbs[self.p.targetlimb][0]+". A critical hit!"+"\n")
                    enemy.limbs[self.p.targetlimb][1] -= self.p.damage
                    enemy.health -= enemy.limbs[self.p.targetlimb][2]*self.p.damage
                    enemy.health = int(enemy.health)
                else:
                    print(str(enemy.name)+" failed to dodge your "+str(self.p.abilities[self.p.ability][0])+" and took "+str(self.p.damage)+" damage to the "+enemy.limbs[self.p.targetlimb][0]+"."+"\n")
                    enemy.limbs[self.p.targetlimb][1] -= self.p.damage
                    enemy.health -= enemy.limbs[self.p.targetlimb][2]*self.p.damage
                    enemy.health = int(enemy.health)
        # If you attack while the enemy is dodging, there is a chance your attack will miss depending on the enemy's agility (dodge chance). If the attack 
        # still lands, it may crit (luck).

        elif enemy.attackturn == self.turn and self.edamagedealt and self.p.dodging:
            dodge = random.randrange(0,100)
            if dodge < self.p.dodgeChance:
                print("You have dodged the enemy "+str(enemy.abilities[enemy.ability][0])+"."+"\n")
            else:
                if self.miss(enemy):
                    print(str(enemy.name)+" has missed."+"\n")
                elif enemy.critical:
                    print("You failed to dodge the enemy "+str(enemy.abilities[enemy.ability][0])+" and took "+str(enemy.damage)+" damage to the "+str(self.p.limbs[enemy.targetlimb][0])+". A critical hit!"+"\n")
                else:
                    print("You failed to dodge the enemy "+str(enemy.abilities[enemy.ability][0])+" and took "+str(enemy.damage)+" damage to the "+str(self.p.limbs[enemy.targetlimb][0])+"."+"\n")
                self.p.health -= self.p.limbs[enemy.targetlimb][2]*enemy.damage
                self.p.limbs[enemy.targetlimb][1] -= enemy.damage
                self.p.health = int(self.p.health)
        # If the enemy is performing a damaging attack while you are in a "dodging state", there is a chance you will evade the attack, which depends on your agility.
        # If the attack lands, there is still a chance the attack will crit.

        elif self.p.attackturn == self.turn and self.pdamagedealt and (not enemy.dodging or enemy.attackturn != self.turn):
            # if self.p.abilities[self.p.ability][0] == "Kick":
            # NOTE: add stuns?
            
            if self.miss(self.p):
                print("You have missed."+"\n")
            elif self.p.critical:
                print("You have used "+str(self.p.abilities[self.p.ability][0])+" on "+str(enemy.name)+" for "+str(self.p.damage)+" damage to the "+enemy.limbs[self.p.targetlimb][0]+". A critical hit!"+"\n")
                enemy.limbs[self.p.targetlimb][1] -= self.p.damage
                enemy.health -= enemy.limbs[self.p.targetlimb][2]*self.p.damage
                enemy.health = int(enemy.health)
            else:
                print("You have used "+str(self.p.abilities[self.p.ability][0])+" on "+str(enemy.name)+" for "+str(self.p.damage)+" damage to the "+enemy.limbs[self.p.targetlimb][0]+"."+"\n")
                enemy.limbs[self.p.targetlimb][1] -= self.p.damage
                enemy.health -= enemy.limbs[self.p.targetlimb][2]*self.p.damage
                enemy.health = int(enemy.health)
            self.condition(enemy)
        # Condition for when player attacks, and enemy neither dodges nor attacks.

        elif enemy.attackturn == self.turn and self.edamagedealt and (not self.p.dodging or self.p.attackturn != self.turn):
            
            if self.miss(enemy):
                print(str(enemy.name)+" has missed."+"\n")
            elif enemy.critical:
                print(str(enemy.name)+" has used "+str(enemy.abilities[enemy.ability][0])+" for "+str(enemy.damage)+" damage to the "+str(self.p.limbs[enemy.targetlimb][0])+". A critical hit!"+"\n")
                self.p.health -= self.p.limbs[enemy.targetlimb][2]*enemy.damage
                self.p.limbs[enemy.targetlimb][1] -= enemy.damage
                self.p.health = int(self.p.health)
            else:
                print(str(enemy.name)+" has used "+str(enemy.abilities[enemy.ability][0])+" for "+str(enemy.damage)+" damage to the "+str(self.p.limbs[enemy.targetlimb][0])+"."+"\n")
                self.p.health -= self.p.limbs[enemy.targetlimb][2]*enemy.damage
                self.p.limbs[enemy.targetlimb][1] -= enemy.damage
                self.p.health = int(self.p.health)
        # Condition for when enemy attacks and player neither dodges nor attacks
    
    def miss(self, entity):
        miss = random.randrange(0,100)
        if miss > entity.hitChance:
            return True

    def condition(self, entity):
        for limb in entity.limbs:
            if limb[1]<=0:
                print(str(entity.name)+" "+limb[0]+" has been severed!"+"\n")
            elif limb[1]<int((entity.ten/10)*200*0.25):
                print(str(entity.name)+" "+limb[0]+" crippled."+"\n")
            elif limb[1]<int((entity.ten/10)*200*0.66):
                print(str(entity.name)+" "+limb[0]+" weakened."+"\n")
            

    def initiate(self, enemy):
        player = self.p
        first = random.choice([enemy, player])
        return first

    def fight(self, enemy):
        player = self.p
        self.fighting = True
        self.turn = 1
        self.currenemy = enemy
        
        while self.fighting:
            print("************************************************************")
            print("TURN "+str(self.turn)+"\n")
            if self.p.attackturn == self.turn or enemy.attackturn == self.turn:
                self.update(enemy)


            print("Player: "+str(self.p.health)+" HP."+"\n")
            print(str(enemy.name)+": "+str(enemy.health)+" HP."+"\n")
            
            if enemy.health <= 0:
                print(str(enemy.name)+" has died."+"\n")
                enemy.loot()
                break
            if self.p.health <= 0:
                print("You have died."+"\n")
                break
            
            enemy.attack()
            self.p.attack()

                        
 
            p = input("Press enter to continue."+"\n")
            self.turn += 1
        
        self.turn = 0
        print("Fight over.")
        self.currenemy = None


w = World()

longsword = Sword(w,"Longsword", "A large double-edged sword. Heavy, but reliable damage.", 8, 17)
shortsword = Sword(w, "Shortsword", "A standard military shortsword. Usually not a first choice for a weapon, but in a pinch, it can prove useful.", 7, 13)
broadsword = Sword(w,"Broadsword", "The most common weapon on the battlefield, with a wide blade. Short and sturdy.",  9, 16)
battleaxe = Axe(w,"Battleaxe", "A heavy and somewhat dull axe, favored by bandits and soldiers alike.", 7, 18)
hoe = Axe(w,"Rusty hoe", "Definitely not meant to be used as a weapon-- still, it is hard and heavy; a weapon for the desperate.", 5, 10)
onehit = Sword(w, "Onehitter", "A magical item used only by the person testing the code.", 200, 202)

salve = Consumable(w, "Healing salve", "A medicinal salve made by soaking medicinal ointments and herbs into a bandage. Heals for 30 HP.", "Healing", heal=30)
luckrock = Consumable(w, "Lucky rock", "Folk tales tell that tossing this rock as far as you can brings good luck. It couldn't hurt to try...", "Stat", stat="Luck", statnum=2)
serum = Consumable(w, "Serum", "Mystics and druids often peddle snake oils claiming to bring supernatural strength. Though unlikely, these substances were banned in many athletic competitions back home... so perhaps they work after all?", "Stat", stat="Strength", statnum=1)



starts = [["SCOUT", 3, 6, 6, 7, 4, "Quick and precise, with relatively high critical chance and perception. Starts with a shortsword.", "You are a scout of the Slate Empire. Time and time again, you have watched as the fertile fields and lush forests you scouted were mired with the blood of enemies and allies alike. This time, however, you decide that this war-- your war, is over.", {shortsword.itemname:shortsword, salve.itemname:salve}], ["INFANTRYMAN", 6, 5, 4, 5, 6, "Common foot soldier with generally well-rounded stats. Starts with a battleaxe.", "Freshly drafted from a small farm in the South, you have fought on the front lines enough to be considered a miraculous survivor, as not many survive the front lines. Every battle may be one's last-- and this is not where you die.", {battleaxe.itemname:battleaxe, salve.itemname:salve}], ["OFFICER", 4, 4, 8, 4, 5, "Low-ranking officer. Not particularly skilled, but relatively clever and well-equipped. Starts with a longsword, a dagger, and armor.", "Recruited from a family of poor nobles, you have been hastily trained to command troops on the battlefield, despite having no experience in combat. It did not take long, however, for your appetite for war to be sated-- shortly after your first foray into the Ashen Wood, you have seen enough. You decide that you'd rather live in shame than die like so many of your subordinates.", {longsword.itemname:longsword, salve.itemname:salve, luckrock.itemname:luckrock}]]

w.p = createChar()



peasant = Human(w, hoe, "Peasant", 3, 3, 1, 1, 1, "It looks like a peasant. He's angry.", "An angry peasant. Basically as weak as they come, in most respects."+"\n")
bandit = Human(w, battleaxe, "Bandit", 7, 3, 1, 5, 7, "A big, scary bandit. He looks angry.", "A bandit common to these parts. Strong, but not too quick."+"\n")
thief = Human(w, broadsword, "Thief", 5, 10, 4, 10, 4, "He looks skinny. Probably a thief.", "A thief looking to make a score. He looks quick, and probably relies heavily on luck for damage."+"\n")

startspiel = ("The Republic of Ashen Wood and Empire of Slate, the two great powers of the world, have been at war for centuries. The reason for the war has been lost to time, as the conflict is as old as the countries that wage it. The last few decades of the Slate Empire have been marked by a ruthless campaign north towards the heart of Ashen Wood-- at devastating costs to both sides."+"\n")

startencounter = Encounter(w, str(startspiel)+"\n"+str(startDesc)+"\n", "Start your journey.", outcome=["", 3])

testencounter = Encounter(w, "This is a test encounter.", "Do nothing", option2 = "Also do nothing")
testencounter1 = Encounter(w, "You stumble upon a cottage by a creek. It seems as though someone managed to remain undetected by the armies of Slate. Smoke rises from the chimney, and there is light inside the cottage." , "Knock on the door", option1 = "Smash down the door.", option2="Leave.", enemy = thief, outcome = ["The door is unlocked. As you enter, you see a thief rifling through the remains of a man and woman, blood fresh on their clothes. Seeking to protect his loot, the thief prepares to make another score.", 0], outcome1 = ["A merchant is tied up inside the house. You untie him, and as thanks, he offers to show you his wares.", 2], outcome2 = ["You prepare to leave.", 3])
testencounter2 = Encounter(w, "You meet a strange old man.", "Talk to him", enemy = peasant, option1 = "Threaten him to give you his valuables.", outcome = ["'Hello,' says the old man.",1], outcome1 = ["Oh, no you don't, sonny Jim!",0], prompt = "Tell me, what bread is best bread?", conv = "Garlic bread is best bread.", resp = ["'That is correct,' he says. You shrug and prepare to move on.", 3], conv1 = "I dunno... French bread?", resp1 = ["'That is incorrect! Prepare for destruction!' he shrieks. Looks like you have to put the old man down.",0])
encounters1 = [testencounter, testencounter1, testencounter2]

        










