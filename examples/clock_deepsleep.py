from machine import SPI, Pin, deepsleep, DEEPSLEEP_RESET, wake_reason
import time
import freemono45H as font
from uEPD import EPD1IN54, EPD2IN9, EPD3IN7, EPD4IN2
"""
This is an example of using text, and also using partial update after you put your microcontroller in deepsleep.
To accelerate the process, you could always use deepsleep memory to store the last values to erase the upon waking form
deep sleep. I did not include it in this example as in micropython not all microcontroller have deepsleep memory implemented
in the same manner. You could also compute the position of each character to change only what has changed to accelerate
the process.
"""
RST = Pin(15)
CS = Pin(7)
DC = Pin(5)
BUSY = Pin(16)
SCK = Pin(12)
MOSI = Pin(11)

epdSPI = SPI(2, sck=SCK, mosi=MOSI, miso=None)
epd = EPD1IN54(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
#epd = EPD2IN9(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
#epd = EPD3IN7(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
#epd = EPD4IN2(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)

if wake_reason() is not DEEPSLEEP_RESET:
    epd.clear()
    #h, m = time.localtime()[3:5]
    h, m = 12, 34
    s = f"{h}:{m}"
    # calculating the center values for our string
    x = (epd.width - epd.draw.txtlen(s, font))//2
    y = (epd.height - epd.draw.txtheight(font))//2
    epd.draw.text(s, font, x, y, c = 0)
    epd.draw.fill(c = 6, diff = True) # giving the font a pattern this makes everything longer
    epd.show()
    epd.sleep()
    deepsleep(10)
else:
    # Putting the display in partial update mode with pingpong
    epd(2, mode = epd.part, pingpong = True)
    # Telling the display what to erase in the diff buffer
    h, m = 12, 34
    s = f"{h}:{m}"
    # calculating the center values for our string
    x = min(0,(epd.width - epd.draw.txtlen(s, font)) // 2)
    y = (epd.height - epd.draw.txtheight(font)) // 2
    epd.draw.text(s, font, x, y, c=0, diff = True)
    epd.draw.fill(c=6, key = 0, diff=True)
    m +=1
    # Drawing the new text
    epd.draw.text(f"{h}:{m}", font, x, y, c=0)
    epd.draw.fill(c=6, key=0)
    epd.show()
    epd.hold = True # Changing the "hold" attribute to maintain ram upon epd sleep.
    epd.sleep()

    time.sleep(5)
    epd.reinit()
    m = +1
    epd.draw.text(f"{h}:{m}", font, x, y, c=0)
    epd.draw.fill(c=6, key=0)
    epd.show()
    epd.hold = False # Releasing the hold on data
    epd.sleep()
    print("Here you go!")