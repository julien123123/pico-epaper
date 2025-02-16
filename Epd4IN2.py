from core.Eink import Eink
from ustruct import pack

class EPD4IN2(Eink): #SSD1683 GDEY042T81 (not for the T2)
    x_set = '2B'
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11

    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 300
        self.ic_side = 400
        self._seqs = (0x03, 0x06, 0x00, 0x05)  # structure ( 0°, 90°, 180°, 270°) 3605 pour framebuf = parfait
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
            self._send(0x1A, 0x6E)
            self._send(0x22, 0xff)
        self._read_busy()
if __name__ == "__main__":
    from machine import Pin, SPI
    import numr110H, freesans20, time
    
    p = Pin(27, Pin.OUT)
    epdSPI = SPI(0, sck=Pin(2), mosi=Pin(3), miso=None)
    epd = EPD4IN2(rotation=0, spi=epdSPI, cs_pin=Pin(1), dc_pin=Pin(26), reset_pin=p, busy_pin=Pin(28), use_partial_buffer=False)

    import core.draw_modes as md
    from core.draw import Drawable as DR
    
    ac = md.DirectMode(epd, md.BW2X)
    ac.text('3', numr110H, 20, 20, c = 1)
    #ac.rect(350,250,50,50)
    #next(DR.draw_all(400, 300, -1, True, black_ram = True))
    #DR.reset()
    ac.show()
    epd._clear_ram()
    ac.mode = md.BW2B
    epd.partial_mode_on()
    manx = 6
    k=0
    ac.rect(220, 30, 40, 40, f=True, c = 0)
    ac.text('42:48', numr110H, manx,100)
    ac.text(' Mercredi 20 dec 2025', freesans20, manx,2, c=1)
    #ac.line(9,23, 57, 10)
    #print(DR.xspan, DR.yspan)

    ac.ellipse(43, 30, 79, 80, f= False)
    #ac.vline(0, 100, 100, 1)
    ac.show(key=k)
    epd.sleep()
    # Yup, we are sleeping babe
    epd.reinit()
    ac.text('42:48', numr110H, manx,100, diff=True)
    ac.text('22:45', numr110H, manx,100)
    ac.show(key=k)
    ac.text('WN:DW', numr110H, manx, 100)
    ac.show(key=k)
    epd.partial_mode_off()
    #ac.text('6', numr110H, 0, 0)
    #ac.show()
    epd.sleep()

 