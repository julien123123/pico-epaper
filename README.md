# Pico_ePaper Work in Progress!

<div align="center">

![HelloThere](img/hello.jpg)

</div>

### I am currently working on expanding functionalities of the original Pico ePaper library. I want to add support to as much display options as possible


The implementation of everything is still a work in progress as I keep discovering new things. It's complicated to make everything
fit together, so I have to make decisions, and it makes it hard to keep up to date with the documentation for now.
The display specific files probably have an example of what is currently working at the bottom of them.

### Here's the rest of the normal readme:

This module is a basic Micropython driver for GoodDisplay e-paper Displays often used by Waveshare, WeAct Studio, and others.
It supports grayscale mode, partial updates and allows setting screen rotation. My goal doing this was to support as much
options given by the driver chips as possible to the user. Along with the driver, this module also
provides a simple drawing API that can be used to draw basic shapes and text on the screen that makes use of the on display
ram, and micrypython's viper mode. This allows for faster drawing times, and drawing the display asynchronously. In addition,
you may still use the FrameBuffer class to draw on the display.

Here are the currently supported displays:
- 1.54" 200x200 with SSD1681 driver  GDEY0154D67
- 2.9" 296x128 with SSD1680 driver GDEY029T94
- 3.7" 540x960 with SSD1677 driver ED037TC1
- 4.2" 400x300 with SSD1683 driver GDEW042T2 / GY-E042A87 (no fast mode)

*If your display is not listed, you can try to use the driver for the closest resolution and driver. It may work, but it 
may not. Using the other epd files as a reference, you can try to make your own driver.

Also, I have only tested this module on ESP-32s, and RP2040, the library may not work as expected on other ports.

I'm in the process of creating the examples. The files are there, but you should rely more on the epd files for the time being

---
## Documentation

You can find all the documentations about how this library works [here](/docs.md)


---

## Installation

1. Copy your display's epd file and the core folder to your device's root directory. 
2. (optional) if you want to use text, download [Peter Hinch's Font_to_py utility](https://github.com/peterhinch/micropython-font-to-py/tree/master)