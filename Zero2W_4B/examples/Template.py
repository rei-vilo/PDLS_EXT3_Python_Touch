#
# @file Template.py
# @brief Example of features for Python edition
#
# @details Library for Pervasive Displays EXT3 - Basic level
# @n Based on highView technology
#
# @author Rei Vilo
# @date 22 Mar 2023
# @version 608
#
# @copyright (c) Rei Vilo, 2010-2023
# @copyright Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
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
print("= Common_WhoAmI")

myScreen.setOrientation(7)
myScreen.selectFont(Font.TERMINAL_16x24)
myScreen.gText(4, 4, myScreen.WhoAmI())

# Flush, wait, regenerate and end
myScreen.flush()

wait(5)
print("- Regenerate")
myScreen.regenerate()

print(". End")
