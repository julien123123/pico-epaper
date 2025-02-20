from core.Eink import Eink
from ustruct import pack

# 0 deg hor part works and full, but draw_all doesn't work if it sends a full update

class EPD4IN2(Eink): #SSD1683 GDEY042T81 (not for the T2)
    x_set = '2B'
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11

    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 300
        self.ic_side = 400
        self._seqs = (0x03, 0x06, 0x00, 0x05)  # structure ( 0°, 90°, 180°, 270°) 3605 pour framebuf = parfait
        #self.x2 = True
        super().__init__(spi, *args, **kwargs)


    def _clear_ram(self, bw=True, red=True, black = False):
        col = 0x66 if black else 0xe6
        if red:
            self._send(0x46, col) #0x66 for black screen
            self._read_busy()
        if bw:
            self._send(0x47, col)
            self._read_busy()

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("hB", 299, 0x00)) #if second byte is 0x1 = mirror
        self._send(0x21, 0x00)

    def _virtual_width(self, num=None):
        ''' returns width the way it is sent to the chip'''
        return self.width // 8 if num is None else 0 if num is 0 else  num // 8

    def _updt_ctrl_2(self):
        # Set Display Update Control 2 / loading LUTs
        if not self._partial:
            self._send(0x22, 0xf7) #if not self.monoc else self._send(0x22, 0xcf)
        else:
            #self._send(0x1A, 0x6E)
            self._send(0x22, 0xff)
        self._read_busy()
if __name__ == "__main__":
    from machine import Pin, SPI
    import numr110H, numr110V, freesans20, time
    from core.draw import Drawable as DR
    
    p = Pin(27, Pin.OUT)
    epdSPI = SPI(0, sck=Pin(2), mosi=Pin(3), miso=None)
    epd = EPD4IN2(rotation=0, spi=epdSPI, cs_pin=Pin(1), dc_pin=Pin(26), reset_pin=p, busy_pin=Pin(28))
    
    epd.draw.text('3', numr110H, 0, 0, c = 1)
    epd.draw.rect(350,250,50,50)
    epd.show()
    epd.draw.ellipse(10,10, 40, 100)
    epd.show(clear=True)
    epd(2, bw= True, partial=True)
    manx = 6
    k=0
    epd.draw.rect(220, 30, 40, 40, f=True, c = 0)
    epd.draw.text('42:48', numr110H, manx,100)
    epd.draw.text(' Mercredi 20 dec 2025', freesans20, manx,2, c=1)

    epd.draw.ellipse(43, 30, 79, 80, f= False)

    epd.draw.show(key=k)
    epd(1, True, False, False)
    epd.sleep()
    
    # Yup, we are sleeping babe
    epd.reinit()
    epd(2, bw=True, partial = True, pingpong = True)

    epd.draw.text('42:48', numr110H, manx,100, diff=True)
    epd.draw.text('22:45', numr110H, manx,100)
    epd.draw.show(key=k)
    epd.draw.text('WN:DW', numr110H, manx, 100)
    epd.draw.show(key=k)
    epd.show_ram()
    epd(1, partial=False)
    epd.sleep()

 