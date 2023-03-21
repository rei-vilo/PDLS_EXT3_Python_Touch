#
# @file Basic_Touch_GUI.py
# @brief Example of features of the Python edition
#
# @details Project Pervasive Displays Library Suite
# @n Ported to MicroPython for Raspberry Pi Pico
# @n Based on highView technology
#
# @author Rei Vilo
# @date 22 Feb 2023
# @version 606
#
# @copyright (c) Rei Vilo, 2010-2023
# @copyright Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
# @see https://creativecommons.org/licenses/by-nc-sa/4.0/
#

from PDLS_EXT3_Python_Touch import *
from hV_GUI import *

# Let's go faster
machine.freq(240000000)

def wait(seconds):
    while (seconds > 0):
        print(">", seconds)
        time.sleep(1)
        seconds -= 1


myScreen = Screen()
myScreen.begin()

# Memory
import gc
print("- Memory")
print(". Before", gc.mem_free())
gc.collect()
print(". After", gc.mem_free())

# Demo code
print("= Basic_Touch_GUI")
# myScreen.regenerate()
print("! Be patient...")

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
        chrono = time.ticks_ms()
        if (myButtonNormal.check(Check.NORMAL)):
            k -= 1
            chrono = time.ticks_diff(time.ticks_ms(), chrono)
            text = "{0:s} in {1:d} ms ({2:d} left)".format(
                "Normal", int(chrono), k)
            myText.draw(text)
            print(text)

        chrono = time.ticks_ms()
        if (myButtonInstant.check(Check.INSTANT)):
            k -= 1
            chrono = time.ticks_diff(time.ticks_ms(), chrono)
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

