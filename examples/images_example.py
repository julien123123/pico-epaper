from uEPD import EPD1IN54, EPD2IN9, EPD3IN7, EPD4IN2
import a_hederson1875 as henderson
from machine import Pin, SPI

RST = Pin(27)
CS = Pin(1)
DC = Pin(26)
BUSY = Pin(28)
SCK = Pin(2)
MOSI = Pin(3)

epdSPI = SPI(0, sck=SCK, mosi=MOSI, miso=4)
#epd = EPD1IN54(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY) # SPI instance fpr E-paper display (miso Pin necessary for SoftSPI, but not needed)
#epd = EPD2IN9(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
#epd = EPD3IN7(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
epd = EPD4IN2(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)

epd(2, mode=epd.gray4)

epd.draw.blit(0,0, henderson.bw, henderson.width, henderson.height, reverse=True)
epd.draw.blit(0,0, henderson.red, henderson.width, henderson.height, diff = True, reverse=True)
epd.show(full = True)
epd.sleep()
