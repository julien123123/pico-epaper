# Pico_ePaper Work in Progress!

<div align="center">

![HelloThere](img/hello.jpg)

</div>

I am currently working on expanding functionalities of the original Pico ePaper library. I want to add:

- Support for 2.9in epaper display
- Support for partial update after deepsleep
- Support for partial update on smaller parts of the display to save on resources
- Direct write to the display without having to use FrameBuffer or the Writer class, which is better for lower memory use, for slower mcus. It also uses less energy in the end
- support for 2 in display buffered screens, also good for slower mcus.
- support for white partial updates over black

The implementation of everything is still a work in progress as I keep discovering new things. It's complicated to make everything
fit together, so I have to make decisions, and it makes it hard to keep up to date with the documentation for now.
The display specific files probably have an example of what is currently working at the bottom of them.

Here's the rest of the normal readme:

This module is a basic driver for Waveshare [Pico e-Paper 3.7 display](https://www.waveshare.com/wiki/Pico-ePaper-3.7).
It supports grayscale mode and allows setting screen rotation. Drawing routines are compatible with
[MicroPython FrameBuffer](https://docs.micropython.org/en/latest/library/framebuf.html) class, which means the same
method names and arguments they require (**blit()** being a slight exception - see below for details).

There are two classes in this module:
1. Eink - uses SPI for communication with the display, can be used with devices other than RP2040.
2. EinkPIO - uses one State Machine and DMA channel to communicate with the display.

Both classes offer the same functionality and the only difference is the optional parameters in the constructor they take.

---

## Note (Eink only)
**show()** method takes considerably longer for rotations 90 and 270, than 0 and 180 (~700 ms vs 80 ms). This is normal and
is a result of additional data processing required before sending buffers to the screen in landscape mode.
There's also a significant memory overhead associated with the processing.
Currently, I have no solution to this problem, except using EinkPIO whenever possible.

#not in my version, but I'm not maintaining einkpio... so...

---

## Constructors
**Eink(rotation=0, spi=None, cs_pin=None, dc_pin=None, reset_pin=None, busy_pin=None, monochrome=True)**

Constructors for these classes take multiple optional arguments that allow setting desired rotation as well as custom
pin assignments.

Accepted values for rotation are: 0, 90, 180 and 270. Supplying unaccepted value will result in an error. The default
value is 0, i.e. screen is horizontal with USB connector facing upwards.

**Eink** class takes additional _spi_ argument that allows setting custom SPI object to be used, if not set it defaults
to SPI(1, baudrate=20_000_000).

By default, Pins setup reflects usage of the e-Paper display as a shield for Raspberry Pi Pico, but the user
can supply custom configuration for use with different boards and microcontrollers (tested with ESP-WROOM-32).

The optional parameter **use_partial_buffer** can be set to _True_ to use separate buffer for partial refreshes.
Otherwise, the BW buffer is used in partial mode.

---

## Public methods

___

### show(flush = True, key = -1)
Sends current frame buffer to screen and start refresh cycle.

'flush' empties the list of object to be drawn the display.
'key' the number is equal to the color that will be transparent. -1 means no transparency at all

---

### sleep()
Puts display in sleep mode.

---

### partial_mode_on(pingpong = False)
Enables partial updates mode.
'pingpong' allows fot the use of 2 buffer interchangeably. each time you use the show() method, the image in red ram goes in bw ram and goes on screen. The images are conserved on the ram.

---

### partial_mode_off()
Disables partial updates mode.

---

### invert_ram(bw=True, red=True)
Inverts the bits in the selected display ram (both are by default)

---

### clear()
This method clears the display without any additional setup

---

### reinit()
Reinits the display. Has to be used after sleep()

---

Additionally, the module has DirectDraw which is very similar to drawing methods found in FrameBuffer class:
1. fill(c=white)
2. pixel(x, y, c=black)
3. hline(x, y, w, c=black)
4. vline(x, y, h, c=black)
5. line(x1, y1, x2, y2, c=black)
6. rect(x, y, w, h, c=black, f=False)
7. ellipse(x, y, xr, yr, c=black, f=False, m=15)
- 'm' parameter lets you specify which quarter you want to be shown in binary. A full circle is 15 because 15 = 0b1111
8. poly(x, y, coords, c=black, f=False)
- not implemented yet
9. text(text, font, x, y, c=black, spacing = False, fixed_width = False, invert = True)
- 'text()' uses [font_to_py.py fonts from Peter Hinch's library on GitHub](https://github.com/peterhinch/micropython-font-to-py/tree/master) I did not include default fonts because I didn't want to deal with de licenses.
- 'spacing' parameter is for specifying spaces between characters.
- 'fixed_width' is used if you want all characters to occupy the same amount of space. It can be easy if you need to do partial updates, and you will only have to change one character in a string like in a clock.

> [!TIP]
> For faster rendering time, you can pre-invert the colour of your fonts, and pre-invert the bytes if your font is vertical.

10. blit(fbuf, x, y, key=-1, palette=None, ram=RAM_RBW)
- 'blit' will just send a pre-rendered buffer directly to the display
- This is the method you want to use if you need to use 'framebuf.Framebuffer'. You can create a FrameBuffer object, send it with blit, and use the 'show()' method to display it.

'diff' parameter: you can use this parameter along with those methods to send the drawn object directly to the red ram 
of the display. In partial mode with BW2B, the black drawings sent to the red buffer that are white in bw ram will turn 
white after show(). If you activate ping pong mode, drawings where diff=True will update the buffer part by part saved in
red ram. Upon show(), the buffer in the red ram will be shown, and the one that was in bw ram will go in the red ram to be
modified.

---

## Note
**blit()** method takes one additional keyword argument compared to the one found in FrameBuffer class - _ram_ - that
specifies the target buffer (and consequently RAM) the source will be drawn into. There are three possible values:
1. RAM_BW - black pixels from source will be rendered in light gray on screen.
2. RAM_RED - black pixels from source will be rendered in dark gray on screen.
3. RAM_RBW - black pixels from source will be rendered in black on screen.

(For RAM_BW and RAM_RED respective pixels in the other buffer are assumed to be white.)

---

---
