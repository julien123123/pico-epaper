from uEPD import EPD3IN7
import img.a_hederson1875 as henderson
from machine import Pin, SPI

SCK = Pin(12)
MOSI = Pin(13)
RST = Pin(2, Pin.OUT)
CS = Pin(10)
DC = Pin(9)
BUSY = Pin(11)

epdSPI = SPI(2, sck=SCK, baudrate=400000, mosi=MOSI, miso=None)  # SPI instance fpr E-paper display (miso Pin necessary for SoftSPI, but not needed)
epd = EPD3IN7(rotation=90, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
epd(mode=epd.gray4)

epd.draw.blit(0,0, henderson.bw, henderson.height, henderson.width)
epd.draw.blit(0,0, henderson.red, henderson.height, henderson.width, diff= True)
epd.show()
epd.sleep()
