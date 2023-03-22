#
# @file Basic_Touch_Draw.py
# @brief Example of features of the Python edition
#
# @details Project Pervasive Displays Library Suite
# @n Ported to MicroPython for Raspberry Pi Pico
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


def wait(seconds):
    while (seconds > 0):
        print(">", seconds)
        time.sleep(1)
        seconds -= 1


myScreen = Screen(Screen_EPD.EXT3_370_0C_Touch)
myScreen.begin()

# Demo code
print("= Basic_Touch_Draw")
myScreen.regenerate()

myScreen.selectFont(Font.TERMINAL_12x16)

myScreen.clear()
myScreen.setOrientation(7)
myScreen.gText(10, 10, "Draw!")

myScreen.flush()

flagTouch = 0
x = 0
y = 0
z = 0
t = 0
index = 16

myScreen.setPenSolid(True)
while (index > 0):
    (flagTouch, x, y, z, t) = myScreen.getTouch()
    if (flagTouch):
        if ((t == touchEvent.RELEASE) or (t == touchEvent.MOVE)):
            # print(index, flagTouch, x, y, z, t)
            myScreen.circle(x, y, 4, Colour.BLACK)
            myScreen.flush()

            index -= 1
            print(index)

    time.sleep(0.010)

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
