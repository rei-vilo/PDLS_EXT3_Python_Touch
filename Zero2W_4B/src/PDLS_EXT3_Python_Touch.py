#
# @file PDLS_EXT3_Python_Touch.py
# @brief Driver for Pervasive Displays 2.70-Touch screen with EXT3-1 and EXT3-Touch boards
#
# @details Project Pervasive Displays Library Suite
# Port of PDLS_EXT3_Basic_Touch to Python
# @n Based on highView technology
#
# @author Rei Vilo
# @date 02 May 2023
# @version 609
#
# @copyright (c) Rei Vilo, 2010-2023
# @copyright Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
# @see https://creativecommons.org/licenses/by-nc-sa/4.0/
#

__copyright__ = "Copyright (C) 2010-2023 Rei Vilo"
__licence__ = "CC BY-NC-SA 4.0 - Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International"
__version__ = "6.0.9"

from hV_Fonts import Font
from hV_Screen import Colour, touchEvent, Screen, Screen_EPD
import time
