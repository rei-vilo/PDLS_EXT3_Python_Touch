#
# @file Common_Colours.py
# @brief Example of features of the Python edition
#
# @details Project Pervasive Displays Library Suite
# @n Ported to MicroPython and Adafruit Blinka
# @n Based on highView technology
#
# @author Rei Vilo
# @date 20 Mar 2023
# @version 607
#
# @copyright (c) Rei Vilo, 2010-2023
# @copyright Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
# @see https://creativecommons.org/licenses/by-nc-sa/4.0/
#

from PDLS_EXT3_Python_Touch import *


def wait(seconds):
    while (seconds > 0):
        print(">", seconds)
        time.sleep(1)
        seconds -= 1


myScreen = Screen()
myScreen.begin()

# Demo code
print("= Common_Colours")
myScreen.setOrientation(7)

maxSize = int(min((myScreen.screenSizeX() * 10 / 50),
              (myScreen.screenSizeY() * 10 / 35)))
dx = int((myScreen.screenSizeX() - maxSize * 50 / 10) / 2)
dy = int((myScreen.screenSizeY() - maxSize * 35 / 10) / 2)

y0 = int(dy + maxSize * 4 / 2)
x0 = int(dx + maxSize / 2)
myScreen.dRectangle(x0 - 2, y0 - 2, maxSize + 4, maxSize + 4, Colour.BLACK)
x0 = int(dx + maxSize * 4 / 2)
myScreen.dRectangle(x0 - 2, y0 - 2, maxSize + 4, maxSize + 4, Colour.BLACK)
x0 = int(dx + maxSize * 7 / 2)
myScreen.dRectangle(x0 - 2, y0 - 2, maxSize + 4, maxSize + 4, Colour.BLACK)

myScreen.setPenSolid()
myScreen.selectFont(Font.TERMINAL_6x8)

x0 = int(dx + maxSize / 2)
y0 = int(dy + maxSize * 4 / 2)
# White
myScreen.dRectangle(x0, y0, maxSize, maxSize, Colour.WHITE)
myScreen.gText(x0, y0 + maxSize + 6, "white", Colour.BLACK)

x0 = int(dx + maxSize * 4 / 2)
y0 = int(dy + maxSize * 4 / 2)
# Grey
myScreen.dRectangle(x0, y0, maxSize, maxSize, Colour.GREY)
myScreen.gText(x0, y0 + maxSize + 6, "grey", Colour.BLACK)

x0 = int(dx + maxSize * 7 / 2)
y0 = int(dy + maxSize * 4 / 2)
# Black
myScreen.dRectangle(x0, y0, maxSize, maxSize, Colour.BLACK)
myScreen.gText(x0, y0 + maxSize + 6, "black", Colour.BLACK)

myScreen.selectFont(Font.TERMINAL_8x12)
myScreen.gText(0, 0, myScreen.WhoAmI(), Colour.BLACK)

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
