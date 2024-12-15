from core.Eink import Eink
from ustruct import pack

#Works!

class EPD4IN2(Eink): #SSD1683 GDEY042T81 (not for the T2)
    x_set = '2B'
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11

    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 300
        self.ic_side = 400
        self._seqs = (0x03, 0x04, 0x01, 0x05)  # structure ( 0°, 90°, 180°, 270°)
        super().__init__(spi, *args, **kwargs)

    def _clear_ram(self, bw=True, red=True):
        if red:
            self._send(0x46, 0xe6) #0x66 for black screen
            self._read_busy()
        if bw:
            self._send(0x47, 0xe6)
            self._read_busy()

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("hB", 299, 0x00)) #if second byte is 0x1 = mirror
        self._send(0x21, 0x00)

    def _virtual_width(self, num=None):
        ''' returns width the way it is sent to the chip'''
        return self.width // 8 if not num else num // 8

    def _updt_ctrl_2(self):
        # Set Display Update Control 2 / loading LUTs
        if not self._partial:
            self._send(0x22, 0xf7) #if not self.monoc else self._send(0x22, 0xcf)
        else:
            self._send(0x1A, 0x6E)
            self._send(0x22, 0xfc)
        self._read_busy()
if __name__ == "__main__":
    from machine import Pin, SPI
    import numr110H
    
    p = Pin(27, Pin.OUT)
    epdSPI = SPI(0, sck=Pin(2), mosi=Pin(3), miso=None)
    epd = EPD4IN2(rotation=270, spi=epdSPI, cs_pin=Pin(1), dc_pin=Pin(26), reset_pin=p, busy_pin=Pin(28), use_partial_buffer=False)

    def direct_text(epd, font, text, w, x, y, invert = True): # won't create framebuf object if not needed
        cur = x
        for char in text:
            cc = font.get_ch(char)
            arr = bytearray(cc[0])
            if invert:
                for i, v in enumerate(cc[0]):
                    arr[i] = 0xFF & ~ v
            epd.quick_buf(cc[2], cc[1], cur, y, arr)
            cur += w
        epd.wndw_set = False #will have to do this better somehow
        
    #direct_text(epd, numr110H, '8', 73, 8, 8)
    #epd.show_ram()
    
    epd.text('mimimimimi', 200, 200)
    epd.show()
    epd.partial_mode_on()
    epd.text('lalalala', 100, 30)
    epd.show()
    #epd.show_ram()
    epd.partial_mode_off()
    
    epd.sleep()
 