import pygame
from PokerAI import Simulator
from Bot import Bot
import time
import random
import copy




pygame.init()

#######################         INSTANCE VARIABLES          ##################

###         INSTANCES                   ###
bot = Bot(1000)     #make a bot


###         CONSTANTS                   ###

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
REDHOVER = (100,0,0)
GREEN = (0,100,0)
GREY = (105,105,105)
display_width = 800
display_height = 600
FPS = 60
BASISINZET = 30
BTNBACKGROUND = pygame.image.load("img/ButtonBackground.jpg")
BTNHHOVER = pygame.image.load("img/ButtonBackgroundHover.jpg")
BTNCLICKED = pygame.image.load("img/ButtonBackgroundClicked.jpg")


###         SCREEN SETTINGS             ###
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Headsup Poker")

clock = pygame.time.Clock()
# Font for text in the game
font = pygame.font.SysFont("Sans",25)


###         CARDS                       ###
tableCards = {}
playerHand = {}
#hand of bot is kept in bot itself
cards = {
    1: 'CA', 2: 'DA', 3: 'HA', 4: 'SA',
    5: 'C2', 6: 'D2', 7: 'H2', 8: 'S2',
    9: 'C3', 10: 'D3', 11: 'H3', 12: 'S3',
    13: 'C4', 14: 'D4', 15: 'H4', 16: 'S4',
    17: 'C5', 18: 'D5', 19: 'H5', 20: 'S5',
    21: 'C6', 22: 'D6', 23: 'H6', 24: 'S6',
    25: 'C7', 26: 'D7', 27: 'H7', 28: 'S7',
    29: 'C8', 30: 'D8', 31: 'H8', 32: 'S8',
    33: 'C9', 34: 'D9', 35: 'H9', 36: 'S9',
    37: 'CT', 38: 'DT', 39: 'HT', 40: 'ST',
    41: 'CJ', 42: 'DJ', 43: 'HJ', 44: 'SJ',
    45: 'CQ', 46: 'DQ', 47: 'HQ', 48: 'SQ',
    49: 'CK', 50: 'DK', 51: 'HK', 52: 'SK'}
cards1 = copy.deepcopy(cards)
turnCard = "XX"
riverCard = "XX"


###         MONEY RELATED VARIABLES     ###
totalPlayer = 1000
betPlayer = 0# the amount of money the player is betting at the current time
betBot = 0  # the amount of money the bot is betting at the current time
pot = 0  # the amount of money in the pot


###         CHECKING VALUES/BOOLEANS                   ###
startgamedraw = 0
optionsreset = 0
setbackground = 0
whoFolded = 0           # 0 voor niemand heeft gefold, 1 voor bot heeft gefold, 2 voor player heeft gefold
ingezet = 0             #
played = 0              #
raised = 0              #
endgameReset =0         #Round resets
riverReset = 0          #
turnReset = 0           #
dealingReset = 0        #
flopReset = 0           #
botHasmove =0           #has the bot calculated a move yet?
cardsDealt = 0          #have the cards been dealt?
calculatewinner = 0     #has the winner been calculated

roundstartmessage = True
priority = -1           #who needs to put in defaultBet and who begins every round
beurt  = priority       #necessary for determining who's turn it is
defaultBetSet = 0       #defaultbet is set

#Different gamestates
Options = False
gameStart = False
gameExit = False
gameOver = False
gameEndScreen = False
dealing = False
flop = False
turn = False
river = False
clicked = False
waitingForPlayer = False
botmovecalculated = False


###         MOVES                       ###
playerMove = ""
botMove = ""
#move of bot is kept in bot itself


###         OTHER                       ###
round = 0
prevcards = []

def nextRound(Whichround):
    global flop
    global turn
    global river
    global gameEndScreen
    global gameStart
    global dealing
    global raised
    global played
    global ingezet
    global round

    if Whichround == "Dealing":                     #bij de eerste ronde moet er maar 1 iemand inzetten als er niet geraised wordt
        flop = True
        proceedGame()
        ingezet = 1
    elif played == 1:                               #bij alle andere rondes moet de ander sowieso eerst aan de beurt komen, of er nu geraised werd of niet
        if Whichround == "Flop":
            turn = True
            ingezet = 1
            proceedGame()
        elif Whichround == "Turn":
            river = True
            ingezet = 1
            proceedGame()
        elif Whichround == "River":
            gameEndScreen = True
            gameStart = False
            dealing = False
            flop = False
            turn = False
            river = False
            ingezet = 1

    print("volgende ronde: "+str(round)+ "  played?: "+str(played) + "  ingezet?: "+ str(ingezet) + "  raised?: "+ str(raised))

def inzetronde(NRound):
    global waitingForPlayer
    global betBot
    global betPlayer
    global gameEndScreen
    global gameStart
    global dealing
    global flop
    global turn
    global river
    global priority
    global whoFolded
    global raised
    global played
    global gameExit
    global ingezet
    global beurt
    global optionsreset

    while (ingezet == 0):
        if played == 1:
            if raised == 0:
                print("aan de beurt:")
                beurt = beurt * -1

                if (beurt == -1):
                    waitingForPlayer = True
                    print("speler, kiest:")
                    while (waitingForPlayer):

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameExit = True
                                gameStart = False
                                dealing = False
                                flop = False
                                turn = False
                                river = False
                                waitingForPlayer = False
                                ingezet = 1
                                raised = 0
                        set_clickable_button("Raise", 150, 420, 125, 38, 20, "Raise", NRound)
                        set_clickable_button("Call/Check", 150, 480, 125, 38, 20, "Call/Check", NRound)
                        set_clickable_button("Fold", 150, 540, 125, 38, 20, "Fold", NRound)

                else:
                    print("bot, kiest:")
                    if bot.move == "Fold":
                        gameEndScreen = True
                        gameStart = False
                        dealing = False
                        flop = False
                        turn = False
                        river = False
                        print("Fold")
                        raised = 0
                        whoFolded = 1
                        ingezet = 1
                    elif bot.move == "Call/Check":
                        betBot = betPlayer
                        print("Call/Check")
                        nextRound(NRound)

                    elif bot.move == "Raise":
                        betBot = betPlayer + BASISINZET
                        raised = 1
                        print("Raise")
                        show_inactive_buttons()
                        pygame.display.update()
            while raised == 1:
                print("aan de beurt:")
                beurt = beurt * -1

                if (beurt == -1):
                    waitingForPlayer = True
                    print("speler, kiest:")
                    while (waitingForPlayer):
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                gameExit = True
                                gameStart = False
                                dealing = False
                                flop = False
                                turn = False
                                river = False
                                waitingForPlayer = False
                                ingezet = 1
                                raised = 0
                        set_clickable_button("Raise", 150, 420, 125, 38, 20, "Raise", NRound)
                        set_clickable_button("Call/Check", 150, 480, 125, 38, 20, "Call/Check", NRound)
                        set_clickable_button("Fold", 150, 540, 125, 38, 20, "Fold", NRound)
                else:
                    print("bot, kiest:")
                    if bot.move == "Fold":
                        gameEndScreen = True
                        gameStart = False
                        dealing = False
                        flop = False
                        turn = False
                        river = False
                        print("Fold")
                        raised = 0
                        whoFolded = 1
                        ingezet = 1
                    elif bot.move == "Call/Check":
                        betBot = betPlayer
                        print("Call/Check")
                        nextRound(NRound)
                        raised = 0

                    elif bot.move == "Raise":
                        betBot = betPlayer + BASISINZET
                        raised = 1
                        print("Raise")
                        show_inactive_buttons()
                        pygame.display.update()

        else:
            if (priority == -1):
                waitingForPlayer = True
                print("eerste zet "+ NRound + " ronde, Player kiest:")
                while (waitingForPlayer):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameExit = True
                            gameStart = False
                            dealing = False
                            flop = False
                            turn = False
                            river = False
                            ingezet = 1
                            raised = 0
                            waitingForPlayer = False
                    set_clickable_button("Raise", 150, 420, 125, 38, 20, "Raise", NRound)
                    set_clickable_button("Call/Check", 150, 480, 125, 38, 20, "Call/Check", NRound)
                    set_clickable_button("Fold", 150, 540, 125, 38, 20, "Fold", NRound)

            else:
                print("eerste zet "+ NRound + " ronde:, bot kiest:")
                if bot.move == "Fold":
                    gameEndScreen = True
                    ingezet = 1
                    gameStart = False
                    dealing = False
                    flop = False
                    turn = False
                    river = False
                    raised = 0
                    print("Fold")
                    whoFolded = 1
                elif bot.move == "Call/Check":
                    betBot = betPlayer
                    raised = 0
                    print("Check")
                    nextRound(NRound)
                    played = 1

                elif bot.move == "Raise":
                    betBot = betPlayer + BASISINZET
                    raised = 1
                    played = 1
                    print("Raise")
                    show_inactive_buttons()
                    pygame.display.update()
    show_inactive_buttons()
    pygame.display.update()



def chooseRandomCard():
    index = random.randint(1,52)
    while index in prevcards:
        index = random.randint(1, 52)
    prevcards.append(index)
    return index


def dealCards():
    for i in range(2):
        rand1 = chooseRandomCard()
        rand2 = chooseRandomCard()
        playerHand.update({rand1: cards.get(rand1)})
        print("PLAYERHAND APPENDED: " + str({rand1: cards.get(rand1)}) )
        bot.hand.update({rand2: cards.get(rand2)})


def check_for_defaultBet():
    global totalPlayer
    global betPlayer
    global betBot
    print("defaultbet"+ str(priority))
    if priority == 1:
        betPlayer += BASISINZET
    else:
        betBot += BASISINZET
        print("betBot = "+str(betBot))


def proceedGame():
    global cards1
    global round
    global turnCard
    global riverCard
    if round == 0:                       #Flop:  3 new random cards on the table
        for i in range(3):
            randcard = chooseRandomCard()
            tableCards.update({randcard: cards.get(randcard)})
            print("Proceedgame is called, added card "+ str(i) +" to tablecards: " + str({randcard: cards.get(randcard)}))
        round = 1
    elif round == 1:                     #Turn: 1 new random card on the table
        randcard = chooseRandomCard()
        tableCards.update({randcard: cards.get(randcard)})
        turnCard = str(cards.get(randcard))
        print("Proceedgame is called, added Turncard to tablecards: " + str(turnCard))
        round = 2
    elif round == 2:                     #River: 1 new random card on the table
        randcard = chooseRandomCard()
        tableCards.update({randcard: cards.get(randcard)})
        riverCard = str(cards.get(randcard))
        print("Proceedgame is called, added Rivercard to tablecards: " + str(riverCard))
        round = 3


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h,fsize, incol,img = "None",trigger = None):         #message (text), x-co, y-co, width, height, inactive color, active color


    if img != "None":
        smallText = pygame.font.Font("impact.ttf", fsize)
        pygame.draw.rect(gameDisplay, BLACK, (x,y,w,h))
        btnImg = pygame.image.load(img)
        btnImg = pygame.transform.scale(btnImg,((w -int(fsize/4)),( h - int(fsize/4))))
        btnsurf, textbtn = text_objects(msg,smallText)
        textbtn.center= ((x + (w / 2)), (y + (h / 2)))
        gameDisplay.blit(btnImg, (x + int(fsize/8), y +int(fsize/8)))
        gameDisplay.blit(btnsurf,textbtn)


def set_clickable_button(msg, x, y, w, h, fsize, action, NRound):
    global raised
    global played
    global gameEndScreen
    global gameStart
    global dealing
    global flop
    global turn
    global river
    global ingezet
    global waitingForPlayer
    global whoFolded
    global betPlayer
    global betBot
    global gameExit
    global gameOver
    global setbackground
    global startgamedraw
    global cardsDealt
    global tableCards
    global Options
    global optionsreset

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(gameDisplay, BLACK, (x, y, w, h))
    smallText = pygame.font.Font("impact.ttf", fsize)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        btnImg = pygame.transform.scale(BTNHHOVER, (w -int(fsize/4), h - int(fsize/4)))
        btnsurf, textbtn = text_objects(msg, smallText)
        textbtn.center = ((x + (w / 2)), (y + (h / 2)))
        gameDisplay.blit(btnImg, (x + int(fsize/8), y + int(fsize/8)))
        gameDisplay.blit(btnsurf, textbtn)
        if click[0] == 1:
            if action == "Fold":
                gameEndScreen = True
                gameStart = False
                dealing = False
                flop = False
                turn = False
                river = False
                ingezet = 1
                waitingForPlayer = False
                print("Fold")
                whoFolded = 2
                raised = 0
            elif action == "Call/Check":
                if played == 1:
                    betPlayer = betBot
                    raised = 0
                    waitingForPlayer = False
                    print("Call/Check")
                    nextRound(NRound)
                else:
                    betPlayer = betBot
                    raised = 0
                    waitingForPlayer = False
                    print("Check")
                    nextRound(NRound)
                    played = 1
            elif action == "Raise":
                if played == 1:
                    betPlayer = betBot + BASISINZET
                    waitingForPlayer = False
                    raised = 1
                    print("Raise wel al played")
                    show_inactive_buttons()
                    pygame.display.update()
                else:
                    betPlayer = betBot + BASISINZET
                    waitingForPlayer = False
                    raised = 1
                    print("Raise nog niet played")
                    played = 1
                    show_inactive_buttons()
                    pygame.display.update()
            elif action == "Start":
                gameStart = True
                gameExit = False

            elif action == "Quit":
                gameExit = True
                gameStart = False
                dealing = False
                flop = False
                turn = False
                river = False
            elif action == "Dealing":
                dealing = True
            elif action =="Continue":
                gameStart = False
                gameEndScreen= False
                optionsreset = 0
                Options = False
                setbackground = 0
                startgamedraw = 0

                cardsDealt = 0
                tableCards = {}
            elif action == "Options":
                Options = True
            elif action == "Diff10":
                bot.set_diff(0.1)
                showDiff()
            elif action == "Diff15":
                bot.set_diff(0.15)
                showDiff()
            elif action == "Diff20":
                bot.set_diff(0.2)
                showDiff()





    else:
        btnImg = pygame.transform.scale(BTNBACKGROUND, (w - int(fsize/4), h - int(fsize/4)))
        btnsurf, textbtn = text_objects(msg, smallText)
        textbtn.center = ((x + (w / 2)), (y + (h / 2)))
        gameDisplay.blit(btnImg, (x + int(fsize/8), y +int(fsize/8)))
        gameDisplay.blit(btnsurf, textbtn)
    pygame.display.update()

def showDiff():
    diff = bot.diffs
    button("Difficulty = " +diff, 525, 350, 175, 70, 20, RED, "img/ButtonBackground.jpg")

def show_inactive_buttons():  #als je niet kan callen/raisen/folden.
    global pot
    global betPlayer
    global betBot
    global totalPlayer

    button("Raise", 150, 420, 125, 38,20, RED,"img/ButtonBackground.jpg")
    button("Call/Check", 150, 480, 125, 38,20, RED,"img/ButtonBackground.jpg")
    button("Fold", 150, 540, 125, 38, 20,RED,"img/ButtonBackground.jpg")
    button("Bot: " + str(bot.amount_of_money) + " $", 550, 20, 100, 45,20,RED,"img/ButtonBackground.jpg")
    button("Pot: " + str(pot) + " $", 25, 400, 100, 50, 20,RED,"img/ButtonBackground.jpg")
    button("Balance: " + str(totalPlayer) + " $", 620, 450, 150, 45,20, RED,"img/ButtonBackground.jpg")
    if gameEndScreen is False:
        button("Bet: " + str(betPlayer) + " $", 425, 390, 100, 45,20, RED,"img/ButtonBackground.jpg")
        button("Bet: " + str(betBot) + " $", 425, 175, 100, 45,20, RED,"img/ButtonBackground.jpg")


def message_to_screen(msg,color):
    screen_text = font.render(msg,True,color)
    text_width, text_height = font.size(msg)
    gameDisplay.blit(screen_text, [(display_width/2)-text_width/2,display_height/2])

def show_deck():
    gameDisplay.blit(backOfCard, (685, 250))
    gameDisplay.blit(backOfCard, (683, 248))
    gameDisplay.blit(backOfCard, (681, 246))
    gameDisplay.blit(backOfCard, (679, 244))
    gameDisplay.blit(backOfCard, (677, 242))
    gameDisplay.blit(backOfCard, (675, 240))

def startAmounts():
    global pot
    global betPlayer
    global betBot
    global totalPlayer
    totalPlayer -= betPlayer
    bot.amount_of_money -= betBot
    pot += betPlayer + betBot
    betPlayer =0
    betBot = 0
    tableCards = {}
    print("pot aangepast")

def playerWins():
    global pot
    global totalPlayer
    totalPlayer += pot
    pot = 0

def botWins():
    global pot
    bot.amount_of_money += pot
    pot = 0

def splitWin():
    global pot
    global totalPlayer
    bot.amount_of_money += pot/2
    totalPlayer += pot/2
    pot = 0


def drawHandCards(hand, type):
    # Type is either PLAYER, BOT   (to implement: turn river flop?)

    if (type == "PLAYER"):
        var_int = 450
    elif (type == "BOT"):
        var_int = 20
    else:
        return 0  # something went wrong
    i = 0
    for val in hand.values():
        card = pygame.image.load("img/" + val + ".png").convert()
        gameDisplay.blit(card, (300 + i* 125, var_int))
        i += 1

def resetRound(ROUND = "niets"):
    global raised
    global played
    global ingezet
    global beurt
    global priority
    global botHasmove

    if ROUND == "Dealing":
        dealCards()
    startAmounts()
    played = 0
    raised = 0
    botHasmove = 0
    ingezet = 0
    beurt = priority


#draws table cards based on phase (FLOP, TURN, RIVER)
def drawTableCards(endgame = 0):
    global turnCard
    global riverCard
    if (len(tableCards)==0):
        pass
    if (len(tableCards)>= 3): #and (len(tableCards) == 3):
        i = 0
        for val in tableCards.values():
            if i<3:
                flopCard = pygame.image.load("img/" + val + ".png").convert()
                gameDisplay.blit(flopCard, (300 + i * 125, 240))
                i += 1
    if (len(tableCards)>= 4):
        turnCardImage = pygame.image.load("img/" + str(turnCard) + ".png").convert()
        gameDisplay.blit(turnCardImage, (175, 240))
    if (len(tableCards)== 5):
        riverCardImage = pygame.image.load("img/" + str(riverCard) + ".png").convert()
        gameDisplay.blit(riverCardImage, (50, 240))
    if (len(tableCards)>5):
        print("WTFF")

def ActivateButtons():
    button
#font importeren

#instance variables
backOfCard = pygame.image.load("img/back.png").convert()
background = pygame.image.load("img/background.jpg").convert()
StartGameBackground = pygame.image.load("img/StartGameBackground.jpg").convert()
background = pygame.transform.scale(background,(800,600))

#
# Start of the game
#
while not gameExit:
    #
    # Show startscreen
    #
    if startgamedraw ==0:
        gameDisplay.blit(StartGameBackground, (0, 0))
        button("Your Balance: " + str(totalPlayer) + " $", 300, 150, 200, 45, 20, RED, "img/ButtonBackground.jpg")
        pygame.display.update()
        startgamedraw =1
    #bepalen waar de muis is en aanpassen op basis van hover
    set_clickable_button("Start", 500, 250, 200, 80, 45, "Start", 0)
    set_clickable_button("Options", 500, 350, 200, 80, 45, "Options", 0)
    set_clickable_button("Quit", 500, 450, 200, 80, 45, "Quit", 0)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    #
    #  Start the game
    #
    while gameStart:
        ingezet = 0                         #Reset everything except money
        pot =0
        raised = 0
        whoFolded = 0
        betBot = 0
        dealingReset = 0
        flopReset = 0
        turnReset = 0
        riverReset = 0
        endgameReset = 0
        played = 0
        betPlayer = 0
        defaultBetSet = 0
        botHasmove = 0
        round = 0
        priority = priority * (-1)
        bot.move = ""
        tableCards = {}
        playerHand = {}
        bot.hand = {}
        prevcards = []
        show_deck()

        if setbackground ==0:
            gameDisplay.blit(background, (0, 0))
            show_inactive_buttons()
            setbackground =1

        #display text, and the labels on screen
        set_clickable_button("Start", 320, 270, 150, 70, 45, "Dealing", 0)
        pygame.display.update()
        clock.tick(15)
        #
        # If N is pressed, deal the first hand (aka go to dealing)
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                gameStart = False
                dealing = False
                flop = False
                turn = False
                river = False


#######################DEALING############################
##########################################################
        while dealing:
            show_deck()
            if dealingReset == 0:               #reset values
                resetRound("Dealing")
                gameDisplay.blit(background, (0, 0))
                gameDisplay.blit(backOfCard, (675, 240))
                check_for_defaultBet()
                show_inactive_buttons()
                dealingReset = 1



            pygame.display.update()

            #draw hand of he player
            drawHandCards(playerHand, "PLAYER")

            # Show the back of the hand of the bot
            for i in range(2):
                gameDisplay.blit(backOfCard, (300 + i * 125, 20))


            # update display and scores
            pygame.display.update()

            #let the bot decide on a move
            if botHasmove == 0:
                sim = Simulator(playerHand,tableCards,1000)
                bot.calc_move(bot.hand, tableCards)
                print("initieel gecalc zet: "+bot.move)
                botHasmove = 1

            #play the round
            inzetronde("Dealing")
##########################FLOP############################
##########################################################
            while flop:
                if flopReset==0:                        #reset values
                    resetRound()
                    flopReset =1

                #drawing the flop
                print("1e keer drawtablecards opgeroepen")
                print("tablecards: " + str(tableCards))
                drawTableCards()

                #let the bot decide on a move
                if botHasmove == 0:
                    bot.calc_move(bot.hand, tableCards)
                    print("flop gecalc move Bot: "+bot.move)
                    botHasmove = 1

                #update the screen
                show_inactive_buttons()
                pygame.display.update()

                #play the round
                inzetronde("Flop")

##########################TURN############################
##########################################################
                while turn:
                        if turnReset == 0:                  #reset values
                            resetRound()
                            turnReset = 1

                        #draw the turn card
                        drawTableCards()

                        #let the bot calculate a move
                        if botHasmove == 0:
                            bot.calc_move(bot.hand, tableCards)
                            print("turn gecalc move Bot: " + bot.move)
                            botHasmove = 1

                        #update screen
                        show_inactive_buttons()
                        pygame.display.update()

                        #Play the round
                        inzetronde("Turn")


###################################RIVER#########################
#################################################################
                        while river:
                            show_deck()
                            if riverReset == 0:                 #reset values
                                resetRound()
                                riverReset = 1
                            #Draw the rivercard
                            drawTableCards()

                            #let the bot decide on a move
                            if botHasmove == 0:
                                bot.calc_move(bot.hand, tableCards)
                                print("river gecalc move Bot: " + bot.move)
                                botHasmove = 1

                            #update screen
                            pygame.display.update()
                            show_inactive_buttons()

                            #Play the round
                            inzetronde("River")






    while Options:
        if optionsreset ==0:
            gameDisplay.blit(StartGameBackground, (0, 0))
            pygame.display.update()
            showDiff()
            optionsreset = 1


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                Options = False
        set_clickable_button("back", 60, 490, 150, 70, 45, "Continue", 0)
        set_clickable_button("Easy", 150, 150, 150, 70, 45, "Diff10", 0)
        set_clickable_button("Normal", 350, 150, 150, 70, 45, "Diff15", 0)
        set_clickable_button("Hard", 550, 150, 150, 70, 45, "Diff20", 0)


    while gameEndScreen:
        if endgameReset == 0:
            startAmounts()
            print("EndgameScreen:")
            gameDisplay.blit(background, (0, 0))
            show_deck()

            #  Show PlayerCards  #

            drawHandCards(playerHand, "PLAYER")

            # Show BotCards #
            drawHandCards(bot.hand, "BOT")

            # Show TableCards #
            drawTableCards()

            # Text: aankondiging #
            show_inactive_buttons()
            endgameReset = 1





        if whoFolded == 0:

            #If nobody folded, decide on a winner:
            sim = Simulator(playerHand, tableCards, 1000)
            besthandbot = sim.best_five(sim.cardsFromDictToNumeric(bot.hand), sim.cardsFromDictToNumeric(tableCards))
            besthandplayer = sim.best_five(sim.cardsFromDictToNumeric(playerHand),
                                           sim.cardsFromDictToNumeric(tableCards))
            winnaar = sim.compare_hands(besthandbot, besthandplayer)
            #act depending on who won
            if winnaar == -1:
                screen_textEndRound = font.render("YOU WON THE ROUND", True,
                                                  BLACK)
                text_widthEndRound, text_heightEndRound = font.size("YOU WON THE ROUND")
                gameDisplay.blit(screen_textEndRound, [75, 150])
                playerWins()


            elif winnaar == 0:
                screen_textEndRound = font.render("IT'S A TIE", True,
                                                  BLACK)
                text_widthEndRound, text_heightEndRound = font.size("IT'S A TIE")
                gameDisplay.blit(screen_textEndRound, [75, 150])
                splitWin()
            elif winnaar == 1:
                screen_textEndRound = font.render("YOU LOST THE ROUND", True,
                                                  BLACK)
                text_widthEndRound, text_heightEndRound = font.size("YOU LOST THE ROUND")
                gameDisplay.blit(screen_textEndRound, [75, 150])
                botWins()

        elif whoFolded == 1:        # DE BOT HEEFT GEFOLD
            screen_textEndRound = font.render("YOU WON THE ROUND", True,
                                              BLACK)
            text_widthEndRound, text_heightEndRound = font.size("YOU WON THE ROUND")
            gameDisplay.blit(screen_textEndRound, [75,150])
            screen_textBotFolded = font.render("THE BOT FOLDED", True, BLACK)
            text_widthBotFolded, text_heightBotFoldedRound = font.size("THE BOT FOLDED")
            gameDisplay.blit(screen_textBotFolded, [92,175])
            playerWins()

        elif whoFolded == 2:  # DE SPELER HEEFT GEFOLD
            screen_textEndRound = font.render("YOU LOST THE ROUND", True,
                                              BLACK)
            text_widthEndRound, text_heightEndRound = font.size("YOU LOST THE ROUND")
            gameDisplay.blit(screen_textEndRound, [75, 150])
            screen_textBotFolded = font.render("YOU FOLDED", True, BLACK)
            text_widthBotFolded, text_heightBotFoldedRound = font.size("THE BOT FOLDED")
            gameDisplay.blit(screen_textBotFolded, [115, 175])
            botWins()
        pygame.display.update()


        # Naar Volgende GameState #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                gameEndScreen = False
                dealing = False
                flop = False
                turn = False
                river = False
        set_clickable_button("Continue", 40, 50, 150, 70, 20, "Continue", 0)
        pygame.display.update()






#dit is nodig om de game af te sluiten
gameDisplay.fill(GREEN)
message_to_screen("The game is over",RED)
pygame.display.update()
time.sleep(1)
pygame.quit()
quit()