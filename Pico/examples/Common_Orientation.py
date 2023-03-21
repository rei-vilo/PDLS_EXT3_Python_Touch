#
# @file Common_Orientation.py
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


def wait(seconds):
    while (seconds > 0):
        print(">", seconds)
        time.sleep(1)
        seconds -= 1


myScreen = Screen()
myScreen.begin()

# Demo code
print("= Common_Orientation")
myScreen.selectFont(Font.TERMINAL_8x12)

for i in range(4):
    myScreen.setOrientation(i)
    text = "> Orientation " + str(i)
    myScreen.gText(10, 10, text)

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
