# works perfectly with direct draw when _partial even with the diffs
# works on a full update if full != True

from core.Eink import Eink
from ustruct import pack

class EPD1IN54(Eink):  # SSD1681
    x_set = '2B'
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11

    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 200
        self.ic_side = 200
        self._seqs = (0x03, 0x01, 0x00, 0x02) # structure ( 0°, 90°, 180°, 270°) framebuf mode good vals (3, 6, 0, 5)
        super().__init__(spi, *args, **kwargs)

    def _clear_ram(self, bw=True, red=True): 
        if red:
            self._send(0x46, 0xe5)
            self._read_busy()
        if bw:
            self._send(0x47, 0xe5)
            self._read_busy()

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("3B", 0xC7, 0x00, 0x00)) # Mirror if last bit == 0x01

    def _virtual_width(self, num=None):
        ''' returns width the way it is sent to the chip'''
        return self.width // 8 if num is None else 0 if num is 0 else  num // 8

    def _updt_ctrl_2(self):
        # Set Display Update Control 2 / loading LUTs
        if not self._partial:
            self._send(0x22, 0xf7)
        else:
            self._send(0x22, 0xff)
        self._read_busy()

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
    
    epd.draw.text("Jimme so les ptates!", smol, 0, 140)
    epd.draw.text('19', big, 20, 16, c = 1)
    epd.draw.rect(0,10,10,10, f = True, c =0)
    epd.show(key = 0)
    epd.sleep()

    epd.reinit()
    epd(2, True, True, True)
    epd.draw.text('19', big, 20, 16, diff=True, c=1)
    epd.draw.text('WW', big, 20, 20, c=1)
    epd.show(True)

    epd(1, True,False, False)
    epd.reinit()
    import fantasmagorie as f
    epd.draw.blit(10,0, f.fantasmagorie,f.width,  f.height, reverse= True, invert = True)
    epd.show(clear=True)

    epd.sleep()
    
    print(epd._abs_xy(0, 0))