from core.Eink import Eink

class EPD2IN9(Eink):  # SSD1680
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11
    x_set = '2B'

    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 296
        self.ic_side = 128
        self._seqs = (0x03, 0x02, 0x01, 0x01)  # structure ( 0°, 90°, 180°, 270°)
        super().__init__(spi, *args, **kwargs)

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("3B", 0x27, 0x01, 0x00))

    def _virtual_width(self, num=None):
        ''' returns width the way it is sent to the chip'''
        return self.width // 8 if num is None else 0 if num is 0 else  num // 8

    def _clear_ram(self, bw=True, red=True):  # 0k, modifié la commande pour 0xe5
        if red:
            self._send(0x46, 0xe5)
            self._read_busy()
        if bw:
            self._send(0x47, 0xe5)
            self._read_busy()

    def _updt_ctrl_2(self):
        # Set Display Update Control 2 / loading LUTs
        if not self._partial:
            self._send(0x22, 0xf7)
        else:
            self._send(0x22, 0xff)
        self._read_busy()

if __name__ == "__main__":
    from machine import Pin, SPI
    p = Pin(2, Pin.OUT)
    epdSPI = SPI(2, sck=Pin(45), baudrate=400000, mosi=Pin(47), miso=0)
    epd = EPD2IN9(rotation=90, spi=epdSPI, cs_pin=Pin(3), dc_pin=Pin(29), reset_pin=p, busy_pin=Pin(5))