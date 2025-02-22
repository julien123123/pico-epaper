from functools import partial

# Epd Classes
```python
from machine import Pin, SPI
import Epd4IN2
epdspi = SPI(2, sck=Pin(12), mosi=Pin(11), miso=None) #Spi object, miso is not needed
epd = Epd4IN2(rotation=0, spi=epdSPI, cs_pin=Pin(7), dc_pin=Pin(5), reset_pin=Pin(15), busy_pin=Pin(16))
```
### Constructor arguments:
- `rotation: int` accepts 0, 90, 180, 270 degrees. 0 degress is always in the orientation where the driver chip is at the bottom
- `spi` SPI object. Most modules don't have a miso pin. If your mcu doesn't accept None, just use an unused pin.
- `cs_pin`, `dc_pin`, `reset_pin`, `busy_pin` accept machine.Pin objects. They are the pins you are using from your Eink modules to your microcontroller.
>[!TIP]
> Sometimes the pins on your module might not be named the same as my module. For example, `SCK` might be named `SCL`, `MOSI`
> might be named `SDA` or `DAT`

## Methods
### __Call\__ (dispay modes)
```python
epd(nbuf = 1, bw = True, partial = True, pingpong = True)
```

# Direct Draw

```python
epd.draw.Ellipse(10, 20, 0,0, c= 0, f = True)
```



### Example with framebuf.FrameBuffer
```python
import framebuf

screen_div = bytearray((100+7)*50//8)
fb = framebuf.FrameBuffer(memoryview(screen_div), 100, 50, framebuf.MONO_HMSB)
fb.text('I love EPDs', 0, 0) # using a framebuffer draw method
epd.draw.blit(x = 100, y = 25, buf = screen_div, w = 100, h = 50)
epd.show() # This will update only the zone specified in the ram so you can have more than one framebuffer or use DirectDraw concurently

```
### Example in using partial update after sleep
```python
import freesans20, machine

# This is more useful if you microcontroller goes to sleep for long whiles and needs to keep its energy consumption low
epd.draw.text(text = "12:34", font =  freesans20, x = 20, y = 20)
epd.show()
epd.sleep()
time.sleep(1) # Here to simulate your mcu going to sleep
epd.reinit()
epd(partial = True, pingpong = True) # Puting the epd in partial mode
epd.draw.text(text = "12:34", font = freesans20, x = 20, y = 20, diff = True) # Sending these pixels to differential to be erased if not black in main ram
epd.draw.text(text = "12:35", font = freesans20, x = 20, y = 20) # Sending actual image
epd.show()
epd.sleep
```
### Example with light sleep and maintaining ram memory
```python
import freesans20, machine

epd.draw.text("12:34", freesans20, 20, 20)
epd.show()
epd.sleep(ram_on = True) # Sending epd to sleep with RAM on.
machine.lightsleep(5)
epd(partial = True, pingpong = True) # Puting the epd in partial mode
epd.draw.text("12:35", freesans20, 20, 20) 
epd.show()
epd.sleep()

```
### Examples with ping pong

```python
import time
import freesans20

epd(nbuf=2, partial=True, pingpong=True)
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