"""
# Epd1In54 definitions
seq = breg[0:4] = b'\x03\x01\x00\x02'
clr_ram_blk = breg[4] = 0xe6
clr_ram_wt = breg[5] = 0xe5
gate_nb = breg[6:9] = b'\xc7\x00\x00'
gate_v = breg[9] = 0xff
source_v = breg[10:13] = 255
st_vcom = breg[13] = 0xff
soft_start = breg[14:19] = 255
upd2_norm = breg[19] = 0xf7
lut_norm = breg[20] = 0xff
upd2_part = breg[21] = 0xfc
lut_part = breg[22] = 0xff
wr_temp_quick = breg[23] = 0x64
ld_temp_quick = breg[24] = 0x91
upd2_quick = breg[25] = 0xc7
lut_quick = breg[26] = 0xff
wr_temp_gr = breg[27] = 0x5a
ld_temp_gr = breg[28] = 0x91
upd2_gr = breg[29] = 0xcf
lut_gr = breg[30] = 0xff
breg = bytearray(b'\x03\x01\x00\x02\xe6\xe5\xc7\x00\x00\xff\xff\x00\x00\xff\xff\x00\x00\x00\x00\xf7\xff\xfc\xffd\x91\xc7\xffZ\x91\xcf\xff')
"""

from core.Eink import Eink
from ustruct import pack

class EPD1IN54(Eink):  # SSD1681
    x_set = '2B'
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11
    breg = b'\x03\x01\x00\x02\xe6\xe5\xc7\x00\x00\xff\xff\x00\x00\xff\xff\x00\x00\x00\x00\xf7\xff\xfc\xffd\x91\xc7\xffZ\x91\xcf\xff\x01'

    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 200
        self.ic_side = 200
        #self._seqs = b'\x03\x01\x00\x02' # structure ( 0°, 90°, 180°, 270°) framebuf mode good vals (3, 6, 0, 5)
        super().__init__(spi, *args, **kwargs)

if __name__ == "__main__":
    from machine import Pin, SPI
    import core.draw_modes as md
    from core.draw import Drawable as DR
    import numr110H, numr110V,freesans20, freesans20V
    
    
    
    p= Pin(15, Pin.OUT)
    epdSPI = SPI(2, sck=Pin(12), mosi=Pin(11), miso=None)
    epd = EPD1IN54(rotation=0, spi=epdSPI, cs_pin=Pin(7), dc_pin=Pin(5), reset_pin=p, busy_pin=Pin(16))
    #epd.clear()
    
    big = numr110H if not epd._sqr else numr110V
    smol = freesans20 if not epd._sqr else freesans20V
    
    epd.draw.text("Jimme so les ptates!", smol, 0, 140, c=0)
    epd.draw.text('19', big, 20, 16, c = 0)
    epd.draw.rect(0,10,10,10, f = True, c =0)
    epd.show(key = 0)
    epd.sleep()
    epd.reinit()
    epd(2, mode = epd.part, pingpong=True)
    epd.draw.text('19', big, 20, 16, diff=True, c=0)
    epd.draw.text('WW', big, 20, 20, c=0)
    epd.show(True)

    epd(1, mode = epd.quick, pingpong = False)
    epd.reinit()
    import fantasmagorie as f
    epd.draw.blit(10,0, f.fantasmagorie,f.width,  f.height, reverse= True, invert = False)
    epd.show(clear=True)

    epd.sleep()