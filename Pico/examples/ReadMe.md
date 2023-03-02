# Examples

## Quick example

If **PDLS\_EXT3\_Python\_Touch** has been copied into the Raspberry Pi Pico, 

+ `Connect the Raspberry Pi Pico to the computer;
+ Open a **REPL** window on the Raspberry Pi;
+ Run the following example

```
MicroPython v1.19.1-837-g67fac4ebc on 2023-01-24; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> 
>>> from PDLS_EXT3_Python_Touch import *
>>> 
>>> myScreen = Screen()
>>> myScreen.begin()
>>>
>>> myScreen.setOrientation(7)
>>>
>>> myScreen.selectFont(myScreen.fontMax())
>>> myScreen.gText(10, 1O, myScreen.WhoAmI())
>>> myScreen.flush()
>>> myScreen.regenerate()
>>>
```

## Notes

Explicit version of the first line `from PDLS_EXT3_Python_Touch import *` could be `from PDLS_EXT3_Python_Touch import Colour, Font, Screen, Update, time`.

Similarly for the GUI example, `from hV_GUI import *` could be replaced by `from hV_GUI import Check, State, GUI, Text, Button`.

## List of examples

The examples are under the `examples` folder.

Common examples

+ `Common_Colours.py`
+ `Common_Fonts.py`
+ `Common_Forms.py`
+ `Common_Orientation.py`
+ `Common_Text.py`
+ `Common_WhoAmI.py`

Fast update example

+ `Example_Fast_Line.py`

Touch examples

+ `Basic_Touch_Draw.py`
+ `Basic_Touch_GUI.py`
+ `Basic_Touch_TicTacToe.py`
