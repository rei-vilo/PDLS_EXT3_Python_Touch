#
# @file hV_GUI.py
# @brief Basic GUI with text and button
#
# @details Project Pervasive Displays Library Suite
# Ported to Python
# @n Based on highView technology
#
# @author Rei Vilo
# @date 20 Mar 2023
# @version 607
#
# @copyright (c) Rei Vilo, 2010-2023
# @copyright Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# @see https://creativecommons.org/licenses/by-nc-sa/4.0/
#

__copyright__ = "Copyright (C) 2010-2023 Rei Vilo"
__licence__ = "CC BY-NC-SA 4.0 - Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International"
__version__ = "6.0.7"

from PDLS_EXT3_Python_Touch import *


class Check:
    NORMAL = 0
    INSTANT = 1


class State:
    RELEASED = 0
    TOUCHED = 1


class GUI:
    _screen: Screen
    _colourFront = Colour.BLACK
    _colourBack = Colour.WHITE
    _colourMiddle = Colour.GREY
    _delegate = False

    def __init__(self, _screen: Screen):
        self._screen = _screen

    def begin(self):
        self._colourFront = Colour.BLACK
        self._colourBack = Colour.WHITE
        self._colourMiddle = Colour.GREY
        self._delegate = False

    def setColours(self, frontColour, backColour, middleColour):
        self._colourFront = frontColour
        self._colourBack = backColour
        self._colourMiddle - middleColour

    def delegate(self, flagDelegate=True):
        self._delegate = flagDelegate


class Text:
    _gui: GUI
    _x0 = 0
    _y0 = 0
    _dx = 0
    _dy = 0
    _fontSize = 0

    def __init__(self, _gui: GUI):
        self._gui = _gui

    def dDefine(self, x0, y0, dx, dy, size=0):
        self._x0 = x0
        self._y0 = y0
        self._dx = dx
        self._dy = dy
        self._fontSize = size

    def draw(self, text: str):
        self._gui._screen.selectFont(self._fontSize)
        k = int(self._gui._screen.stringLengthToFitX(text, self._dx - 8))
        _text = text[0:k]

        _xt = self._x0 + \
            ((self._dx - self._gui._screen.stringSizeX(_text)) >> 1)
        _yt = self._y0 + ((self._dy - self._gui._screen.characterSizeY()) >> 1)

        self._gui._screen.setPenSolid(True)
        self._gui._screen.dRectangle(self._x0, self._y0, self._dx,
                                     self._dy, self._gui._colourBack)
        self._gui._screen.gText(_xt, _yt, _text, self._gui._colourFront)

        if (self._gui._delegate):
            self._gui._screen.flush()


class Button(Text):
    def dStringDefine(self, x0, y0, dx, dy, text: str, size=0):
        self.dDefine(x0, y0, dx, dy, size)
        super(Button, self).draw(text)  # calling parent method Text.draw()
        self.draw(State.RELEASED)

    def draw(self, state=State.RELEASED):
        self._gui._screen.setPenSolid(False)
        self._gui._screen.dRectangle(self._x0 + 1, self._y0 + 1,
                                     self._dx - 2, self._dy - 2, self._gui._colourFront)

        if (state == State.TOUCHED):
            self._gui._screen.dRectangle(
                self._x0, self._y0, self._dx, self._dy, self._gui._colourFront)
            self._gui._screen.dRectangle(
                self._x0 + 2, self._y0 + 2, self._dx - 4, self._dy - 4, self._gui._colourFront)
        else:  # Released
            self._gui._screen.dRectangle(
                self._x0, self._y0, self._dx, self._dy, self._gui._colourBack)
            self._gui._screen.dRectangle(
                self._x0 + 2, self._y0 + 2, self._dx - 4, self._dy - 4, self._gui._colourBack)

        if (self._gui._delegate):
            self._gui._screen.flush()

    def check(self, mode=Check.NORMAL):
        x = 0
        y = 0
        z = 0
        t = 0
        flagTouch = False
        flagResult = False

        (flagTouch, x, y, z, t) = self._gui._screen.getTouch()
        if (flagTouch):  # Touched
            if ((x >= self._x0) and (x < self._x0 + self._dx) and (y >= self._y0) and (y < self._y0 + self._dy)):

                if (mode == Check.INSTANT):
                    return True

                self.draw(State.TOUCHED)

                flagWhile = True
                while (flagWhile):
                    time.sleep(0.100)
                    (flagTouch, x, y, z, t) = self._gui._screen.getTouch()
                    flagWhile = (t != touchEvent.RELEASE)

                # Released
                if ((x >= self._x0) and (x < self._x0 + self._dx) and (y >= self._y0) and (y < self._y0 + self._dy)):
                    flagResult = True

                self.draw(State.RELEASED)

        return flagResult
