# Pervasive Displays Library Suite - Touch - Python Edition for Raspberry Pi Pico 

This is an experimental port of the [Pervasive Displays Library Suite](https://github.com/rei-vilo/PDLS_EXT3_Basic_Touch) to Python on the Raspberry Pi Pico and Raspberry Pi Zero 2W or 4B.

---

The Pervasive Displays Library Suite is specifically designed for the [Pervasive Displays](https://www.pervasivedisplays.com) e-paper screens and EXT3 extension board.

![](https://pdls.pervasivedisplays.com/userguide/img/Logo_PDI_text_320.png)

The **PDLS\_EXT3\_Python\_Touch** provides a high-level interface to drive the [E-paper Pico Development Kit 2.71"-Touch (EPDK-271-Touch)](https://www.pervasivedisplays.com/product/touch-expansion-board-ext3-touch/#tab-3), which includes

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

+ Install [MicroPython v1.19.1](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) from Raspberry Pi;
+ Launch the [Thonny](https://thonny.org) IDE;
+ Copy the content of the `Pico` subfolder of the `PDLS_EXT3_Python_Touch` library into the Raspberry Pi Pico.

Hardware

+ Pervasive Displays [E-paper Pico Development Kit 2.71"-Touch (EPDK-271-Touch)](https://www.pervasivedisplays.com/product/touch-expansion-board-ext3-touch/#tab-3)
+ [Connecting the Pervasive Displays e-Paper EPD Extension Kit Gen 3](https://embeddedcomputing.weebly.com/connecting-the-e-paper-epd-extension-kit-gen-3.html)
+ Tested on [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)

## Notes

1. Contrary to the version for the Zero 2W or 4B, the version for the Pico does not rely on the Blinka library due to its overhead. Instead, it uses the offcial MicroPython version from Raspberry Pi. 

1. Even when the RP2040 is overclocked at 240 MHz and SPI speed set at 8 MHz, the refresh process in fast mode is very slow (about 2 seconds), compared to less than a second in C++ (about 700 ms).

1.  Due to Pico limited size of Flash and RAM, only three fonts are provided. Adding the fourth one raises an memory overflow error.

1.  Memory can be tracked with `gc`.

```
# Memory
import gc
print("Before", gc.mem_free())
gc.collect()
print("After", gc.mem_free())
```

## Licence

Copyright &copy; Rei Vilo, 2010-2023

Licence [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](./LICENCE.md)

![](./by-nc-sa.svg)

