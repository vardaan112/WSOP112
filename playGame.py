from cmu_graphics import *
import random
import math

class playGame:
    def __init__(self, noPlayers):
        self.noPlayers = noPlayers
        self.round = []
        self.cards = [str(i) for i in range(2,10)]
        self.cards += ['T', 'J', 'Q', 'K', 'A']
        self.suits = ['c','d','h','s']
        self.resetDeck()
        
        self.cardsInMiddle = []
        self.playerStatus = [True for i in range(noPlayers)]
    
    def resetDeck(self):
        self.deck = []
        for suit in self.suits:
            for num in self.cards:
                self.deck.append(num + suit)
        random.shuffle(self.deck)

    def resetHands(self):
        self.round = [[] for player in range(self.noPlayers)]
        self.cardsInMiddle = []

    def drawCard(self):
        card = self.deck[0]
        self.deck = self.deck[1:]
        return card
    
    def drawRound(self):
        self.round = []
        for player in range(self.noPlayers):
            playerHand = self.drawHand()
            self.round += [playerHand]
        return self.round
    
    def drawHand(self):
        card1 = self.drawCard()
        card2 = self.drawCard()
        return (card1, card2)
    
    def drawFlop(self):
        card1 = self.drawCard()
        card2 = self.drawCard()
        card3 = self.drawCard()
        self.cardsInMiddle.append(card1)
        self.cardsInMiddle.append(card2)
        self.cardsInMiddle.append(card3)
        return self.cardsInMiddle
    
    def drawTurn(self):
        card = self.drawCard()
        self.cardsInMiddle.append(card)
        return self.cardsInMiddle

    def drawRiver(self):
        card = self.drawCard()
        self.cardsInMiddle.append(card)
        return self.cardsInMiddle

    
    
    


    
        