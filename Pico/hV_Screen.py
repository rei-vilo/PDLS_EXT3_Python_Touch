#
# @file hV_Screen.py
# @brief Driver for Pervasive Displays 2.70-Touch screen with EXT3-1 and EXT3-Touch boards
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

from machine import Pin, SPI, I2C
import time
from hV_Fonts import *


# @brief Colours constants
# Colours RGB = 565 Red  Green Blue
#                   4321054321043210
class Colour:
    BLACK = 0b0000000000000000  # Black
    WHITE = 0b1111111111111111  # White
    GREY = 0b0111101111101111  # Grey
    GRAY = 0b0111101111101111  # American-English variant for grey

# @brief Touch events


class touchEvent:
    NONE = 0  # no event
    PRESS = 1  # press event
    RELEASE = 2  # release event
    MOVE = 3  # move event
    STRING = ["NONE", "PRESS", "RELEASE", "MOVE"]

# @brief Main class


class Screen:
    # GPIOs for Raspberry Pi Pico
    # Pin refers to the GPIO, not the pin number
    # Board
    boardLED = Pin(25, Pin.OUT)

    # Touch
    touchINT = Pin(2, Pin.IN) 
    touchRESET = Pin(3, Pin.OUT)
    i2cAddress = 0x41

    # Panel
    panelCS = Pin(17, Pin.OUT)
    flashCS = Pin(10, Pin.OUT)
    panelRESET = Pin(11, Pin.OUT)
    panelDC = Pin(12, Pin.OUT)
    panelBUSY = Pin(13, Pin.IN)

    # Parameters
    _fontSize = 0
    _fontSolid = False
    _penSolid = False
    _invert = False
    _fontSpaceX = 1
    _fontSpaceY = 1
    _orientation = 0
    _font = Font.font_s

    # COG registers
    indexE5_data = [0x19]  # temperature
    indexE0_data = [0x02]  # activate temperature
    index00_data = [0xcf, 0x8d]  # PSR, constant
    # index50_data goes here

    # Screen variables for 2.71-Touch
    _screenSizeV = 264  # vertical = wide size
    _screenSizeH = 176  # horizontal = small size
    _screenDiagonal = 270  # 270 for touch
    _screenColourBits = 2
    _bufferDepth = _screenColourBits  # 2 colours
    _bufferSizeV = _screenSizeV  # vertical = wide size
    _bufferSizeH = (_screenSizeH >> 3)  # horizontal = small size 112 / 8
    _pageColourSize = _bufferSizeV * _bufferSizeH
    _newImage = bytearray(_pageColourSize)  # Next
    _oldImage = bytearray(_pageColourSize)  # Previous
    _i2cAddress = 0x41

    # Touch
    _touchPrevious = touchEvent.NONE
    _touchX = 0
    _touchY = 0
    _touchXmin = 0
    _touchYmin = 0
    _touchXmax = 0
    _touchYmax = 0

    # _i2c = busio.I2C(scl=board.SCL, sda=board.SDA, frequency=400000)
    _i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400_000)
    # _spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
    _spi = SPI(0, 8_000_000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

    # Utilities
    def __bitSet(self, value, bit_index):
        return value | (1 << bit_index)

    def __bitClear(self, value, bit_index):
        return value & ~(1 << bit_index)

    def __bitRead(self, value, bit_index):
        return value & (1 << bit_index)

    def __checkRange(self, value, valueMin, valueMax):
        localMin = min(valueMin, valueMax)
        localMax = max(valueMin, valueMax)

        return min(max(localMin, value), localMax)

    def __mapValue(self, value, valueMin, valueMax, targetMin, targetMax):
        target = (value - valueMin) * (targetMax - targetMin) / \
            (valueMax - valueMin) + targetMin
        return int(target)

    # SPI utilities
    def __waitBusy(self):
        # LOW = busy, HIGH = ready
        while (self.panelBUSY.value() != 1):
            time.sleep(0.032)

    def __sendCommand8(self, command):
        """
        print("%16s [0x%02x]" % ("__sendCommand8", command))
        """
        self.panelDC.value(0)  # DC Low = Command
        self.panelCS.value(0)  # CS Low = Select

        time.sleep(0.050)
        self._spi.write(bytearray([command]))
        time.sleep(0.050)

    def __sendIndexData(self, index, data, size):
        """
        print("%16s [0x%02x] " % ("__sendIndexData", index), end=" ")

        for i in data[0:8]:
            print("0x%02x" % (i), end=" ")
        if (size >= 8):
            print("...", end=" ")
        print()
        """
        self.panelDC.value(0)  # DC Low = Command
        self.panelCS.value(0)  # CS Low = Select

        time.sleep(0.050)
        self._spi.write(bytearray([index]))
        time.sleep(0.050)

        self.panelCS.value(1)  # CS High = Unselect
        self.panelDC.value(1)  # DC High = Data
        self.panelCS.value(0)  # CS Low = Select

        time.sleep(0.050)
        self._spi.write(bytearray(data))
        time.sleep(0.050)

        self.panelCS.value(1)  # CS High = Unselect

    # COG utilities
    def __COG_initial(self):
        # New algorithm
        self.__sendIndexData(0x00, [0x00], 1)  # Soft-reset
        self.__waitBusy()

        # Temperature settings
        self.__sendIndexData(0xe5, [0x19 | 0x40], 1)  # IN Temperature: 25C
        self.__sendIndexData(0xe0, [0x02], 1)  # Activate Temperature
        self.__sendIndexData(0x00, [0xcf | 0x10, 0x8d | 0x02], 2)  # PSR
        # _flag50a goes here

    def __COG_sendImageDataFast(self):
        self.__sendIndexData(0x10, self._oldImage,
                             self._pageColourSize)  # Previous frame
        self.__sendIndexData(0x13, self._newImage,
                             self._pageColourSize)  # Next frame
        self._oldImage[:] = self._newImage  # Copy displayed next to previous

    def __COG_update(self):
        # _flag50b goes here

        self.__sendCommand8(0x04)  # Power on
        self.panelCS.value(1)  # CS# = 1
        self.__waitBusy()

        self.__sendCommand8(0x12)  # Display Refresh
        self.panelCS.value(1)  # CS# = 1
        self.__waitBusy()

    def __COG_powerOff(self):
        self.__sendCommand8(0x02)  # Turn off DC/DC
        self.panelCS.value(1)  # CS# = 1
        self.__waitBusy()

    # Functions
    def __init__(self):
        pass

    def __del__(self):
        pass

    def begin(self):
        self.flashCS.value(1)
        self.panelCS.value(1)

        # Panel reset
        time.sleep(0.005)
        self.panelRESET.value(1)
        time.sleep(0.005)
        self.panelRESET.value(0)
        time.sleep(0.010)
        self.panelRESET.value(1)
        time.sleep(0.005)
        self.panelCS.value(1)
        time.sleep(0.005)

        # Touch reset
        self.touchRESET.value(1)
        time.sleep(0.100)
        self.touchRESET.value(0)
        time.sleep(0.100)
        self.touchRESET.value(1)
        time.sleep(0.100)

        # I2C
        self._i2c.writeto(self._i2cAddress, bytes([0x20]))
        bufferRead = bytearray(10)
        self._i2c.readfrom_into(self._i2cAddress, bufferRead)

        self._touchXmin = 0
        self._touchXmax = bufferRead[0] + (bufferRead[1] << 8)
        self._touchYmin = 0
        self._touchYmax = bufferRead[2] + (bufferRead[3] << 8)

        # Font and touch
        self.selectFont(0)
        self._touchPrevious = touchEvent.NONE

    def WhoAmI(self):
        return "iTC 2'70-Touch"

    def flush(self):
        # Configure
        self.__COG_initial()

        # Send image data
        self.__COG_sendImageDataFast()

        # Update
        self.__COG_update()
        self.__COG_powerOff()

    def clear(self, colour=Colour.WHITE):
        if (colour == Colour.GREY):
            for i in range(self._bufferSizeV):
                if ((i % 2) == 0):
                    pattern = 0b10101010
                else:
                    pattern = 0b01010101

                for j in range(self._bufferSizeH):
                    self._newImage[i * self._bufferSizeH + j] = pattern

        elif ((colour == Colour.WHITE) ^ self._invert):
            # physical black 00
            for i in range(self._bufferSizeV):
                for j in range(self._bufferSizeH):
                    self._newImage[i * self._bufferSizeH + j] = 0x00

        else:
            # physical white 10
            for i in range(self._bufferSizeV):
                for j in range(self._bufferSizeH):
                    self._newImage[i * self._bufferSizeH + j] = 0xff

    def regenerate(self):
        self.clear(Colour.BLACK)
        self.flush()
        time.sleep(0.100)

        self.clear(Colour.WHITE)
        self.flush()
        time.sleep(0.100)

    def invert(self, flag):
        self._invert = flag

    def point(self, x1, y1, colour):
        # Orient and check coordinates are within screen
        # _orientCoordinates() returns false = success, true = error
        (flag, x1, y1) = self.__orientCoordinates(x1, y1)
        if (flag):
            return 0

        (z1, t1) = self.__getZT(x1, y1)

        # Convert combined colours into basic colours
        flagOdd = ((x1 + y1) % 2 == 0)

        if (colour == Colour.GREY):
            if (flagOdd):
                colour = Colour.BLACK  # black
            else:
                colour = Colour.WHITE  # white

        # Basic colours
        if ((colour == Colour.WHITE) ^ self._invert):
            # physical black 00
            self._newImage[z1] = self.__bitClear(
                self._newImage[z1], t1)

        elif ((colour == Colour.BLACK) ^ self._invert):
            # physical white 10
            self._newImage[z1] = self.__bitSet(
                self._newImage[z1], t1)

    def setOrientation(self, orientation):
        if (orientation == 6):
            self._orientation = 0
            if (self.screenSizeX() > self.screenSizeY()):
                self._orientation = 1

        elif (orientation == 7):
            self._orientation = 0
            if (self.screenSizeX() < self.screenSizeY()):
                self._orientation = 1

        self._orientation = orientation % 4

    def getOrientation(self):
        return self._orientation

    def __orientCoordinates(self, x, y):
        flag = True  # false = success, true = error

        if (self._orientation == 3):  # checked, previously 1

            if ((x < self._screenSizeV) and (y < self._screenSizeH)):
                x = self._screenSizeV - 1 - x
                flag = False

        elif (self._orientation == 2):  # checked

            if ((x < self._screenSizeH) and (y < self._screenSizeV)):
                x = self._screenSizeH - 1 - x
                y = self._screenSizeV - 1 - y
                (y, x) = (x, y)  # swap
                flag = False

        elif (self._orientation == 1):  # checked, previously 3

            if ((x < self._screenSizeV) and (y < self._screenSizeH)):
                y = self._screenSizeH - 1 - y
                flag = False

        else:  # checked

            if ((x < self._screenSizeH) and (y < self._screenSizeV)):
                (y, x) = (x, y)  # swap
                flag = False

        return flag, x, y

    def screenSizeX(self):
        if ((self._orientation == 1) or (self._orientation == 3)):
            return self._screenSizeV  # _maxX

        elif ((self._orientation == 0) or (self._orientation == 2)):
            return self._screenSizeH  # _maxX

        else:
            return 0

    def screenSizeY(self):
        if ((self._orientation == 1) or (self._orientation == 3)):
            return self._screenSizeH  # _maxY

        elif ((self._orientation == 0) or (self._orientation == 2)):
            return self._screenSizeV  # _maxY

        else:
            return 0

    def screenDiagonal(self):
        return self._screenDiagonal

    def screenColourBits(self):
        return self._screenColourBits

    def __getZT(self, x1, y1):
        return x1 * self._bufferSizeH + (y1 >> 3), 7 - (y1 % 8)

    def readPixel(self, x1, y1):
        # Orient and check coordinates are within screen
        # _orientCoordinates() returns false = success, true = error
        (flag, x1, y1) = self.__orientCoordinates(x1, y1)
        if (flag):
            return 0

        result = 0
        value(0)

        (z1, t1) = self.__getZT(x1, y1)

        value = self.__bitRead(self._newImage[z1], t1)
        value <<= 4
        value &= 0b11110000

        # red = 0-1, black = 1-0, white 0-0
        if (value == 0x10):
            result = Colour.BLACK

        else:
            result = Colour.WHITE

        return result

    def circle(self, x0, y0, radius, colour):
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius

        if (self.
                _penSolid == False):
            self.point(x0, y0 + radius, colour)
            self.point(x0, y0 - radius, colour)
            self.point(x0 + radius, y0, colour)
            self.point(x0 - radius, y0, colour)

            while (x < y):
                if (f >= 0):
                    y -= 1
                    ddF_y += 2
                    f += ddF_y

                x += 1
                ddF_x += 2
                f += ddF_x

                self.point(x0 + x, y0 + y, colour)
                self.point(x0 - x, y0 + y, colour)
                self.point(x0 + x, y0 - y, colour)
                self.point(x0 - x, y0 - y, colour)
                self.point(x0 + y, y0 + x, colour)
                self.point(x0 - y, y0 + x, colour)
                self.point(x0 + y, y0 - x, colour)
                self.point(x0 - y, y0 - x, colour)
        else:
            while (x < y):
                if (f >= 0):
                    y -= 1
                    ddF_y += 2
                    f += ddF_y

                x += 1
                ddF_x += 2
                f += ddF_x

                self.line(x0 + x, y0 + y, x0 - x, y0 + y, colour)  # bottom
                self.line(x0 + x, y0 - y, x0 - x, y0 - y, colour)  # top
                self.line(x0 + y, y0 - x, x0 + y, y0 + x, colour)  # right
                self.line(x0 - y, y0 - x, x0 - y, y0 + x, colour)  # left

            self.setPenSolid(True)
            self.rectangle(x0 - x, y0 - y, x0 + x, y0 + y, colour)

    def dLine(self, x0, y0, dx, dy, colour):
        self.line(x0, y0, x0 + dx - 1, y0 + dy - 1, colour)

    def line(self, x1, y1, x2, y2, colour):
        if ((x1 == x2) and (y1 == y2)):
            self.point(x1, y1, colour)

        elif (x1 == x2):
            if (y1 > y2):
                (y2, y1) = (y1, y2)  # swap

            for y in range(y1, y2+1):
                self.point(x1, y, colour)

        elif (y1 == y2):
            if (x1 > x2):
                (x2, x1) = (x1, x2)  # swap

            for x in range(x1, x2+1):
                self.point(x, y1, colour)

        else:
            wx1 = x1
            wx2 = x2
            wy1 = y1
            wy2 = y2

            flag = abs(wy2 - wy1) > abs(wx2 - wx1)
            if (flag):
                (wy1, wx1) = (wx1, wy1)  # swap
                (wy2, wx2) = (wx2, wy2)  # swap

            if (wx1 > wx2):
                (wx2, wx1) = (wx1, wx2)  # swap
                (wy2, wy1) = (wy1, wy2)  # swap

            dx = wx2 - wx1
            dy = abs(wy2 - wy1)
            err = dx / 2

            if (wy1 < wy2):
                ystep = 1
            else:
                ystep = -1

            while (wx1 <= wx2):
                if (flag):
                    self.point(wy1, wx1, colour)
                else:
                    self.point(wx1, wy1, colour)

                err -= dy
                if (err < 0):
                    wy1 += ystep
                    err += dx

                wx1 += 1

    def setPenSolid(self, flag=True):
        self._penSolid = flag

    def rectangle(self, x1, y1, x2, y2, colour):
        if (self._penSolid == False):
            self.line(x1, y1, x1, y2, colour)
            self.line(x1, y1, x2, y1, colour)
            self.line(x1, y2, x2, y2, colour)
            self.line(x2, y1, x2, y2, colour)

        else:
            if (x1 > x2):
                (x2, x1) = (x1, x2)  # swap

            if (y1 > y2):
                (y2, y1) = (y1, y2)  # swap

            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    self.point(x, y, colour)

    def dRectangle(self, x0, y0, dx, dy, colour):
        self.rectangle(x0, y0, x0 + dx - 1, y0 + dy - 1, colour)

    # Touch functions
    def getTouchInterrupt(self):
        return (self.touchINT.value() == 0)

    def getTouch(self):
        _number = bytearray(1)

        try:
            self._i2c.writeto(self._i2cAddress, bytes([0x10]))
            self._i2c.readfrom_into(self._i2cAddress, _number)
        except:
            _number = [0]

        x0 = 0
        y0 = 0
        z0 = 0
        t0 = 0

        if (_number[0] > 0):
            bufferRead = bytearray(5)
            self._i2c.writeto(self._i2cAddress, bytes([0x11]))
            self._i2c.readfrom_into(self._i2cAddress, bufferRead)

            _status = bufferRead[0]
            x0 = (bufferRead[1] << 8) + bufferRead[2]
            y0 = (bufferRead[3] << 8) + bufferRead[4]

            if (_status & 0x80):  # touch
                if (self._touchPrevious != touchEvent.NONE):
                    t0 = touchEvent.MOVE
                else:
                    t0 = touchEvent.PRESS

                # Keep position for next release
                self._touchPrevious = touchEvent.PRESS
                self._touchX = x0
                self._touchY = y0

            else:
                t0 = touchEvent.RELEASE

            z0 = 0x16

        elif (self._touchPrevious != touchEvent.NONE):
            # Take previous position for release
            self._touchPrevious = touchEvent.NONE
            t0 = touchEvent.RELEASE
            x0 = self._touchX
            y0 = self._touchY
            z0 = 0x16

        elif (self._touchPrevious == touchEvent.NONE):
            t0 = touchEvent.NONE
            z0 = 0

        x = 0
        y = 0
        z = z0
        t = t0

        if (z > 0x10):
            x0 = self.__checkRange(x0, self._touchXmin, self._touchXmax)
            y0 = self.__checkRange(y0, self._touchYmin, self._touchYmax)

            if (self._orientation == 0):  # ok
                x = self.__mapValue(x0, self._touchXmin, self._touchXmax,
                                    0, self._screenSizeH)
                y = self.__mapValue(y0, self._touchYmin, self._touchYmax,
                                    0, self._screenSizeV)

            elif (self._orientation == 1):  # ok
                x = self.__mapValue(y0, self._touchYmin, self._touchYmax,
                                    0, self._screenSizeV)
                y = self.__mapValue(x0, self._touchXmin, self._touchXmax,
                                    self._screenSizeH, 0)

            elif (self._orientation == 2):  # ok
                x = self.__mapValue(x0, self._touchXmin, self._touchXmax,
                                    self._screenSizeH, 0)
                y = self.__mapValue(y0, self._touchYmin, self._touchYmax,
                                    self._screenSizeV, 0)

            elif (self._orientation == 3):  # ok
                x = self.__mapValue(y0, self._touchYmin, self._touchYmax,
                                    self._screenSizeV, 0)
                y = self.__mapValue(x0, self._touchXmin, self._touchXmax,
                                    0, self._screenSizeH)

            return True, x, y, z, t

        else:
            return False, 0, 0, 0, 0

    def clearTouch(self):
        while (self.getTouchInterrupt()):
            time.sleep(0.010)

    # Font functions
    def setFontSolid(self, flag):
        self._fontSolid = flag

    def selectFont(self, font):
        if (font < Font.MAX_FONT_SIZE):
            self._fontSize = font
        else:
            self._fontSize = Font.MAX_FONT_SIZE - 1

        if (self._fontSize == 0):
            # kind, height, maxWidth, first, number
            self._font.kind = 0x40
            self._font.height = 8
            self._font.maxWidth = 6
            self._font.first = 32
            self._font.number = 224

        elif (self._fontSize == 1):
            self._font.kind = 0x40
            self._font.height = 12
            self._font.maxWidth = 8
            self._font.first = 32
            self._font.number = 224

        elif (self._fontSize == 2):
            self._font.kind = 0x40
            self._font.height = 16
            self._font.maxWidth = 12
            self._font.first = 32
            self._font.number = 224

        elif (self._fontSize == 3):
            self._font.kind = 0x40
            self._font.height = 24
            self._font.maxWidth = 16
            self._font.first = 32
            self._font.number = 224

    def getFont(self):
        return self._fontSize

    def fontMax(self):
        return Font.MAX_FONT_SIZE

    def characterSizeX(self, character):
        return self._font.maxWidth + self._fontSpaceX

    def characterSizeY(self):
        return self._font.height

    def stringSizeX(self, text: str):
        return len(text) * self._font.maxWidth

    def stringLengthToFitX(self, text: str, pixels):
        # Monospaced font
        index = pixels / self._font.maxWidth - 1
        if (index > len(text)):
            index = len(text)

        return index

    def setFontSpaceX(self, number):
        self._fontSpaceX = number

    def setFontSpaceY(self, number):
        self_fontSpaceY = number

    def __getCharacter(self, character, index):
        if (self._fontSize == 0):
            return Font._Terminal6x8e[character][index]

        elif (self._fontSize == 1):
            return Font._Terminal8x12e[character][index]

        elif (self._fontSize == 2):
            return Font._Terminal12x16e[character][index]

#         elif (self._fontSize == 3):
#             return Font._Terminal16x24e[character][index]

        else:
            return 0

    def gText(self, x0, y0, text: str, textColour=Colour.BLACK, backColour=Colour.WHITE):
        if (self._fontSize == 0):
            for k in range(0, len(text)):
                c = ord(text[k]) - ord(" ")

                for i in range(0, 6):
                    line = self.__getCharacter(c, i)

                    for j in range(0, 8):
                        if (self.__bitRead(line, j) > 0):
                            self.point(x0 + 6 * k + i, y0 + j, textColour)
                        elif (self._fontSolid):
                            self.point(x0 + 6 * k + i, y0 + j, backColour)

        elif (self._fontSize == 1):
            for k in range(0, len(text)):
                c = ord(text[k]) - ord(" ")

                for i in range(0, 8):
                    line = self.__getCharacter(c, 2 * i)
                    line1 = self.__getCharacter(c, 2 * i + 1)

                    for j in range(0, 8):
                        if (self.__bitRead(line, j)):
                            self.point(x0 + 8 * k + i, y0 + j, textColour)
                        elif (self._fontSolid):
                            self.point(x0 + 8 * k + i, y0 + j, backColour)

                        if (self.__bitRead(line1, j)):
                            self.point(x0 + 8 * k + i, y0 + 8 + j, textColour)
                        elif ((self._fontSolid) and (j < 4)):
                            self.point(x0 + 8 * k + i, y0 + 8 + j, backColour)

        elif (self._fontSize == 2):
            for k in range(0, len(text)):
                c = ord(text[k]) - ord(" ")

                for i in range(0, 12):
                    line = self.__getCharacter(c, 2 * i)
                    line1 = self.__getCharacter(c, 2 * i + 1)

                    for j in range(0, 8):
                        if (self.__bitRead(line, j)):
                            self.point(x0 + 12 * k + i, y0 + j, textColour)
                        elif (self._fontSolid):
                            self.point(x0 + 12 * k + i, y0 + j, backColour)

                        if (self.__bitRead(line1, j)):
                            self.point(x0 + 12 * k + i, y0 + 8 + j, textColour)
                        elif (self._fontSolid):
                            self.point(x0 + 12 * k + i, y0 + 8 + j, backColour)

#         elif (self._fontSize == 3):
#             for k in range(0, len(text)):
#                 c = ord(text[k]) - ord(" ")
# 
#                 for i in range(0, 16):
#                     line = self.__getCharacter(c, 3 * i)
#                     line1 = self.__getCharacter(c, 3 * i + 1)
#                     line2 = self.__getCharacter(c, 3 * i + 2)
# 
#                     for j in range(0, 8):
#                         if (self.__bitRead(line, j)):
#                             self.point(x0 + 16 * k + i, y0 + j, textColour)
#                         elif (self._fontSolid):
#                             self.point(x0 + 16 * k + i, y0 + j, backColour)
# 
#                         if (self.__bitRead(line1, j)):
#                             self.point(x0 + 16 * k + i, y0 + 8 + j, textColour)
#                         elif (self._fontSolid):
#                             self.point(x0 + 16 * k + i, y0 + 8 + j, backColour)
# 
#                         if (self.__bitRead(line2, j)):
#                             self.point(x0 + 16 * k + i, y0 +
#                                        16 + j, textColour)
#                         elif (self._fontSolid):
#                             self.point(x0 + 16 * k + i, y0 +
#                                        16 + j, backColour)

