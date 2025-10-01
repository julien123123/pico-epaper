import time
from machine import Pin, SPI
from uEPD import EPD1IN54, EPD2IN9, EPD3IN7, EPD4IN2
import freemono45H as font

"""
This file is inteded to show you all the basic patterns in fill(), inverted and not inverted.
"""

RST = Pin(27)
CS = Pin(1)
DC = Pin(26)
BUSY = Pin(28)
SCK = Pin(2)
MOSI = Pin(3)

epdSPI = SPI(0, sck=SCK, mosi=MOSI, miso=4)
#epd = EPD1IN54(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
#epd = EPD2IN9(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
#epd = EPD3IN7(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)
epd = EPD4IN2(rotation=0, spi=epdSPI, cs_pin=CS, dc_pin=DC, reset_pin=RST, busy_pin=BUSY)

f_h = epd.draw.txtheight(font)  # Font height
square_size = 64  # Each pattern square is 64x64 pixels

# Calculate how many pairs of squares fit horizontally and vertically
row_w = epd.width // (square_size * 2)  # Pairs of squares (normal + inverted)
row_h = epd.height // (square_size + f_h + 6)  # Add padding for text and spacing

# Calculate spacing to center the grid
h_spacing = (epd.width - row_w * square_size * 2) // (row_w + 1)
v_spacing = (epd.height - row_h * (square_size + f_h + 6)) // (row_h + 1)
pattern_i = 2

def make_pattern(row, column, h_spacing, v_spacing, cursor):
    for i in range(row):
        for e in range(column):
            if cursor >= 24:
                break
            # Calculate base position for each pair
            base_x = h_spacing + (square_size * 2 + h_spacing) * e
            base_y = v_spacing + (square_size + f_h + 6 + v_spacing) * i
            # Draw text label
            epd.draw.text(f"{cursor}", font, base_x, base_y, 0)
            # Draw normal square
            epd.draw.fill(base_x, base_y + f_h + 3, square_size, square_size, c=cursor, invert =False, key=0)
            # Draw inverted square
            epd.draw.fill(base_x + square_size, base_y + f_h + 3, square_size, square_size, c=cursor, invert=True, key = 0)
            cursor += 1
    epd.show(full = True)
    epd.sleep()
    time.sleep(20)
    return cursor

while pattern_i < 24:
    epd.reinit()
    pattern_i = make_pattern(row_h, row_w, h_spacing, v_spacing, pattern_i)

print("Here you go!")
