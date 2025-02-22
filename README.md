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
- 1.54" 200x200 with SSD1681 driver / GDEW0154M09
- 2.9" 296x128 with SSD1680 driver GDEH029A1
- 3.7" 540x960 with SSD1677 driver GDEW0371W7
- 4.2" 400x300 with SSD1683 driver GDEW042T2

*If your display is not listed, you can try to use the driver for the closest resolution and driver. It may work, but it 
may not. Using the other epd files as a reference, you can try to make your own driver.

Also, I have only tested this module on ESP-32s, and RP2040, the library may not work as expected on other ports.

---

## Note  **This is currently being evaluated
**show()** method takes considerably longer for rotations 90 and 270, than 0 and 180 (~700 ms vs 80 ms). This is normal and
is a result of additional data processing required before sending buffers to the screen in landscape mode.
There's also a significant memory overhead associated with the processing.


---

## Constructors
**Eink(rotation=0, spi=None, cs_pin=None, dc_pin=None, reset_pin=None, busy_pin=None, monochrome=True)**

Accepted values for rotation are: 0, 90, 180 and 270. Supplying unaccepted value will result in an error. The default
value is 0, i.e. screen is horizontal with USB connector facing upwards.

_spi_ argument that allows setting custom SPI object to be used

---

## Public methods

___

### show(full = False, flush = True, key = -1, clear = False)
Sends current frame buffer to screen and start refresh cycle.

`flush` empties the list of object to be drawn the display.

`key` the number is equal to the color that will be transparent. -1 means no transparency at all

`clear` will clear the ram before sending the buffer to the display. If it is set to False, and Full is False, all images sent to the display will be retained between refreshes.

`full` Will send a whole buffer to the display, essentially erasing the last one. It takes more memory

---

### draw.export(full = False, flush = True, key = -1, bw = True, red = False)
Same Params as show(), but will return the current buffer a tuple of the `red` and/pr `bw` buffer if either is True.

The tuples will be structured like so: (bw_buffer, width in bytes, height), (red_buffer, width in bytes, height)

---

### draw.send_to_disp(full= False, flush = True, key = -1)
Sends the buffers to the display without refreshing. This allows you to draw de display asynchronously.

The parameters are exactly the same as the show() method.

Use show_ram() to refresh the display when you are done.

>[!NOTE]
>  The display ram dont have any transparency, if you send a buffer to the display RAM, you override what was there before.

---

### sleep(ram_on = False)
Puts display in sleep mode.
- `ram_on` will keep the ram on while sleeping. This will use a bit more current.

---

### \__call__(nbuf = 1, bw = True, partial = False, pingpong = False)
Enables different update modes for the display. Use it by calling the name of your instance and adding the parameters in parentheses.

- `pingpong` allows fot the use of 2 buffer interchangeably. each time you use the show() method, the image in red ram goes in bw ram and goes on screen. The images are conserved on the ram.
    - in partial mode, pingpong = True, will allow for sequential updates without having to send the differential image every time.
    - If the red buffer remains unchanged, and you want to cycle through both buffers, just use `show_ram()`.

- `nbuf` is the number of buffers you want to use. 1 is the default value. 1 in full mode is more economical. In partial mode, may want to use 2 for differential updates, or if you want to control ping pong as 2 interchangeable buffers. Otherwise, if pingpong is true, you can use 1 buffer, and the display should erase the last every time. If you want black on white, you will need to diff buffer, so use 2.
  - Shades of grey mode will automatically use 2 buffers.
  - In full mode, if you use 2 buffers, bw ram will show white as opaque and black as transparent. Red ram will show black as opaque and white as transparent. The red ram will show images normally within what is black in the bw ram. That's why in 1 buffer mode, the red ram is voided.

- `partial` is for quick partial updates. if False, the display will be updated completely with the ram content.

- `bw` is false if you want to use shades of grey. Otherwise, set it to True.
  - in grey mode, all other options are False, and the display will use 2 buffers.
> [!NOTE]
> When you call this method, only change the parameters you need. All the other parameters will be set from the epd attributes.
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
- `m` parameter lets you specify which quarter you want to be shown in binary. A full circle is 15 because 15 = 0b1111
8. poly(x, y, coords, c=black, f=False)
- not implemented yet
9. text(text, font, x, y, c=black, spacing = False, fixed_width = False, invert = True)
- `text()` uses [font_to_py.py fonts from Peter Hinch's library on GitHub](https://github.com/peterhinch/micropython-font-to-py/tree/master) I did not include default fonts because I didn't want to deal with de licenses.
- `spacing` parameter is for specifying spaces between characters.
- `fixed_width` is used if you want all characters to occupy the same amount of space. It can be easy if you need to do partial updates, and you will only have to change one character in a string like in a clock.

> [!TIP]
> For faster rendering time, you can pre-invert the colour of your fonts, and pre-invert the bytes if your font is vertical.

10. blit(fbuf, x, y, key=-1, ram=RAM_RBW, reverse = False, invert = False)
- `blit` will just send a pre-rendered buffer directly to the display
- This is the method you want to use if you need to use 'framebuf.Framebuffer'. You can create a FrameBuffer object, send it with blit, and use the 'show()' method to display it.

`diff` parameter: you can use this parameter along with those methods to send the drawn object directly to the red ram 
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
