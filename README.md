# Pervasive Displays Library Suite - Touch - Python Edition 

[![Release](https://img.shields.io/github/v/release/rei-vilo/PDLS_EXT3_Python_Touch)](https://github.com/rei-vilo/PDLS_EXT3_Python_Touch/releases) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/e7c079a51eaa494bacea1adade2574d9)](https://www.codacy.com/gh/rei-vilo/PDLS_EXT3_Python_Touch/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=rei-vilo/PDLS_EXT3_Python_Touch&amp;utm_campaign=Badge_Grade) [![GitHub issues](https://img.shields.io/github/issues/rei-vilo/PDLS_EXT3_Python_Touch)](https://github.com/rei-vilo/PDLS_EXT3_Python_Touch/issues) [![](https://img.shields.io/badge/-Documentation-blue)](https://rei-vilo.github.io/PDLS_EXT3_Basic_Documentation/html/index.html)

This is an experimental port of the [Pervasive Displays Library Suite](https://github.com/rei-vilo/PDLS_EXT3_Basic_Touch) to Python on the Raspberry Pi Pico and Raspberry Pi Zero 2W or 4B.

---

The Pervasive Displays Library Suite is specifically designed for the [Pervasive Displays](https://www.pervasivedisplays.com) e-paper screens and EXT3 extension board.

![](https://pdls.pervasivedisplays.com/userguide/img/Logo_PDI_text_320.png)

The **PDLS\_EXT3\_Python\_Touch** provides a high-level interface to drive the [E-paper Pico Development Kit 2.71"-Touch (EPDK-271-Touch)](https://www.pervasivedisplays.com/product/touch-expansion-board-ext3-touch/#tab-3) and the [EXT3-Touch with 3.70" Touch EPD](https://www.pervasivedisplays.com/product/touch-expansion-board-ext3-touch/#tab-2).

The EPDK-271-Touch includes

+ iTC 2.7" e-paper screen with embedded fast update and capacitive touch;
+ [EPD Extension Kit Gen 3 (EXT3-1)](https://www.pervasivedisplays.com/product/epd-extension-kit-gen-3-EXT3/);
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

For hardware, refer to

+ [Assembling the Pervasive Displays EXT3-Touch](https://embeddedcomputing.weebly.com/assembling-the-pervasive-displays-ext3-touch.html); and
+ [Connecting the EXT3 to the Raspberry Pi Pico](https://embeddedcomputing.weebly.com/connecting-the-ext3-to-the-raspberry-pi-pico.html).

![](Pico/EPDK-271-Touch.jpg)

For software, see the procedures on the respective folders for [Raspberry Pi Pico](./Pico/ReadMe.md) and [Raspberry Pi Zero 2W or 4B](./Zero2W_4B/ReadMe.md).

## Notes

+ Contrary to the version for the Zero 2W and Model 4B, the version for the Pico does not rely on the Blinka library due to its overhead. Instead, it uses the official MicroPython version from Raspberry Pi which includes access to the SPI and I&sup2;C ports and GPIOs. 

+ The refresh process is very slow with Python. Fast mode refresh takes 2 seconds, compared to 700 ms in in C++, even with the Model 4B, the RP2040 overclocked at 240 MHz, and SPI speed set at 8 MHz.

+ Due to the limited size of Flash and RAM on the Pico, only three fonts are provided. Adding the fourth one raises an memory overflow error.

+ Memory can be tracked with `gc`.

```
# Memory
import gc
print("Before", gc.mem_free())
gc.collect()
print("After", gc.mem_free())
```

## Licence

**Copyright** &copy; Rei Vilo, 2010-2023

**Licence** [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](./LICENCE.md)

![](./by-nc-sa.svg)

