import random

def checkInput(inputprompt, allowed, errormsg):
    while True:
        input_ = int(input(str(inputprompt)))
        if input_ in allowed:
            return input_
            break
        else:
            print(str(errormsg)+"\n")

class Encounter:
    def __init__(self, world, text, option, enemy = None, enemy1 = None, option1 = None, option2 = None, option3 = None, outcome = None, outcome1 = None, outcome2 = None, outcome3 = None, prompt=None, resp=None, conv = None, conv1 = None, conv2 = None, conv3 = None, resp1=None, resp2=None, resp3=None):
        # Options will be represented by strings, and outcomes will be duples of strings and the methods that accompany them [string, method #]. If the method number is 0, a fight 
        # will happen. If method number is 1, a conversation takes place. The Prompt and Resp parms are what talk1() uses in the event of a conversation. Prompt is the initial
        # "conversation starter," resp is one of the available responses (also in the forms of string-method# duples, in case you say something that starts a fight or starts a 
        # trade.
        self.world = world
        self.directions = ["Southwest", "South", "Southeast"]
        self.enemy = enemy
        self.text = text
        self.prompt = prompt
        self.conv, self.conv1, self.conv2, self.conv3 = conv, conv1, conv2, conv3
        self.convs = [self.conv, self.conv1, self.conv2, self.conv3]
        self.resp, self.resp1, self.resp2, self.resp3 = resp, resp1, resp2, resp3
        self.resps = [self.resp, self.resp1, self.resp2, self.resp3]
        self.option, self.option1, self.option2, self.option3 = option, option1, option2, option3
        self.options = [self.option, self.option1, self.option2, self.option3]
        self.outcome, self.outcome1, self.outcome2, self.outcome3 = outcome, outcome1, outcome2, outcome3
        self.outcomes = [self.outcome, self.outcome1, self.outcome2, self.outcome3]

    def runEncounter(self):
        print(str(self.text)+"\n")
        indexLen = 0
        for option in [self.option, self.option1, self.option2, self.option3]:
            if option != None:
                indexLen += 1
                print(str(self.options.index(option))+": "+str(option))
        action = checkInput("What will you do? "+"\n", list(range(0,indexLen)), "Not an option. Choose a number to act: "+"\n")
        if action == 0:
            print(str(self.outcome[0]))
            self.encounterCheck(self.outcome[1])
        elif action == 1:
            print(str(self.outcome1[0]))
            self.encounterCheck(self.outcome1[1])
        elif action == 2:
            print(str(self.outcome2[0]))
            self.encounterCheck(self.outcome2[1])



    def nextArea(self):
        direction = checkInput("You must continue south. Choose your bearings: "+"\n", [0,1,2], "You cannot go that way. Choose your bearings: "+"\n")

    def encounterCheck(self, outcomenum):
        # This method checks what the number of the outcome method is and runs the respective method.
        if outcomenum == 0:
            self.conflict0()
        elif outcomenum == 1:
            self.talk1()
        elif outcomenum == 2:
            self.trade2()
        elif outcomenum == 3:
            self.leave3()

    def conflict0(self):
        # I give the method names in the Encounter class numbers that are used to identify them in the outcome inputs.
        self.world.fight(self.enemy)


    def talk1(self):
        print(str(self.prompt))
        respIndex = 0
        for conv in self.convs:
            if conv != None:
                print(str(respIndex)+": "+str(conv))
                respIndex += 1
        say = checkInput("Say: "+"\n", list(range(0,respIndex)), "Invalid Input. Choose a number to say something: "+"\n")
        if say == 0:
            print(str(self.resp[0]))
            self.encounterCheck(self.resp[1])
        elif say == 1:
            print(str(self.resp1[0]))
            self.encounterCheck(self.resp1[1])
        elif say == 2:
            print(str(self.resp2[0]))
            self.encounterCheck(self.resp2[1])
        elif say == 3:
            print(str(self.resp3[0]))
            self.encounterCheck(self.resp3[1])
    
    def trade2(self):
        print("Buy something."+"\n")

    def leave3(self):
        print("You prepare to move on."+"\n")
        self.world.p.act()