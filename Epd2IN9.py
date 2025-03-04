"""
# Epd2IN9 definitions
seq = breg[0:4] = b'\x03\x02\x00\x01'
clr_ram_blk = breg[4] = 0xe6
clr_ram_wt = breg[5] = 0xe5
gate_nb = breg[6:9] = b"'\x01\x00"
gate_v = breg[9] = 0xff
source_v = breg[10:13] = 255
st_vcom = breg[13] = 0xff
soft_start = breg[14:19] = 255
upd2_norm = breg[19] = 0xf7
lut_norm = breg[20] = 0xff
upd2_part = breg[21] = 0x1c
lut_part = breg[22] = 0xff
wr_temp_quick = breg[23] = 0x5a
ld_temp_quick = breg[24] = 0x91
upd2_quick = breg[25] = 0xc7
lut_quick = breg[26] = 0xff
wr_temp_gr = breg[27] = 0xff
ld_temp_gr = breg[28] = 0xff
upd2_gr = breg[29] = 0xf4
lut_gr = breg[30] = 0xff
breg = bytearray(b"\x03\x02\x00\x01\xe6\xe5'\x01\x00\xff\xff\x00\x00\xff\xff\x00\x00\x00\x00\xf7\xff\x1c\xffZ\x91\xc7\xff\xff\xff\xf4\xff")
"""

from core.Eink import Eink

class EPD2IN9(Eink):  # SSD1680
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11
    x_set = '2B'
    breg = b"\x03\x02\x00\x01\xe6\xe5'\x01\x00\xff\xff\x00\x00\xff\xff\x00\x00\x00\x00\xf7\xff\x1c\xffZ\x91\xc7\xff\xff\xff\xf4\xff"

    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 296
        self.ic_side = 128
        #self._seqs = b'\x03\x02\x00\x01'  # structure ( 0°, 90°, 180°, 270°)
        super().__init__(spi, *args, **kwargs)

    def _virtual_width(self, num=None):
        ''' returns width the way it is sent to the chip'''
        return self.width // 8 if num is None else 0 if num is 0 else  num // 8

if __name__ == "__main__":
    from machine import Pin, SPI
    p = Pin(2, Pin.OUT)
    epdSPI = SPI(2, sck=Pin(45), baudrate=400000, mosi=Pin(47), miso=0)
    epd = EPD2IN9(rotation=90, spi=epdSPI, cs_pin=Pin(3), dc_pin=Pin(29), reset_pin=p, busy_pin=Pin(5))