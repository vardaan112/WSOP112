from AI1 import AI1
from playGame import playGame
from player import Player
from cmu_graphics import *
import math
import copy
import treys
from treys import evaluator



def onAppStart(app):
    app.winner = False
    app.loser = False
    app.homeScreen = True
    app.instructions = False
    app.load = False

    reset(app)

def reset(app):
    app.width = 1500
    app.height = 900
    app.cX = 750
    app.cY = 300
    app.rX = 500
    app.rY = 220


    app.counter = 1


    isAI = False
    app.nextMove = ''
    app.loadText = ''
    app.loadStatus = 1

    app.raiseAmount = 50
    app.raiseStep = 10
    app.maxRaise = 300

    app.cardWidth = 65
    app.cardHeight = 100
    app.dealerPosition = 0
    app.smallBlind = 10
    app.bigBlind = 20
    app.levelTime = 0

    app.backgroundImage = 'background.png' #https://stock.adobe.com/images/poker-background-suits-vector-black-grey/182899779
    app.casino = 'casino.jpg' #https://www.freepik.com/free-vector/casino-poker-game-background-black-gold-colors_6922729.htm
    app.home = 'home.png' #https://www.vectorstock.com/royalty-free-vector/golden-luxury-home-icon-vector-44618889




    app.cardImages = {}
    suits = ['h', 'd', 'c', 's']
    vals = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    #https://www.ivory.co.uk/playingcard-faces
    for suit in suits:
        for val in vals:
            card = f'{val}{suit}'
            app.cardImages[card] = (f'cards:{card}.png')

    app.cardImages['BACK'] = ('cards:BACK.png')

    app.allInStep = 1
    app.numPlayers = 8
    app.players = []
    app.playerTurn = 0
    app.playersInHand = app.numPlayers
    app.pot = 0
    app.userBet = 0
    app.userMove = None
    app.cPlayer = rgb(80,0,20)
    app.game1 = playGame(app.numPlayers)
    app.middle = []
    app.currentBet = 0
    app.paused = False
    app.gameStatus = ''
    app.playersPlayed = 0
    app.userTurn = False
    app.needsToMove = False
    app.roundStatus = False
    app.handStatus = True
    app.winHand = False
    app.winPlayer = ''
    app.callError = False
    app.checkError = False
    app.stepsPerSecond = 1.5
    app.show = False
    app.allIn = False



def createPlayers(app, difficulty):
    isAI = False
    app.nextMove = ''
    for i in range(app.numPlayers):
        if i != 1:
            isAI = True
            newPlayer = Player('AI', isAI, difficulty)
        else: 
            isAI = False
            newPlayer = Player('User', isAI, difficulty)
        app.players.append(newPlayer)

    for i in range(app.numPlayers):
        angle = i * 360/app.numPlayers
        x = app.cX + app.rX * (math.cos(math.radians(angle)))
        y = app.cY + app.rY * math.sin(math.radians(angle))
        app.players[i].playerLocation = (x, y)
        app.players[i].playerImage = f'avatar{i + 1}.png'
        #1:Freepik
        #2:https://www.freepik.com/photos/casino-slot-game-character
        #3:Adobe Stock
        #4:https://stock.adobe.com/search/images?k=poker+player
        #5:https://www.freepik.com/premium-ai-image/perfect-poker-player-striking-ad-with-singlecolored-4k-avatar-background_161690710.htm
        #6:https://www.freepik.com/premium-ai-image/alluring-ace-decentraland-darling-mesmerizing-female-poker-player-avatar-4k-sporting-st_161691670.htm
        #7:https://www.freepik.com/premium-photo/poker-player-with-black-bow-tie_75898384.htm
        #8:Adobe Stock
        


def preFlop(app):
    playerTurn = app.playerTurn % len(app.players)
    while app.players[playerTurn].inHand != True:
        app.playerTurn += 1
        playerTurn = app.playerTurn % len(app.players)
    if not(app.playerTurn >= app.playersInHand and app.roundStatus):
        playerTurn = app.playerTurn % len(app.players)
        player = app.players[playerTurn]
        if player.inHand and not player.allIn:
            if player.isAI: 
                nextPlayer(app, player)
                app.playersPlayed += 1
            else:
                app.userTurn = True
                if app.userMove == '':
                    return
                else:
                    app.playersPlayed += 1
                    app.userTurn = False
                    app.userMove = ''
    app.playerTurn += 1


    app.handStatus = True
    for player in app.players:
        if player.inHand and not player.allIn:
            if player.bet != app.currentBet:
                app.handStatus = False
                
    

    if app.playersPlayed >= app.playersInHand and app.handStatus:
        app.roundStatus = True

def flop(app):
    if app.playerTurn == 0:
            app.middle = app.game1.drawFlop()

    playerTurn = app.playerTurn % len(app.players)
    if app.playerTurn == 0:
        while app.players[playerTurn].smallBHolder != True:
            app.playerTurn += 1
            playerTurn = app.playerTurn % len(app.players)

    if not(app.playerTurn >= app.playersInHand and app.roundStatus):
        playerTurn = app.playerTurn % len(app.players)
        player = app.players[playerTurn]
        if player.inHand and not player.allIn:
            if player.isAI: 
                nextPlayer(app, player)
                app.playersPlayed += 1
            else:
                app.userTurn = True
                if app.userMove == '':
                    return
                else:
                    app.playersPlayed += 1
                    app.userTurn = False
                    app.userMove = ''
        app.playerTurn += 1

    app.handStatus = True
    for player in app.players:
        if player.inHand and not player.allIn:
            if player.bet != app.currentBet:
                app.handStatus = False
    if app.playersPlayed >= app.playersInHand and app.handStatus:
        app.roundStatus = True
    
def turn(app):
    if app.playerTurn == 0:
            app.middle = app.game1.drawTurn()
    
    playerTurn = app.playerTurn % len(app.players)
    if app.playerTurn == 0:
        while app.players[playerTurn].smallBHolder != True:
            app.playerTurn += 1
            playerTurn = app.playerTurn % len(app.players)

    if not(app.playerTurn >= app.playersInHand and app.roundStatus):
        playerTurn = app.playerTurn % len(app.players)
        player = app.players[playerTurn]
        if player.inHand and not player.allIn:
            if player.isAI: 
                nextPlayer(app, player)
                app.playersPlayed += 1
            else:
                app.userTurn = True
                if app.userMove == '':
                    return
                else:
                    app.playersPlayed += 1
                    app.userTurn = False
                    app.userMove = ''
        app.playerTurn += 1

    app.handStatus = True
    for player in app.players:
        if player.inHand and not player.allIn:
            if player.bet != app.currentBet:
                app.handStatus = False
    if app.playersPlayed >= app.playersInHand and app.handStatus:
        app.roundStatus = True

def river(app):
    if app.playerTurn == 0:
            app.middle = app.game1.drawRiver()

    playerTurn = app.playerTurn % len(app.players)
    if app.playerTurn == 0:
        while app.players[playerTurn].smallBHolder != True:
            app.playerTurn += 1
            playerTurn = app.playerTurn % len(app.players)

    if not(app.playerTurn >= app.playersInHand and app.roundStatus):
        playerTurn = app.playerTurn % len(app.players)
        player = app.players[playerTurn]
        if player.inHand and not player.allIn:
            if player.isAI: 
                nextPlayer(app, player)
                app.playersPlayed += 1
            else:
                app.userTurn = True
                if app.userMove == '':
                    return
                else:
                    app.playersPlayed += 1
                    app.userTurn = False
                    app.userMove = ''
        app.playerTurn += 1

    app.handStatus = True
    for player in app.players:
        if player.inHand and not player.allIn:
            if player.bet != app.currentBet:
                app.handStatus = False
    if app.playersPlayed >= app.playersInHand and app.handStatus:
        app.roundStatus = True

def blinds(app):
    smallP = (app.dealerPosition + 1) % app.numPlayers
    bigP = (app.dealerPosition + 2) % app.numPlayers

    
    playerSmall = app.players[smallP]
    playerSmall.smallB = True
    playerSmall.smallBHolder = True
    if playerSmall.balance >= app.smallBlind:
        playerSmall.balance -= app.smallBlind
        playerSmall.bet += app.smallBlind
    else:
        playerSmall.bet += playerSmall.balance
        playerSmall.balance = 0
        playerSmall.allIn = True

    playerBig = app.players[bigP]
    playerBig.bigB = True
    if playerBig.balance >= app.bigBlind:
        playerBig.balance -= app.bigBlind
        playerBig.bet += app.bigBlind
    else:
        playerBig.bet += playerBig.balance
        playerBig.balance = 0
        playerBig.allIn = True

    app.pot += playerSmall.bet + playerBig.bet
    app.currentBet = playerBig.bet

    return smallP, bigP

def dealerPosition(app):
    app.dealerPosition = (app.dealerPosition + 1) % app.numPlayers
    

def resetBeforeNextRound(app):
    app.playerTurn = 0
    app.playersInHand = 0
    app.userMove = ''
    app.userTurn = False
    app.roundStatus = False
    app.handStatus = True
    for player in app.players:
        player.prevMove = player.nextMove
        player.nextMove = ''
        player.bet = 0
        if player.inHand and not player.allIn:
            app.playersInHand += 1
        player.smallB = False
        player.bigB = False
    app.currentBet = 0
    app.playersPlayed = 0   

def allInState(app, gameStatus):
    if gameStatus == 'pre':
        app.middle = app.game1.drawFlop()
        app.middle = app.game1.drawTurn()
        app.middle = app.game1.drawRiver()
    elif gameStatus == 'flop':
        app.middle = app.game1.drawTurn()
        app.middle = app.game1.drawRiver()

    elif gameStatus == 'turn':
        app.middle = app.game1.drawRiver()
    allInHand(app)

def allInHand(app):
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
    bestHand = []
    bestRank = (0,)
    handsToRank = []
    for player in app.players:
        if player.inHand:
            (x,y) = player.hand
            board = [x] + [y] + app.middle
            handsToRank.append(board)
    for hand in handsToRank:
        checkRank = rankHand(hand)
        if checkRank > bestRank:
            curHand = hand[0:2]
            x = curHand[0]
            y = curHand[1]
            curHand = (x,y)
            bestHand = []
            bestHand.append(curHand)
            bestRank = checkRank
        elif checkRank == bestRank:
            curHand = hand[0:2]
            x = curHand[0]
            y = curHand[1]
            curHand = (x,y)
            bestHand.append(curHand)

    for player in app.players:
        if player.hand in bestHand:
            player.balance += app.pot/len(bestHand)
            app.winHand = True
            app.winPlayer += player.name
                    
def onStep(app):
    if app.homeScreen:
        return
    elif app.instructions:
        return
    elif app.winner:
        return
    elif app.loser:
        return
    elif app.load:
        app.counter += 1
        if app.counter >= 1 and app.counter < 3:
            app.loadText = 'Loading Poker Table...'
            app.loadStatus = 1
        elif app.counter >= 3 and app.counter < 4:
            app.loadStatus = 2
            app.loadText = 'Loading AI Entities...'
        elif app.counter >= 4 and app.counter < 6:
            app.loadStatus = 3
            app.loadText = 'Loading Avatars...'
        elif app.counter >= 6 and app.counter < 8:
            app.loadStatus = 4
            app.loadText = 'Loading Casino...'
        elif app.counter >= 8 and app.counter < 9:
            app.loadStatus = 5
            app.loadText = 'Loading Deck...'
        elif app.counter >= 9 and app.counter < 11:
            app.loadStatus = 6
            app.loadText = 'Shuffling Deck...'
        elif app.counter >= 11 and app.counter < 14:
            app.loadStatus = 7
            app.loadText = 'Table Ready!'
        elif app.counter == 14:
            app.load = False
            app.counter = 1
            app.loadStatus = 1
            

    else:
        #Checks if winner
        if len(app.players) == 1:
            app.winner = True
        app.counter += 1
        #Small blind Big blind time counter
        if app.counter % 100 == 0:
            app.smallBlind *= 2
            app.bigBlind *= 2
        app.levelTime = math.floor((100 - app.counter%100)//app.stepsPerSecond)

        
        #Checks if the remaining players in the hand are all in or if there is only one person left other than the person who is all in
        #Skips to river and showdown
        curPlayersinHand = 0
        for player in app.players:
            if player.inHand:
                curPlayersinHand += 1
                
        curPlayersAllIn = 0
        for player in app.players:
            if player.allIn:
                curPlayersAllIn += 1

            
        if ((curPlayersinHand - curPlayersAllIn == 1 or curPlayersinHand - curPlayersAllIn == 0) and app.roundStatus and curPlayersAllIn > 0):
            app.show = True
            if app.allInStep == 1:
                allInState(app, app.gameStatus)
                app.allIn = True
            print(app.allIn)
            app.allInStep += 1
            if app.allInStep == 8:
                app.gameStatus = 'post'
                app.allIn = False



        if not app.allIn:
            #Resets Deck and starts new round
            if app.gameStatus == '':
                app.game1.resetHands()
                app.game1.resetDeck()
                app.middle = []
                app.gameStatus = 'pre'
                hands = app.game1.drawRound()
                for i in range(len(hands)):
                    app.players[i].hand = hands[i]
                resetBeforeNextRound(app)
                smallP, bigP = blinds(app)
                dealerPosition(app)
                app.playerTurn = (bigP + 1) % app.numPlayers
            #Preflop
            elif app.gameStatus == 'pre':
                app.playersInHand = len(app.players)

                #Checks if round is done or not
                if  not (app.roundStatus):
                    preFlop(app)
                else: 
                    app.gameStatus = 'flop'
                    resetBeforeNextRound(app)
            #Flop
            elif app.gameStatus == 'flop':
                if not app.roundStatus:
                    flop(app)
                else: 
                    app.gameStatus = 'turn'
                    resetBeforeNextRound(app)
            #Turn
            elif app.gameStatus == 'turn':
                if not app.roundStatus:
                    turn(app)
                else: 
                    app.gameStatus = 'river'
                    resetBeforeNextRound(app) 
            #River     
            elif app.gameStatus == 'river':
                if not app.roundStatus:
                    river(app)
                else: 
                    #Show cards if at showdown
                    app.show = True
                    if app.allInStep == 1:      
                        allInHand(app)
                    elif  app.allInStep == 5:
                        app.gameStatus = 'post'
                        resetBeforeNextRound(app)
                    app.allInStep += 1
            #Resets variables and checks for any players with 0 balance as well as changes blind
            else:
                for player in app.players:
                    player.nextMove = ''
                    player.hand = ''
                    player.inHand = True
                    player.allIn = False
                    player.smallBHolder = False
                    if player.balance == 0:
                        if not player.isAI:
                            app.loser = True
                        app.players.remove(player)
                        app.numPlayers -= 1
                        for i in range(app.numPlayers):
                            angle = i * 360/app.numPlayers
                            x = app.cX + app.rX * (math.cos(math.radians(angle)))
                            y = app.cY + app.rY * math.sin(math.radians(angle))
                            app.players[i].playerLocation = (x, y)
                app.game1 = playGame(app.numPlayers)
                app.winHand = False
                app.winPlayer = ''
                app.gameStatus = ''
                app.pot = 0
                app.show = False
                app.allInStep = 1

            

        #Checks if everyone else in hand has folded
        curPlayers = 0
        for player in app.players:
            if player.inHand:
                curPlayers += 1
        if curPlayers <= 1 and curPlayersAllIn == 0:
            for player in app.players:
                if player.inHand:
                    player.balance += app.pot
                    app.winHand = True
                    app.winPlayer = player.name
            app.gameStatus = 'post' 

#Ai Move
def nextPlayer(app, player):
        playerTurn = app.playerTurn % len(app.players)
        if app.players[playerTurn].inHand and not app.players[playerTurn].allIn:
            curPlayer = app.players[playerTurn]
            curPlayers = 0
            for player in app.players:
                if player.inHand:
                    curPlayers += 1
            betRequired = app.currentBet - curPlayer.bet
            pot = app.pot
            nextMove = curPlayer.AI.nextMove(curPlayer.hand, app.middle, curPlayers, betRequired, pot)
            if nextMove == 'fold':
                curPlayer.inHand = False
                curPlayer.hand = ''
                curPlayer.nextMove = 'fold'
            elif nextMove == 'check':
                if curPlayer.bet == app.currentBet:
                    curPlayer.nextMove = 'check'
            elif nextMove == 'call':
                curPlayer.nextMove = 'call'
                difference = app.currentBet - curPlayer.bet
                if curPlayer.balance <= difference:
                    app.pot += curPlayer.balance
                    curPlayer.bet += curPlayer.balance
                    curPlayer.balance = 0
                    curPlayer.nextMove = 'All In'
                    curPlayer.allIn = True
                    if curPlayer.bet > app.currentBet:
                        app.currentBet = curPlayer.bet
                else:
                    curPlayer.balance -= difference
                    curPlayer.bet += difference
                    app.pot += difference
            else:
                raiseAm = 50
                if curPlayer.balance <= (app.currentBet + raiseAm - curPlayer.bet):
                    app.pot += curPlayer.balance
                    curPlayer.bet += curPlayer.balance
                    print(curPlayer.bet)
                    curPlayer.balance = 0
                    curPlayer.nextMove = 'All In'
                    curPlayer.allIn = True
                    if curPlayer.bet > app.currentBet:
                        app.currentBet = curPlayer.bet
                else:
                    curPlayer.nextMove = 'bet'
                    app.currentBet = curPlayer.bet + raiseAm
                    app.pot += (app.currentBet - curPlayer.bet)
                    curPlayer.balance -= (app.currentBet - curPlayer.bet)
                    curPlayer.bet += (app.currentBet - curPlayer.bet)

#User Move
def onMousePress(app, mouseX, mouseY):
        if app.homeScreen:
            if mouseY >= 260 and mouseY <= 350:
                if mouseX >= 520 and mouseX <= 720:
                    app.homeScreen = False
                    createPlayers(app, 'easy')
                    app.load = True
                    app.counter = 0
                elif mouseX >= 775 and mouseX <= 975:
                    app.homeScreen = False
                    createPlayers(app, 'Difficult')
                    app.load = True
                    app.counter = 0
            elif mouseY >= 385 and mouseY <= 475:
                if mouseX >= 650 and mouseX <= 850:
                    app.homeScreen = False
                    app.instructions = True
        elif app.instructions:
            if mouseX >= 1300 and mouseX <= app.width and mouseY >= 650 and mouseY <= app.height:
                app.instructions = False
                app.homeScreen = True
        elif app.winner or app.loser:
            if mouseX >= 1300 and mouseX <= app.width and mouseY >= 650 and mouseY <= app.height:
                app.winner = False
                app.loser = False
                app.homeScreen = True
                reset(app)
        else:
            if app.userTurn:
                playerTurn = app.playerTurn % len(app.players)
                curPlayer = app.players[playerTurn]
                app.maxRaise = curPlayer.balance
                '''app.raiseAmount = 30
                if app.raiseAmount < curPlayer.balance:
                    app.raiseAmount = curPlayer.balance'''
                if mouseY > 650 and mouseY < 750:
                    if mouseX > 200 and mouseX < 400:
                        if curPlayer.bet == app.currentBet:
                            curPlayer.nextMove = 'check'
                            app.userMove = 'move'
                            if app.callError:
                                app.callError = False
                        else:
                            app.checkError = True
                    elif mouseX > 500 and mouseX < 700:
                        if app.checkError:
                            app.checkError = False
                        if app.callError:
                            app.callError = False
                        curPlayer.inHand = False
                        curPlayer.hand = ''
                        curPlayer.nextMove = 'fold'
                        app.userTurn = False
                        app.userMove = ''
                        app.playersPlayed += 1
                    elif mouseX > 800 and mouseX < 1000:
                        if app.checkError:
                            app.checkError = False
                        if curPlayer.bet != app.currentBet:
                            curPlayer.nextMove = 'call'
                            difference = app.currentBet - curPlayer.bet
                            if curPlayer.balance <= difference:
                                app.pot += curPlayer.balance
                                curPlayer.bet += curPlayer.balance
                                curPlayer.balance = 0
                                curPlayer.nextMove = 'All In'
                                curPlayer.allIn = True
                                app.playersPlayed += 1
                            else:
                                curPlayer.balance -= difference
                                curPlayer.bet += difference
                                app.pot += difference
                            app.userMove = 'move'
                        else:
                            app.callError = True
                    elif mouseX > 1100 and mouseX < 1300:
                        if app.checkError:
                            app.checkError = False
                        if app.callError:
                            app.callError = False
                        if curPlayer.balance <= (app.currentBet + app.raiseAmount - curPlayer.bet):
                            app.pot += curPlayer.balance
                            curPlayer.bet += curPlayer.balance
                            curPlayer.balance = 0
                            curPlayer.nextMove = 'All In'
                            app.currentBet = curPlayer.bet
                            curPlayer.allIn = True
                            app.playersPlayed += 1
                            
                            
                        else:
                            curPlayer.nextMove = 'bet'
                            app.currentBet = app.currentBet + app.raiseAmount
                            app.pot += (app.currentBet - curPlayer.bet)
                            curPlayer.balance -= (app.currentBet - curPlayer.bet)
                            curPlayer.bet += (app.currentBet - curPlayer.bet)
                        app.userMove = 'move'
                elif mouseY > 780 and mouseY < 790 and mouseX > 1050 and mouseX < 1350:
                    positionInSlider = (mouseX - 1025) / 300
                    app.raiseAmount = math.floor(positionInSlider * app.maxRaise)
                    if app.raiseAmount > 500:
                        app.raiseAmount = 500
                    if app.raiseAmount >= (curPlayer.balance - curPlayer.bet):
                        app.raiseAmount = curPlayer.balance - curPlayer.bet
                        
                    

def redrawAll(app):

    if app.homeScreen:
        color = rgb(255, 215, 0)
        drawImage(app.casino, 0, 0, width = app.width, height = app.height)
        drawLabel('WSOP 112', 750, 200, size = 60, fill = 'Gold')
        drawRect(520, 260, 200, 90, border = color, borderWidth = 3)
        drawLabel('Easy Mode', 620, 305, size=25, fill='White')
        drawRect(775, 260, 200, 90, border = color, borderWidth = 3)
        drawLabel('Hard Mode', 875, 305, size=25, fill='White')
        drawRect(650, 385, 200, 90, border = color, borderWidth = 3)
        drawLabel('Instructions', 750, 430, size=25, fill='White')
        
    elif app.winner:
        color2 = rgb(25, 25, 25)
        color1 = rgb(65,65,65)
        drawRect(0,0, app.width, app.height, fill = gradient(color1, color2, start='center'))
        drawImage(app.backgroundImage, 0, 0, width = app.width, height = app.height)
        color2 = rgb(12, 135, 41)
        color1 = rgb(48, 175, 77)
        drawOval(app.cX, app.cY, app.rX * 2, app.rY * 2, fill = gradient(color1, color2, start='center'))
        drawOval(app.cX, app.cY, app.rX * 2, app.rY * 2, fill= None, border="gold")
        drawLabel("WSOP WINNER!!!", app.cX, app.cY, size = 45, fill = 'white')
        drawImage(app.home, 1300, 650, width = 200, height = 200)
    elif app.loser:
        color2 = rgb(25, 25, 25)
        color1 = rgb(65,65,65)
        drawRect(0,0, app.width, app.height, fill = gradient(color1, color2, start='center'))
        drawImage(app.backgroundImage, 0, 0, width = app.width, height = app.height)
        color2 = rgb(12, 135, 41)
        color1 = rgb(48, 175, 77)
        drawOval(app.cX, app.cY, app.rX * 2, app.rY * 2, fill = gradient(color1, color2, start='center'))
        drawOval(app.cX, app.cY, app.rX * 2, app.rY * 2, fill= None, border="gold")
        drawLabel("Unlucky you lost to AI coded by a 112 student, Try Again.", app.cX, app.cY, size = 30, fill = 'Red')
        drawImage(app.home, 1300, 650, width = 200, height = 200)


    elif app.instructions:
        drawImage(app.casino, 0, 0 , width = app.width, height = app.height)
        drawLabel('Poker Instructions', 750, 100, size = 60, bold = True, fill = 'Gold')
        drawRect(400, 150, 700, 600, border = rgb(255, 215, 0))
        instructions = (
        "1. Each player is dealt two cards. Blinds start at 10, 20, and are to the left of the player.\n"
        "2. A round of betting begins, starting with the player to the left of the dealer.\n"
        "3. The dealer places three community cards face up on the table.\n"
        "4. Another round of betting occurs.\n"
        "5. A fourth community card is placed, followed by another betting round.\n"
        "6. The fifth and final community card is placed\n"
        "7. Players reveal their hands, and the best five-card hand wins.\n"
        "8. Winning hands are ranked High Card to Royal Flush.\n"
        "9. The objective of the game is to be the last one remaining.\n"
        "10. If at any point the user has no remaining balance, the game has been lost."
        )
        
        startY = 180
        for line in instructions.splitlines():
            drawLabel(line, 410, startY, size=18, fill='White', align='left')
            startY += 60
        drawImage(app.home, 1300, 650, width = 200, height = 200)
    elif app.load:
        drawImage(app.casino, 0, 0 , width = app.width, height = app.height)
        drawLabel(app.loadText, 750, 200, size = 30, fill = 'Gold')
        drawRect(550, 300, 400, 80, border = 'White' , borderWidth = 3)
        if app.loadStatus == 1:
            return
        elif app.loadStatus == 2:
            drawRect(550, 300, 66, 80, fill = 'White')
        elif app.loadStatus == 3:
            drawRect(550, 300, 132, 80, fill = 'White')
        elif app.loadStatus == 4:
            drawRect(550, 300, 198, 80, fill = 'White')
        elif app.loadStatus == 5:
            drawRect(550, 300, 264, 80, fill = 'White')
        elif app.loadStatus == 6:
            drawRect(550, 300, 340, 80, fill = 'White')
        elif app.loadStatus == 7:
            drawRect(550, 300, 400, 80, fill = 'White')
        print(app.loadStatus)




    else:
        color2 = rgb(25, 25, 25)
        color1 = rgb(65,65,65)
        drawRect(0,0, app.width, app.height, fill = gradient(color1, color2, start='center'))
        drawImage(app.backgroundImage, 0, 0, width = app.width, height = app.height)
        color2 = rgb(12, 135, 41)
        color1 = rgb(48, 175, 77)
        drawOval(app.cX, app.cY, app.rX * 2, app.rY * 2, fill = gradient(color1, color2, start='center'))
        drawOval(app.cX, app.cY, app.rX * 2, app.rY * 2, fill= None, border="gold")

        
        startX = app.cX - (5 * 120)/2.5
        startY = app.cY 
        for i in range(len(app.middle)):
            x = startX + i * 120 + 5 * i
            y = startY
            drawCard(app, app.middle[i], x, y)
        

        drawLabel(f'Blinds: ({app.smallBlind}, {app.bigBlind}), Increase in {app.levelTime}', 200, 800, size = 23, fill = 'Gold')
        

        '''for card in range(len(app.middle)):
            drawLabel(str(app.middle[card]), app.cX - 150 + card * 75, app.cY, size = 25, fill = 'red')'''
        drawLabel(f'Pot: {app.pot}        CurBet: {app.currentBet}'  , app.width/2, app.cY - 80, size = 20)

    
        if app.winHand:
            drawLabel(f'{app.winPlayer} won the hand', app.width/2, app.cY + 80, fill = 'red', size = 25)

        selectedUser = app.playerTurn % app.numPlayers
        for player in range(len(app.players)):
            (x, y) = app.players[player].playerLocation
            if player == app.dealerPosition - 1:
                color = 'Gold'
                drawLabel('Dealer', x + 30, y - 45, size = 25, fill = color)
            '''drawLabel(app.players[player].hand, x - 12, y-12, size = 16, fill = 'red')'''
            '''drawLabel(app.players[player].name, x - 40, y - 40, size = 22, fill = 'red')'''
            if player == selectedUser:
                chipsToCall = app.currentBet - app.players[player].bet
                if chipsToCall > 0:
                    drawLabel(f'{chipsToCall} to Call', app.width/2, app.cY + 120, size = 30, fill = 'blue')

            if app.players[player].allIn:
                drawLabel('All In', x - 60, y - 44, size = 22, fill = 'red')
            elif app.players[player].nextMove != '':
                drawLabel(app.players[player].nextMove.upper(), x - 60, y - 44, size = 22, fill = 'red')
            elif not  app.players[player].inHand and selectedUser == player and app.playerTurn != 0:
                drawLabel('FOLDED', x, y - 30, size = 22, fill = 'Red')
                
            cardAngle = 0
            if app.players[player].isAI and app.players[player].inHand:
                if app.show and app.players[player].hand != () and type(app.players[player].hand) == tuple:
                    (c1, c2) = app.players[player].hand
                    drawCard(app, c1, x - 25, y, hidden=False, angle = cardAngle, width = 45, height = 67.5)
                    drawCard(app, c2, x + 25, y, hidden=False, angle = cardAngle, width = 45, height = 67.5)
                else:
                    drawCard(app, 'BACK', x - 20, y, hidden=True, angle = cardAngle, width = 30, height = 46.2)
                    drawCard(app, 'BACK', x + 20, y, hidden=True, angle = cardAngle, width = 30, height = 46.2)
            else:
                if app.players[player].hand != () and type(app.players[player].hand) == tuple and app.players[player].inHand:
                    (c1, c2) = app.players[player].hand
                    drawCard(app, c1, x - 25, y, hidden=False, angle = cardAngle, width = 45, height = 67.5)
                    drawCard(app, c2, x + 25, y, hidden=False, angle = cardAngle, width = 45, height = 67.5)
            if selectedUser == player and app.players[player].inHand:
                drawPlayerCard(app, app.players[player], x, y, color = 'Yellow')
                drawCircle(x, y, 8, fill = 'Yellow')
            else:
                drawPlayerCard(app, app.players[player], x, y, color = 'Red')
                drawCircle(x, y, 8, fill = app.cPlayer)


        y = 650
        width = 200
        height = 100

        color1 = rgb(99,0,0)
        color2 = rgb(180,0,0)
        
        if not app.players[selectedUser].isAI:
            color1 = gradient(color2, color1)
            drawRect(200, y, width, height, fill= color1, border="black", borderWidth=2)
            drawLabel("Check", 200 + width / 2, y + height / 2, size=20, fill="white")
            drawRect(500, y, width, height, fill= color1, border="black", borderWidth=2)
            drawLabel("Fold", 500 + width / 2, y + height / 2, size=20, fill="white")
            drawRect(800, y, width, height, fill= color1, border="black", borderWidth=2)
            drawLabel("Call", 800 + width / 2, y + height / 2, size=20, fill="white")
            drawRect(1100, y, width, height, fill= color1, border="black", borderWidth=2)
            drawLabel("Raise", 1100 + width / 2, y + height / 2, size=20, fill="white")
            drawRect(1050, 780, 300, 10, fill='white')  
            drawCircle(1025 + (app.raiseAmount / app.maxRaise) * 300, 785, 8, fill='gold')  
            drawLabel(f'Raise Amount: ${app.raiseAmount}', 1200, 810, size=20, fill='white')
        else:
            drawRect(200, y, width, height, fill= color1, border="black", borderWidth=2)
            drawLabel("Check", 200 + width / 2, y + height / 2, size=20, fill="white")
            drawRect(500, y, width, height, fill= color1, border="black", borderWidth=2)
            drawLabel("Fold", 500 + width / 2, y + height / 2, size=20, fill="white")
            drawRect(800, y, width, height, fill= color1, border="black", borderWidth=2)
            drawLabel("Call", 800 + width / 2, y + height / 2, size=20, fill="white")
            drawRect(1100, y, width, height, fill= color1, border="black", borderWidth=2)
            drawLabel("Raise", 1100 + width / 2, y + height / 2, size=20, fill="white")

        if app.userTurn:
            drawLabel("User's Turn to Play!!!", app.width/2, app.height - 30, size = 28, fill = 'white')
        if app.callError:
            drawLabel("You must either Check, Raise, or Fold!", 200, 25, size = 25, fill = 'red')
        if app.checkError:
            drawLabel("You must either Call, Raise, or Fold!", 200, 25, size = 25, fill = 'red')

def drawCard(app, card, x, y, hidden = False, angle = 0, width = 65, height = 100):
    if hidden:
        cardImage = app.cardImages.get('BACK', None)
    else:
        cardImage = app.cardImages.get(card, None)

    drawImage(cardImage, x, y, align = 'center', width = width, height = height, rotateAngle = angle)
    if cardImage is None:
        raise ValueError(f"CARD NOT FOUND")
    
def drawPlayerCard(app, player, x, y, color = 'Red'):
    '''drawRect(x + 20, y + 20, 60, 90, fill = 'darkGreen', border = 'gold', borderWidth = 2)
    if not player.isAI:
        drawRect(x + 20, y + 20 , 60, 90, fill = 'darkGreen', border = 'red', borderWidth = 2)'''
    drawImage(player.playerImage, x + 50, y + 50, align = 'center', width = 50, height = 50)
    drawLabel(f'{player.name} BAL: ${player.balance}', x + 50, y + 90, size = 15, fill = color)
    color = rgb(130, 1, 184)
    color = 'White'
    if player.inHand and player.smallB:
            drawLabel(f'Small Blind: ${app.smallBlind}', x + 34, y - 44, size = 15, fill = color, bold = True)
    if player.inHand and player.bigB:
            drawLabel(f'Big Blind: ${app.bigBlind}', x + 34, y - 44, size = 15, fill = color, bold = True)
      

def main():
    runApp()

main()