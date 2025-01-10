from cmu_graphics import *
import copy
import random

#Crazy AI with low simulations
class AI3:
    def __init__(self): 
        self.name = 'the by the book AI'
        self.cards = [str(i) for i in range(2,10)]
        self.cards += ['T', 'J', 'Q', 'K', 'A']
        self.suits = ['c','d','h','s']

        self.deck = []
        for suit in self.suits:
            for num in self.cards:
                self.deck.append(num + suit)

   
   
    def checkOpponentWin(self, opponentHand, AIHand, centerCards):

    #RANKS HighCard = 0, Pair = 1, Two Pair = 2, ThreeOfAKind = 3, Straight = 4, Flush = 5, Full House = 6, Quads = 7, Straight Flush = 8
        
        def rankHand(hand):
            values = '23456789TJQKA'
            suits = 'cdhs'

            suits = []
            for card in hand:
                suits.append(card[1])
            
            #FLUSH
            flush = False
            flushS = ''
            for suit in ('s','d','h','c'):
                if suits.count(suit) >= 5:
                    flush = True
                    flushS = suit
            flushNumbers = []
            if flush:
                for card in hand:
                    if card[1] == flushS:
                        flushNumbers.append(card[0])
            
            #STRAIGHT
            valueToNo = dict()
            index = 2
            for val in values:
                valueToNo[val] = index
                index += 1
            
            newFlushNumbers = []
            for numbers in flushNumbers:
                for key in valueToNo:
                    if numbers == key:
                        flushNumbers.remove(numbers)
                        newFlushNumbers.append(valueToNo[key])
            flushNumbers = newFlushNumbers
            
            cardsToNo = []
            for card in hand:
                for key in valueToNo:
                    if key == card[0]:
                        cardsToNo.append(valueToNo[key])


            straight = False
            straightHighCard = None
            cardsSorted = sorted(set(cardsToNo))
            for i in range(len(cardsSorted) - 4):
                if cardsSorted[i + 4] - cardsSorted[i] == 4:
                    straight = True
                    straightHighCard = cardsSorted[i + 4]
                    break
            else:
                if [2,3,4,5,14] in cardsSorted:
                    straight = True
                    straightHighCard = 5

            #STRAIGHT FLUSH
            if flush and straight:
                flushNumbers = sorted(flushNumbers, reverse = True)
                for i in range(len(flushNumbers) - 4):
                    if flushNumbers[i] - flushNumbers[i + 4] == 4:
                        return (8, flushNumbers[i])
                if [14,1,2,3,4] in flushNumbers:
                    return (8, 5)
            
            numbers = []
            for card in hand:
                for key in valueToNo:
                    if key == card[0]:
                        numbers.append(valueToNo[key])
            numberCount = dict()
            for number in numbers:
                numberCount[number] = numberCount.get(number, 0) + 1
            numbers = sorted(numbers)
            
            pairs = []
            pair = False
            for key in numberCount:
                if numberCount[key] == 2:
                    pairs.append(key)
                    pair = True
            
            trips = []
            trip = False
            for key in numberCount:
                if numberCount[key] == 3:
                    trips.append(key)
                    trip = True
            
            quads = []
            quad = False
            for key in numberCount:
                if numberCount[key] == 4:
                    quads.append(key)
                    quad = True

            numberQ = set(numbers)

            if quad:
                if max(numberQ) == quads[0]:
                    numberQ.remove(quads[0])
                return (7, quads[0], max(numberQ))
            elif trip and pair:
                return (6, trips[0], pairs[0])
            elif flush:
                return (5, flushNumbers)
            elif straight:
                return (4, straightHighCard)
            elif trip:
                if max(numberQ) == trips[0]:
                    numberQ.remove(trips[0])
                max1 = max(numberQ)
                numberQ.remove(max1)
                if max(numberQ) == trips[0]:
                    numberQ.remove(trips[0])
                max2 = max(numberQ)
                return (3, trips[0], max1, max2)
            elif len(pairs) >= 2:
                top2Pairs = sorted(pairs, reverse = True)

                top2Pairs = top2Pairs[:2]
                return(2, top2Pairs,  sorted(numbers, reverse = True))
            elif len(pairs) == 1:
                return(1, pairs[0],  sorted(numbers, reverse = True))
            else:
                return (0, sorted(numbers, reverse = True))
        (x, y) = opponentHand
        opponentBestHandCalc = [x] + [y] + centerCards
        (x, y) = AIHand
        AIBestHandCalc = [x] + [y] + centerCards
        return rankHand(opponentBestHandCalc) >= rankHand(AIBestHandCalc)

            
            
    
    def simulation(self, player, centerCards, numOpponents, monteCarloRuns = 30):
        wins = 0
        deck = copy.copy(self.deck)
        (x, y) = player
        cardsPlayed = [x] + [y] + centerCards
        for card in cardsPlayed:
            deck.remove(card)
        
        for i in range(monteCarloRuns):
            random.shuffle(deck)
            newDeck = copy.copy(deck)
            fullCenterCards = copy.copy(centerCards)
            for cardDraw in range (5 - len(centerCards)):
                cardDrawn = newDeck[0]
                fullCenterCards.append(cardDrawn)
                newDeck = newDeck[1:]
            opponentCards = []
            for opponent in range(numOpponents):
                opponentCard1 = newDeck[0]
                newDeck = newDeck[1:]
                opponentCard2 = newDeck[0]
                newDeck = newDeck[1:]
                opponentCards.append((opponentCard1,opponentCard2))
            losses = 0
            for opponent in opponentCards:
                if self.checkOpponentWin(opponent, player, fullCenterCards):
                    losses += 1
            if losses == 0:
                wins += 1
        return wins/(monteCarloRuns)
    
    def nextMove(self, player, centerCards, numOpponents, betRequired, pot):
        probability = self.simulation(player, centerCards, numOpponents)
        if betRequired == 0: 
            if probability > 0.6:
                return  'raise 2x'
            else:
                return 'check'
        else:
            if probability > 0.7:
                return 'raise 2x'
            elif betRequired/pot <= probability:
                return 'call'
            else:
                return 'fold'

                


        
        
        
        
        
