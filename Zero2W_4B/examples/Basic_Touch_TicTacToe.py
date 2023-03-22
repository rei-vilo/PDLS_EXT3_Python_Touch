#
# @file Basic_Touch_TicTacToe.py
# @brief Example of features of the Python edition
#
# @details Project Pervasive Displays Library Suite
# @n Ported to MicroPython and Adafruit Blinka
# @n Based on highView technology
#
# @author Rei Vilo
# @date 22 Mar 2023
# @version 608
#
# @copyright (c) Rei Vilo, 2010-2023
# @copyright Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
# @see https://creativecommons.org/licenses/by-nc-sa/4.0/
#

from PDLS_EXT3_Python_Touch import *
import random


class Player:
    NONE = 0
    HUMAN = 1
    MCU = 2


# Number of columns and rows
NUMBER = 4

myScreen = Screen(Screen_EPD.EXT3_370_0C_Touch)
myScreen.begin()

colourHuman = Colour.BLACK
colourMCU = Colour.GREY
colourGrid = Colour.GREY
colourBackground = Colour.WHITE
colourMessage = Colour.BLACK

x = 0
y = 0
dx = 0
dy = 0
minX = 0
maxX = 0
minY = 0
maxY = 0
tFlag = False
tx = 0
ty = 0
tz = 0
tt = 0
sizeTable = 0
sizeCell = 0
fsmScreen = 1
moves = 1
winner = 0  # 0 = Draw, 1 = Human, 2 = MCU

# Utilities
#
# @brief Display text centered on coordinates
# @param x0 x coordinate
# @param y0 y coordinate
# @param text text
# @param colour colour
#


def displayCenteredText(x0, y0, text, colour, font = Font.TERMINAL_12x16):
    myScreen.selectFont(font)
    dz = int(myScreen.characterSizeY() >> 1)
    myScreen.setPenSolid(True)
    myScreen.dRectangle(0, int(y0 - dz), myScreen.screenSizeX(),
                        int(2 * dz), colourBackground)

    dX = int(x0 - (myScreen.stringSizeX(text) >> 1))
    dY = int(y0 - (myScreen.characterSizeY() >> 1))
    myScreen.gText(dX, dY, text, colourMessage)


# holds position data 0 is blank, 1 human, 2 is MCU
board = [[0 for i in range(NUMBER)] for j in range(NUMBER)]

# Utilities


def setBoard(i, j, player):
    if (board[i][j] == Player.NONE):
        board[i][j] = player
        return True

    else:
        return False


def resetGame():
    global moves, winner
    for i in range(NUMBER):
        for j in range(NUMBER):
            board[i][j] = 0

    moves = 1
    winner = Player.NONE
    fsmScreen = 2


def drawStartScreen():
    # Draw white frame
    myScreen.clear(colourBackground)
    myScreen.rectangle(minX, minY, maxX, maxY, colourGrid)

    # Print "Tic Tac Toe" Text
    displayCenteredText(int(minX + sizeTable / 2), int(minY +
                        sizeTable * 1 / 4), "Tic Tac Toe", colourMessage)
    displayCenteredText(int(minX + sizeTable / 2), int(minY +
                        sizeTable * 3 / 4), "Touch to start", colourMessage, Font.TERMINAL_8x12)
    myScreen.flush()


def drawGameScreen():
    # Draw white frame
    myScreen.clear(colourBackground)

    for i in range(NUMBER + 1):
        z = int(i * sizeCell)
        myScreen.dLine(int(minX + z), int(minY + 0),
                       int(1), int(maxY - minY), colourGrid)
        myScreen.dLine(int(minX + 0), int(minY + z),
                       int(maxX - minX), int(1), colourGrid)

    myScreen.flush()


def drawGameOverScreen():
    global colourGrid, colourHuman, colourMCU, winner

    if (winner == Player.NONE):
        text = "DRAW"
        colour = colourGrid

    elif (winner == Player.HUMAN):
        text = "HUMAN WINS"
        colour = colourHuman

    elif (winner == Player.MCU):
        text = "MCU WINS"
        colour = colourMCU

    myScreen.clear(colourBackground)

    myScreen.rectangle(int(minX), int(minY), int(maxX), int(maxY), colourGrid)
    displayCenteredText(int(minX + sizeTable / 2), int(minY +
                        sizeTable * 3 / 4), text, colour)
    displayCenteredText(int(minX + sizeTable / 2), int(minY +
                        sizeTable * 1 / 4), "GAME OVER", colourMessage)
    displayCenteredText(int(minX + sizeTable / 2), int(minY +
                        sizeTable * 2 / 4), "Touch to start", colourMessage, Font.TERMINAL_8x12)

    myScreen.flush()


def playGame():
    flag = True
    global moves, winner, fsmScreen

    while (flag):
        if (moves % 2 == 1):
            displayCenteredText(int(maxX / 2), int(maxY / 8),
                                "MCU plays", colourMessage, Font.TERMINAL_8x12)
            myScreen.flush()
            moveMCU()
        else:
            displayCenteredText(int(maxX / 2), int(maxY / 8),
                                "Human plays", colourMessage, Font.TERMINAL_8x12)
            myScreen.flush()
            moveHuman()

        printBoard()
        winner = checkWinner()
        # drawWinnerPlayer(winner)
        moves += 1

        flag = (winner == Player.NONE) and (moves < NUMBER * NUMBER + 1)

    print("--- ")
    time.sleep(0.100)

    if (winner == Player.HUMAN):
        print("HUMAN WINS")

    elif (winner == Player.MCU):
        print("MCU WINS")

    else:
        print("DRAW")

    time.sleep(0.100)
    fsmScreen = 3
    drawGameOverScreen()


def moveHuman():
    validMove = False

    print("--- Player.HUMAN")

    tt = touchEvent.NONE
    ttt = touchEvent.NONE
    while (not validMove):
        # Touch acquisition
        while (tt != touchEvent.PRESS):
            (tflag, tx, ty, tz, tt) = myScreen.getTouch()
            time.sleep(0.010)

        # Wrong coordinates with touchEvent.RELEASE
        while (tt != touchEvent.RELEASE):
            (tflag, tx, ty, tz, tt) = myScreen.getTouch()
            time.sleep(0.010)

        i = int((tx - minX) / sizeCell)
        j = int((ty - minY) / sizeCell)

        if ((i < NUMBER) and (j < NUMBER)):
            validMove = setBoard(i, j, Player.HUMAN)

        time.sleep(0.010)

    drawMovePlayer(i, j, Player.HUMAN)


def printBoard():
    global moves
    print("--- Move", moves)
    for i in range(NUMBER):
        print("[ ", end=" ")
        for j in range(NUMBER):
            # print(board[i * 3 + j])
            print(board[j][i], end=" ")

        print("]")
    print("")


def checkHuman(i, j):
    k = 0

    # Check lines
    for i in range(NUMBER):
        k = 0
        for j in range(NUMBER):
            if (board[i][j] == Player.HUMAN):
                k += 1

        if (k == NUMBER - 1):
            for j in range(NUMBER):
                if (board[i][j] == Player.NONE):
                    i = i
                    j = j
                    return True, i, j

    # Check diagonal
    k = 0
    for i in range(NUMBER):
        if (board[i][i] == Player.HUMAN):
            k += 1

    if (k == NUMBER - 1):
        for i in range(NUMBER):
            if (board[i][i] == Player.NONE):
                i = i
                j = i
                return True, i, j

    return False, i, j


def moveMCU():
    global moves
    flagPlayed = False
    counter = 0
    movesPlayed = 0
    print("--- Player.MCU")

    i = 0
    j = 0

    # Four corners
    firstMovesI = [0, 0, NUMBER - 1, NUMBER - 1]
    firstMovesJ = [0, NUMBER - 1, 0, NUMBER - 1]
    # will use these positions first
    for counter in range(4):  # Count first moves played
        # First move is played by someone
        if (board[firstMovesI[counter]][firstMovesJ[counter]] != 0):
            movesPlayed += 1

    flagLoop = True
    while flagLoop:
        if (moves <= 2):  # First two moves
            randomMove = random.randint(0, 3)
            i = firstMovesI[randomMove]
            j = firstMovesI[randomMove]
        else:
            result, i, j = checkHuman(i, j)
            if (result == False):
                if (movesPlayed == 4):  # After two first moves
                    i = random.randint(0, NUMBER-1)
                    j = random.randint(0, NUMBER-1)
                else:
                    randomMove = random.randint(0, 3)
                    i = firstMovesI[randomMove]
                    j = firstMovesJ[randomMove]
            else:
                i = random.randint(0, NUMBER-1)
                j = random.randint(0, NUMBER-1)

        flagPlayed = setBoard(i, j, Player.MCU)
        flagLoop = (flagPlayed == False)

    drawMovePlayer(i, j, Player.MCU)


def drawMovePlayer(i, j, player):
    x0 = int(minX + i * sizeCell)
    y0 = int(minY + j * sizeCell)
    dz = int(sizeCell >> 1) - 8

    myScreen.setPenSolid(True)
    if (player == Player.MCU):
        myScreen.circle(int(x0 + sizeCell / 2), int(y0 +
                        sizeCell / 2), dz, colourMCU)

    elif (player == Player.HUMAN):
        myScreen.dRectangle(x0 + 8, y0 + 8, sizeCell -
                            16, sizeCell - 16, colourHuman)

    myScreen.setPenSolid(False)
    myScreen.flush()


def checkWinnerPlayer(player):
    flag = False
    k1 = 0
    k2 = 0

    # Check lines and columns
    if (not flag):
        for i in range(NUMBER):
            k1 = 0
            k2 = 0
            for j in range(NUMBER):
                if (board[i][j] == player):
                    k1 += 1

                if (board[j][i] == player):
                    k2 += 1

            flag |= (k1 == NUMBER) | (k2 == NUMBER)

    # Check diagonal and inverse diagonal
    if (not flag):
        k1 = 0
        k2 = 0
        for i in range(NUMBER):
            if (board[i][i] == player):
                k1 += 1

            if (board[NUMBER - 1 - i][i] == player):
                k2 += 1

        flag |= (k1 == NUMBER) | (k2 == NUMBER)

    return flag


def drawWinnerPlayer(player):
    flag = False
    k1 = 0
    k2 = 0
    x0 = 0
    y0 = 0
    dz = (sizeCell >> 1) - 8

    myScreen.setPenSolid()
    # Check lines and columns
    if (not flag):
        for i in range(NUMBER):
            k1 = 0
            k2 = 0
            for j in range(NUMBER):
                if (board[i][j] == player):
                    k1 += 1

                if (board[j][i] == player):
                    k2 += 1

            if (k1 == NUMBER):
                flag = True
                x0 = i * sizeCell

                if (player == Player.MCU):

                    for k in range(1, NUMBER):
                        y0 = int(k * sizeCell - sizeCell / 3)
                        myScreen.circle(
                            int(minX + x0 + sizeCell / 2), int(minY + y0 + sizeCell / 2), dz, colourMCU)
                        y0 = int(k * sizeCell - sizeCell * 2 / 3)
                        myScreen.circle(int(minX + x0 + sizeCell / 2),
                                        int(minY + y0 + sizeCell / 2), dz, colourMCU)

                if (player == Player.HUMAN):

                    for k in range(1, NUMBER):
                        y0 = int(k * sizeCell - sizeCell / 2)

                        myScreen.dRectangle(
                            minX + x0 + 8, minY + y0 + 8, sizeCell - 16, sizeCell - 16, colourHuman)

            if (k2 == NUMBER):
                flag = True
                y0 = int(i * sizeCell)

                if (player == Player.MCU):

                    for k in range(1, NUMBER):
                        x0 = int(k * sizeCell - sizeCell / 3)
                        myScreen.circle(
                            int(minX + x0 + sizeCell / 2), int(minY + y0 + sizeCell / 2), dz, colourMCU)
                        x0 = int(k * sizeCell - sizeCell * 2 / 3)
                        myScreen.circle(int(minX + x0 + sizeCell / 2),
                                        int(minY + y0 + sizeCell / 2), dz, colourMCU)

                elif (player == Player.HUMAN):
                    for k in range(1, NUMBER):
                        x0 = int(k * sizeCell - sizeCell / 2)

                        myScreen.dRectangle(
                            minX + x0 + 8, minY + y0 + 8, sizeCell - 16, sizeCell - 16, colourHuman)

    # Check diagonal and inverse diagonal
    if (not flag):
        k1 = 0
        k2 = 0
        for i in range(NUMBER):
            if (board[i][i] == player):
                k1 += 1

            if (board[NUMBER - 1 - i][i] == player):
                k2 += 1

        if (k1 == NUMBER):
            flag = True

            if (player == Player.MCU):

                for k in range(1, NUMBER):
                    x0 = int(k * sizeCell - sizeCell / 3)
                    y0 = int(k * sizeCell - sizeCell / 3)
                    myScreen.circle(int(minX + x0 + sizeCell / 2),
                                    int(minY + y0 + sizeCell / 2), dz, colourMCU)
                    x0 = int(k * sizeCell - sizeCell * 2 / 3)
                    y0 = int(k * sizeCell - sizeCell * 2 / 3)
                    myScreen.circle(int(minX + x0 + sizeCell / 2),
                                    int(minY + y0 + sizeCell / 2), dz, colourMCU)

            elif (player == Player.HUMAN):

                for k in range(1, 2*NUMBER):
                    x0 = int(k * sizeCell - sizeCell / 2)
                    y0 = int(k * sizeCell - sizeCell / 2)
                    myScreen.dRectangle(
                        minX + x0 + 8, minY + y0 + 8, sizeCell - 16, sizeCell - 16, colourHuman)
                    x0 = int(k * sizeCell - sizeCell * 2 / 3)
                    y0 = int(k * sizeCell - sizeCell * 2 / 3)
                    myScreen.dRectangle(
                        minX + x0 + 8, minY + y0 + 8, sizeCell - 16, sizeCell - 16, colourHuman)

        if (k2 == NUMBER):
            flag = True

            if (player == Player.MCU):

                for k in range(1, NUMBER):
                    x0 = int(k * sizeCell - sizeCell / 3)
                    y0 = int((NUMBER - k) * sizeCell - sizeCell / 3)
                    myScreen.circle(int(minX + x0 + sizeCell / 2),
                                    int(minY + y0 + sizeCell / 2), dz, colourMCU)
                    x0 = int(k * sizeCell - sizeCell * 2 / 3)
                    y0 = int((NUMBER - k) * sizeCell - sizeCell * 2 / 3)
                    myScreen.circle(int(minX + x0 + sizeCell / 2),
                                    int(minY + y0 + sizeCell / 2), dz, colourMCU)

            elif (player == Player.HUMAN):

                for k in range(1, NUMBER):
                    x0 = int(k * sizeCell - sizeCell / 3)
                    y0 = int((NUMBER - k) * sizeCell - sizeCell / 3)
                    myScreen.dRectangle(
                        minX + x0 + 8, minY + y0 + 8, sizeCell - 16, sizeCell - 16, colourHuman)
                    x0 = int(k * sizeCell - sizeCell * 2 / 3)
                    y0 = int((NUMBER - k) * sizeCell - sizeCell * 2 / 3)
                    myScreen.dRectangle(
                        minX + x0 + 8, minY + y0 + 8, sizeCell - 16, sizeCell - 16, colourHuman)

    myScreen.setPenSolid(False)
    myScreen.flush()


def checkWinner():
    # checks board to see if there is a winner
    # places result in the global variable 'winner'
    if (checkWinnerPlayer(Player.HUMAN)):
        return Player.HUMAN

    elif (checkWinnerPlayer(Player.MCU)):
        return Player.MCU

    else:
        return Player.NONE

# Functions


# Start
print("begin... ")
myScreen.begin()
print(" done")

myScreen.setOrientation(0)
myScreen.selectFont(Font.TERMINAL_12x16)
myScreen.regenerate()

print(myScreen.WhoAmI())

minX = 0
maxX = myScreen.screenSizeX()
minY = 0
maxY = myScreen.screenSizeY()

sizeTable = min(maxX - minX, maxY - minY)
sizeCell = int(sizeTable / NUMBER)

w = int((maxX - minX - NUMBER * sizeCell) / 2)
minX += w
maxX -= w
w = int((maxY - minY - NUMBER * sizeCell) / 2)
minY += w
maxY -= w

colourHuman = Colour.BLACK
colourMCU = Colour.GREY
colourGrid = Colour.GREY
colourBackground = Colour.WHITE
colourMessage = Colour.BLACK

printBoard()
drawStartScreen()

# Add loop code
while (True):
    (tFlag, tx, ty, tz, tt) = myScreen.getTouch()

    if (tt == touchEvent.PRESS):
        print("=== START")
        myScreen.regenerate()
        resetGame()
        drawGameScreen()
        playGame()
        time.sleep(0.010)

    time.sleep(0.100)
