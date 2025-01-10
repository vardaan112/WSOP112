from cmu_graphics import *
from AI1 import AI1
from AI2 import AI2
from AI3 import AI3
from AI4 import AI4
from AI5 import AI5
import random

class Player:
    def __init__(self, name, isAI, mode):
        self.hand = ()
        self.balance = 200
        self.bet = 0
        self.inHand = True
        self.playerLocation = ()
        self.name = name
        self.isAI = isAI
        self.nextMove = ''
        self.allIn = False
        if mode == 'easy':
            if isAI:
                self.AI = AI1()
            else:
                self.AI = None
        else:
            if isAI:
                x = random.randint(1, 5)
                if x == 1:
                    self.AI = AI1()
                elif x == 2:
                    self.AI = AI2()
                elif x == 3:
                    self.AI = AI3()
                elif x == 4:
                    self.AI = AI4()
                elif x == 5:
                    self.AI = AI5()
            else:
                self.AI = None

        self.playerImage = ''
        self.smallB = False
        self.smallBHolder = False
        self.bigB = False


    