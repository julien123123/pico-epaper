# Epd Classes
```python
from machine import Pin, SPI
import Epd4IN2
epdspi = SPI(2, sck=Pin(12), mosi=Pin(11), miso=None) #Spi object, miso is not needed
epd = Epd4IN2(rotation=0, spi=epdSPI, cs_pin=Pin(7), dc_pin=Pin(5), reset_pin=Pin(15), busy_pin=Pin(16), hold = False)
```
### Constructor arguments:
- `rotation: int` accepts 0, 90, 180, 270 degrees. 0 degress is always in the orientation where the driver chip is at the bottom
- `spi` SPI object. Most modules don't have a miso pin. If your mcu doesn't accept None, just use an unused pin.
- `cs_pin`, `dc_pin`, `reset_pin`, `busy_pin` accept machine.Pin objects. They are the pins you are using from your Eink modules to your microcontroller.
- `hold`[*bool*, default = *True*] If true, ram in epd IC will be retained.
>[!TIP]
> Sometimes the pins on your module might not be named the same as my module. For example, `SCK` might be named `SCL`, `MOSI`
> might be named `SDA` or `DAT`

## Methods
### __Call\__ (dispay modes)
```python
epd(nbuf = 1, mode = None, pingpong = None, hold = None) # put display in partial mode.
```
Enables different update modes for the display. Use it by calling the name of your instance and adding the parameters in parentheses.

- `pingpong` allows fot the use of 2 buffer interchangeably. each time you use the show() method, the image in red ram goes in bw ram and goes on screen. The images are conserved on the ram.
    - in partial mode, pingpong = True, will allow for sequential updates without having to send the differential image every time.
    - If the red buffer remains unchanged, and you want to cycle through both buffers, just use `show_ram()`.

- `nbuf` is the number of buffers you want to use. 1 is the default value. 1 in full mode is more economical. In partial mode, may want to use 2 for differential updates, or if you want to control ping pong as 2 interchangeable buffers. Otherwise, if pingpong is true, you can use 1 buffer, and the display should erase the last every time. If you want black on white, you will need to diff buffer, so use 2.
  - Shades of grey mode will automatically use 2 buffers.
  - In full mode, if you use 2 buffers, bw ram will show white as opaque and black as transparent. Red ram will show black as opaque and white as transparent. The red ram will show images normally within what is black in the bw ram. That's why in 1 buffer mode, the red ram is voided.

- `mode`[*mode*, default = current mode (*None*)] this gives you a choice between [whatever you choose to name your instance, in this case epd]. any of these modes:
  - [instance].norm : normal full refresh updates
  - [instance].quick: 1 flash update, not the same as partial, but not as many flashes as norm
  - [instance].part: very quick, no flash updates to a part of the display
  - [instance].gray4: 4 shades of grey, from white to black mode; more flashes than norm.

> [!NOTE]
> When you call this method, only change the parameters you need. All the other parameters will be set from the epd attributes.

### Ping pong usage example:

```python
import time
import freesans20

epd(nbuf=2, mode = epd.part, pingpong=True)
epd.draw.text(text="Welcome to my EPD", font=freesans20, x=20, y=20)
epd.show()
epd.draw.text(text="SEND NUDES", font=freesans20, x=20, y=20, diff=True)
epd.show_ram()
time.sleep(3)
epd.show_ram()
time.sleep(2)
epd.show_ram()
epd.sleep()
```

## Show()
```python
import freesans20

epd.draw.rect(x=0, y = 10, w = 40, h = 10, f = True)
epd.show(full = True, flush = False, k = -1, clear = False) # Send a full buffer to the display, but keep the draw lineup in memory.
epd.draw.text('hello',freesans20, 10, 11, c=1, invert = False) # Draw text
epd.show() # just perform a normal show(). The draw lineup will be flushed after this.
```
Sends current frame buffer to screen and start refresh cycle.

- `flush`[*bool*, defaults to *True*] empties the list of object to be drawn the display. 

- `key`[*int*, defaults to *-1*] the number is equal to the color that will be transparent. -1 means no transparency at all

- `clear`[*bool*, defaults to *False*] will clear the ram before sending the buffer to the display. If it is set to False, and Full is False, all images sent to the display will be retained between refreshes.

- `full`[*bool*, defaults to *False*] Will send a whole buffer to the display, essentially erasing the last one. It takes more memory

>[!TIP]
> Calling just `epd.show()` will perform an update to the specified display area. You don't always need to use parameters

## Sleep()
```python
epd.sleep(ram_on = True) # Send epd to sleep, but keep the ram
```
Puts display in sleep mode.
- `ram_on`[*bool*, defaults to *False*] will keep the ram on while sleeping. This will drain a bit more current. If True, the display will discard its ram. You may initiate the display with hold = True if you plan on keeping the memory and have your microcontroller go in a deepsleep mode
### Example with light sleep and maintaining ram memory
```python
import freesans20, machine

epd.draw.text("12:34", freesans20, 20, 20)
epd.show()
epd.sleep(ram_on = True) # Sending epd to sleep with RAM on.
machine.lightsleep(5)
epd.reinit()
epd(partial = True, pingpong = True) # Puting the epd in partial mode
epd.draw.text("12:35", freesans20, 20, 20) 
epd.show()
epd.sleep()
```
>[!NOTE]
> reinit must be called everytime you want to re-use the display after sleep.

## invert_ram()
```python
epd.invert_ram(bw=True, red=True)
```
Inverts the bits in the selected display ram (both are by default)
## clear()
This method clears the display without any additional setup

## reinit()
Reinits the display. Must be used after sleep().
- reinit will take hold parameter and the current mode in consideration everytime. To change it, you must use the __call__ function
## show_ram()
```python
import freesans20

epd.draw.rect(0,0, 60, 30, c=0)
epd.draw.text('12:34', freesans20, 20, 10)
epd.draw.send_to_disp(key = 0) # send current draw buffer to the display

epd.draw.rect(100, 0, 30, 30, c=0)
epd.draw.text('23°C', freesans20, 102, 2)
epd.draw.send_to_disp(key = 0) # Send this other section
epd.shop_ram() # Show everything together
epd.sleep()
```
Triggers an update sequence from display ram. This allows to draw sections of the screen asychronously. Be aware that there won't be transparency between the sections themselves. 

# Direct Draw

This module mirors micropython's framebuf methods, but it's been optimized to work with specifically e-papers, deepsleep, 
and micropython native/viper. If you don't need to update the whole display every time, it will use way less ressources 
too (I mean, that's my goal). For example, if you are making a clock, and you have to wake up your microcontroller every 
minute, you can just make it draw the number you need without having to deal with a large bytearray. This can be quite 
quick.
>[!TIP]
> This library gives you a lot of options for dynamically showing shapes created from scratch, which can be useful for
> actually coming up with your program. When you are further in development, it's a good idea to pre-render as much graphics
> as possible using the `export()` function for example. You can also process fonts directly through [font_to_py](https://github.com/peterhinch/micropython-font-to-py/tree/master), or using
> quick functions to apply patterns for example.

## Diff parameter
- `diff` [*bool*, defaults to *False*] parameter: you can use this parameter along with those methods to send the drawn object directly to the red ram 
of the display. In partial mode with BW2B, the black drawings sent to the red buffer that are white in bw ram will turn 
white after show(). If you activate ping pong mode, drawings where diff=True will update the buffer part by part saved in
red ram. Upon show(), the buffer in the red ram will be shown, and the one that was in bw ram will go in the red ram to be
modified.
## Drawing Methods
>[!NOTE]
> In order to use the following methods, you must call you epd object, and then add .draw.*the method of your choosing* after it.
### 1. fill(x = None, y = None, w =None, h = None, c = 1, key=-1, invert = False, diff = True)
Special DirectDraw function. It is used to fill the background of the buffers.
- `c`[_int_, defaults to _1_] 0 or 1 determines the background of the buffers. 1 is always the default. if `diff` is False, This will change the background in the black and white RAM, if it's True, it will change de background in the red RAM.
  - Values between 2 and 23 will fill the buffer determined by the diff keyword with a pattern. In normal updates, 2 buffers mode, the black (0s) in the bw RAM will be transparent. Filling red RAM with a pattern will change the color/pattern of what is on the be RAM.
- `x`, `y`. `w`, `h`[_int_] are the same as for rectangles. You can specify those values if you only want a portion of the display to be filled. For balck or white fill, use rectangle instead.
- `key`[_int_, defaults to _-1_] if you put the fill object on top of other objects, you can choose a color to make transparent by choosing either 1 or 2.
- `invert`[_bool_, defaults to _False_] Make True if you want to invert the color of the pattern.

```python
import freesans20
epd(2) # put epd in 2 buffer modes
epd.draw.fill(c = 2, diff = True)
epd.draw.ellipse(60,60, 20, 20, fill = True, c = 0)
epd.text("Hello you", freesans20, 50, 40, invert = False) # This will create white text over a black circle
epd.show() # Here the black will become the checkers pattern since the diff buffer will be filled with it
epd.sleep()
```

### 2. pixel(x, y, c=black, diff =False)
```python
epd.draw.pixel(0,1)
epd.show()
```
### 3. hline(x, y, w, c=black, diff = False)

horizontal line
- `w`[*int*] Width in int.

### 4. vline(x, y, h, c=black, diff = False)

vertical line
- `h`[*int*] height in int

### 5. line(x1, y1, x2, y2, c=black, diff = False)
Line between two points
### 6. rect(x, y, w, h, c=black, f=False, diff = False)
- `f`[*bool*, defaults to *False*] if True, will fill the rectangle
### 7. ellipse(x, y, xr, yr, c=black, f=False, m=15, diff = False)
```python
epd.draw.Ellipse(0,0,10, 20, c= 0, f = True)
epd.show()
```
- `m`[*int*, defaults to *15*] parameter lets you specify which quarter you want to be shown in binary. A full circle is 15 because 15 = 0b1111
- `f`[*bool*, defaults to *False*] if True, will fill the ellipse.
### 8. poly(coords, c=black, f=False)
Shape created by linking pre-defined points together. You might need to change the orders of the points to get the result you want.

-`coords`[*list of tuples*] list of points in tuples like so: [(x,y)]. There must be at least 3 in order to get a shape.

### 9. text(text, font, x, y, c=black, spacing = False, fixed_width = False, diff = False, invert = True, v_rev = True)
```python
import freesans20
epd.draw.text('Bonjour', freesans20, 20, 20)
epd.show()
```
`text()` uses [font_to_py.py fonts from Peter Hinch's library on GitHub](https://github.com/peterhinch/micropython-font-to-py/tree/master) I did not include default fonts because I didn't want to deal with de licenses.
- `text`[*str*] Your text string
- `font`[*font_to_py font*] 
- `spacing`[*int*, defaults to 0] parameter is for specifying spaces between characters.
- `fixed_width`[*int*, defaults to 0] is used if you want all characters to occupy the same amount of space. It can be easy if you need to do partial updates, and you will only have to change one character in a string like in a clock.
- `invert`[*bool*, defaults to *True*] Inverts the colour of the given font. Default Fonts_to_py fonts will appear as white on the display.
- `v_rev`[*bool*, defaults to *True*] Option to revert the byte order of your fonts when the display is in vertical orientation. Default Font_to_py fonts will not appear correctly if thet are sliced vertically.

> [!TIP]
> For faster rendering time, you can pre-invert the colour of your fonts, and pre-invert the bytes if your font is vertical.

### 10. blit(fbuf, x, y, key=-1, ram=RAM_RBW, reverse = False, invert = False, diff = False, reverse = False)
- `blit` will just send a pre-rendered buffer directly to the display
- `invert`[*bool*, defaults to *False*] Inverts the colour of the given buffer.
- `reverse` [*bool*, defaults to *False*] Option to revert the byte order of your buffer. This is espacially heplful if it doesn't display proprely in vertical orientation.
- This is the method you want to use if you need to use 'framebuf.Framebuffer'. You can create a FrameBuffer object, send it with blit, and use the 'show()' method to display it.
### Example with framebuf.FrameBuffer
```python
import framebuf

screen_div = bytearray((100+7)*50//8)
fb = framebuf.FrameBuffer(memoryview(screen_div), 100, 50, framebuf.MONO_HMSB)
fb.text('I love EPDs', 0, 0) # using a framebuffer draw method
epd.draw.blit(x = 100, y = 25, buf = screen_div, w = 100, h = 50)
epd.show() # This will update only the zone specified in the ram so you can have more than one framebuffer or use DirectDraw concurently
```
## Other Draw Methods
### export(full = False, flush = True, key = -1, bw = True, red = False)
Exports the current draw lineup.Same Params as show(), but will return the current buffer a tuple of the `red` and/pr `bw` buffer if either is True.

The tuples will be structured like so: (bw_buffer, width in bytes, height), (red_buffer, width in bytes, height)

*See show_ram example

### export_into(buff, full = False, flush = True, key = -1, bw = True, red = False)
Exports current draw lineup in specified buffer. If the buffer is smaller than the display buffer, you may have to run the function many times with parameter flush = False.
### send_to_disp(full = False, flush = True, key = -1)
Sends the buffers to the display without refreshing. This allows you to draw de display asynchronously.

The parameters are exactly the same as the show() method.

Use show_ram() to refresh the display when you are done.

>[!NOTE]
>  The display ram dont have any transparency, if you send a buffer to the display RAM, you override what was there before.

*See show_ram example
# Other examples

### Example in using partial update after sleep
```python
import freesans20, machine

# This is more useful if you microcontroller goes to sleep for long whiles and needs to keep its energy consumption low
epd.draw.text(text = "12:34", font =  freesans20, x = 20, y = 20)
epd.show()
epd.sleep()
time.sleep(1) # Here to simulate your mcu going to sleep
epd.reinit()
epd(nbuf = 2, mode = epd.part, pingpong = True) # Putting the epd in partial mode
epd.draw.text(text = "12:34", font = freesans20, x = 20, y = 20, diff = True) # Sending these pixels to differential to be erased if not black in main ram
epd.draw.text(text = "12:35", font = freesans20, x = 20, y = 20) # Sending actual image
epd.show()
epd.sleep
```
### Creating a new pattern
```python
from core.draw import Pattern

new_pattern = Pattern(*Pattern.append(b'\xaaU'), w = 1, h = 2) # This is the same as the checkers pattern
epd.draw.fill(c = 24) # This new pattern will be appended after the default ones
```
`Pattern.append()` returns the in an out of the main Pattern class bytearray. The patterns have to fit within 8bits bytes,
and the parameters `w` for width and `h` for height are the minimum amount of byte it takes for the pattern to repeat.
> [!TIP]
> Creating patterns directly in your ide is easier using binary notation like so `bytearray([0b00000000])`, or you can use
> an image editor that's able to export xbm files, and edit pixels in black and white.