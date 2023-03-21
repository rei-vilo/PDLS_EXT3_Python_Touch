#
# @file Common_WhoAmI.py
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
print("= Common_WhoAmI")

myScreen.setOrientation(7)
myScreen.selectFont(Font.TERMINAL_16x24)
y = 10
myScreen.gText(10, y, myScreen.WhoAmI())
y += myScreen.characterSizeY()
text = "{x:d}x{y:d}".format(x=myScreen.screenSizeX(), y=myScreen.screenSizeY())
myScreen.gText(10, y, text)

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
