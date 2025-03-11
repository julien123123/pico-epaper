import time

from uEPD import EPD1IN54, EPD2IN9, EPD3IN7, EPD4IN2
import freemono45H as font

"""
This file is inteded to show you all the basic patterns in fill(), inverted and not inverted.
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

f_h = epd.draw.txtheight(font)
row_w = epd.width // 64
row_h = epd.height//(32 + f_h +1)
h_spacing = (epd.width - row_w * 64)//(row_w + 1 )
v_spacing = (epd.height - row_h *32)//(row_h + f_h + 3 + 1 )
pattern_i = 2

def make_pattern( row, column, h_spacing, v_spacing, cursor):
    for i in range(row):
        for e in range(column):
            if cursor >= 24:
                break
            base_x = h_spacing+(64+h_spacing)*e
            base_y = v_spacing+(v_spacing+32)*i
            epd.draw.text(f"{cursor}", font, base_x, base_y, 0)
            epd.draw.fill(base_x, base_y+ f_h +3, 32, 32, c = cursor)
            epd.draw.fill(base_x + 32 , base_y + f_h + 3, 32, 32, c = cursor, invert= True)
            cursor +=1
    epd.show()
    time.sleep(20)

while pattern_i > 24:
    epd.reinit()
    make_pattern(row_w, row_h, h_spacing, v_spacing, pattern_i)
    epd.sleep()

print("Here you go!")
