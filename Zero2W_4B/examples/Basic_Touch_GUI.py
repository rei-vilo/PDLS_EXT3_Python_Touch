#
# @file Basic_Touch_GUI.py
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
from hV_GUI import *


def wait(seconds):
    while (seconds > 0):
        print(">", seconds)
        time.sleep(1)
        seconds -= 1


myScreen = Screen(Screen_EPD.EXT3_370_0C_Touch)
myScreen.begin()

# Demo code
print("= Basic_Touch_GUI")
# myScreen.regenerate()

myGUI = GUI(myScreen)
myGUI.begin()

fontText = Font.TERMINAL_12x16
fontButton = Font.TERMINAL_8x12

myScreen.selectFont(fontText)

myScreen.clear()
myScreen.setOrientation(7)

myButtonNormal = Button(myGUI)
myButtonInstant = Button(myGUI)
myText = Text(myGUI)

x = myScreen.screenSizeX()
y = myScreen.screenSizeY()
dx = int(x / 7)
dy = int(y / 5)

myGUI.delegate(False)

myText.dDefine(0, dy, x, dy, fontText)
myButtonNormal.dStringDefine(dx * 1, dy * 3, dx * 2, dy, "Normal", fontButton)
myButtonInstant.dStringDefine(
    dx * 4, dy * 3, dx * 2, dy, "Instant", fontButton)

myText.draw("Empty")
myButtonNormal.draw()
myButtonInstant.draw()

myScreen.flush()

myGUI.delegate(True)

k = 8
while (k > 0):
    if (myScreen.getTouchInterrupt()):
        chrono = time.time()*1000.0
        if (myButtonNormal.check(Check.NORMAL)):
            k -= 1
            chrono = time.time()*1000.0 - chrono
            text = "{0:s} in {1:d} ms ({2:d} left)".format(
                "Normal", int(chrono), k)
            myText.draw(text)
            print(text)

        chrono = time.time()*1000.0
        if (myButtonInstant.check(Check.INSTANT)):
            k -= 1
            chrono = time.time()*1000.0 - chrono
            text = "{0:s} in {1:d} ms ({2:d} left)".format(
                "Instant", int(chrono), k)
            myText.draw(text)
            print(text)

    time.sleep(0.100)

myText.draw("Done")

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
