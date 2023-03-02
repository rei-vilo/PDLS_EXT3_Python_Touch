#
# @file Common_Text.py
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
print("= Common_Text")
myScreen.setOrientation(7)

x = int(myScreen.screenSizeX())
y = int(myScreen.screenSizeY())

myScreen.selectFont(Font.TERMINAL_8x12)

for i in range(2, 17):
    text = ".{index:x}".format(index=i-1)
    myScreen.gText(int(i * x / 17), 0, text)

for j in range(2, 16):
    text = "{index:x}.".format(index=j)
    myScreen.gText(0, int((j - 1)*y / 15), text)

for i in range(2, 17):
    for j in range(2, 16):
        k = (i - 1) + j * 16
        text = chr(k)
        dx = int(i * x / 17 + (x / 17 - myScreen.stringSizeX(text)) / 2)
        myScreen.gText(dx, int((j - 1)*y / 15), text)

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
