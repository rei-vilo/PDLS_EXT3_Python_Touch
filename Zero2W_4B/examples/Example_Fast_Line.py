#
# @file Example_Fast_Line.py
# @brief Example of features of the Python edition
#
# @details Project Pervasive Displays Library Suite
# @n Ported to MicroPython and Adafruit Blinka
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


def wait(seconds):
    while (seconds > 0):
        print(">", seconds)
        time.sleep(1)
        seconds -= 1


myScreen = Screen()
myScreen.begin()

# Demo code
print("= Example_Fast_Line")
myScreen.setOrientation(7)

x = myScreen.screenSizeX()
x -= (x % 32)
y = myScreen.screenSizeY()
dx = int(x / 5)
dy = int(y / 5)

myScreen.selectFont(myScreen.fontMax())
myScreen.gText(0, 0, "Line")

myScreen.setPenSolid(True)

for index in range(0, x, 32):
    myScreen.dLine(index, dy, 32, dy * 4, Colour.BLACK)
    chrono = time.time()*1000.0
    myScreen.flush()
    chrono = time.time()*1000.0 - chrono
    text = "{chrono:.0f} ms".format(chrono=chrono)
    print(text)

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
