#
# @file Common_Fonts.py
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
print("= Common_Fonts")
myScreen.setOrientation(7)
y = 10

myScreen.selectFont(Font.TERMINAL_12x16)

myScreen.gText(10, y, myScreen.WhoAmI())
y += myScreen.characterSizeY()

myScreen.gText(10, y, str(myScreen.screenSizeX()) +
               "x" + str(myScreen.screenSizeY()))
y += myScreen.characterSizeY()
y += myScreen.characterSizeY()

myScreen.selectFont(Font.TERMINAL_6x8)
myScreen.gText(10, y, "Terminal6x8")
y += myScreen.characterSizeY()

myScreen.selectFont(Font.TERMINAL_8x12)
myScreen.gText(10, y, "Terminal8x12")
y += myScreen.characterSizeY()

myScreen.selectFont(Font.TERMINAL_12x16)
myScreen.gText(10, y, "Terminal12x16")
y += myScreen.characterSizeY()

# myScreen.selectFont(Font.TERMINAL_16x24)
# myScreen.gText(10, y, "Terminal16x24")
# y += myScreen.characterSizeY()

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
