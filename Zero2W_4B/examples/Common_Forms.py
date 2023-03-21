#
# @file Common_Forms.py
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
print("= Common_Forms")
myScreen.setOrientation(7)

x = myScreen.screenSizeX()
y = myScreen.screenSizeY()
z = min(x, y)

myScreen.setPenSolid(False)
myScreen.dRectangle(0, 0, x, y, Colour.BLACK)
myScreen.dLine(0, 0, x, y, Colour.BLACK)

myScreen.setPenSolid(True)
myScreen.circle(int(x / 3), int(y / 3), int(z / 4), Colour.GREY)
# myScreen.triangle(x * 2 / 3, y / 3, x * 3 / 4, y * 2 / 3 - 10, x - 10, 10, Colour.black)
myScreen.dRectangle(int(x / 3), int(y * 2 / 3),
                    int(x / 3), int(y / 4), Colour.BLACK)

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
