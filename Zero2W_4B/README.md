# Pervasive Displays Library Suite - Touch - Python Edition for Raspberry Pi Zero 2W or 4B

This is an experimental port of the [Pervasive Displays Library Suite](https://github.com/rei-vilo/PDLS_EXT3_Basic_Touch) to Python on the Raspberry Pi Pico and Raspberry Pi Zero 2W or 4B.

---

The Pervasive Displays Library Suite is specifically designed for the [Pervasive Displays](https://www.pervasivedisplays.com) e-paper screens and EXT3 extension board.

![](https://pdls.pervasivedisplays.com/userguide/img/Logo_PDI_text_320.png)

The **PDLS\_EXT3\_Python\_Touch** provides a high-level interface to drive the [E-paper Pico Development Kit 2.71"-Touch (EPDK-271-Touch)](https://www.pervasivedisplays.com/product/touch-expansion-board-ext3-touch/#tab-3) and the [EXT3-Touch with 3.70" Touch EPD](https://www.pervasivedisplays.com/product/touch-expansion-board-ext3-touch/#tab-2).

The EPDK-271-Touch includes

+ iTC 2.7" e-paper screen with embedded fast update and capacitive touch;
+ [EPD Extension Kit Gen 3 (EXT3 or EXT3-1)](https://www.pervasivedisplays.com/product/epd-extension-kit-gen-3-EXT3/);
+ [Touch Expansion Board for EXT3 (EXT3-Touch)](https://www.pervasivedisplays.com/product/touch-expansion-board-ext3-touch/); 
+ [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) board;
+ cables; 
+ nuts, bolts and spacers.

## Features

+ Graphics routines
+ Text routines
+ Fast update
+ Touch management
+ GUI with button and text
+ Four extended fonts
+ Go to the [documentation](https://rei-vilo.github.io/PDLS_EXT3_Basic_Documentation/index.html) 

## Installation

Software

+ [Python](https://www.python.org/downloads/) release 3.9.2
+ [Adafruit Platform Detect](https://github.com/adafruit/Adafruit_Python_PlatformDetect) package, release 3.39.0
+ [Adafruit Blinka](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi#update-your-pi-and-python-2993452) package, release 8.2.1
+ [PDLS_EXT3_Python_Touch](https://github.com/rei-vilo/PDLS_EXT3_Python_Touch) package, release 6.0.9

Hardware

+ Pervasive Displays [E-paper Pico Development Kit 2.71"-Touch (EPDK-271-Touch)](https://www.pervasivedisplays.com/product/touch-expansion-board-ext3-touch/#tab-3)
+ [Connecting the Pervasive Displays e-Paper EPD Extension Kit Gen 3](https://embeddedcomputing.weebly.com/connecting-the-e-paper-epd-extension-kit-gen-3.html)
+ Tested on [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) and [Raspberry Pi 4B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)

Please refer to the Jupyter notebooks for the [installation](./Notebook%20-%20Installation.ipynb), an interactive [first example](./Notebook%20-%20First%20Example.ipynb) and the list of [other examples](./examples/Notebook%20-%20Other%20Examples.ipynb).

## Notes

1. The version for the Zero 2W or 4B relies on Python and the Adafruit Blinka library. 

1. Even with the powerful CPUs of the Raspberry Pi Zero 2 W and 4B, and SPI speed set at 8 MHz, the refresh process in fast mode is very slow (about 2 seconds), compared to less than a second in C++ (about 700 ms).

## Licence

**Copyright** &copy; Rei Vilo, 2010-2023

**Licence** [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](./LICENCE.md)

![](./by-nc-sa.svg)

