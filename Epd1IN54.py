from core.Eink import Eink

class EPD1IN54(Eink):  # SSD1681
    x_set = '2B'
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11

    def __init__(self, spi=None, *args, **kwargs):
        self.long = 200
        self.short = 200
        super().__init__(spi, *args, **kwargs)

    def _clear_ram(self, bw=True, red=True):  # 0k, modifié la commande pour 0xe5
        if red:
            self._send(0x46, 0x55)
            self._read_busy()
        if bw:
            self._send(0x47, 0x55)
            self._read_busy()

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("3B", 0xC7, 0x00, 0x00))

    def _virtual_width(self, num=None):
        ''' returns width the way it is sent to the chip'''
        return self.width // 8 if not num else num // 8

    def _updt_ctrl_2(self):
        # Set Display Update Control 2 / loading LUTs
        if not self._partial:
            self._send(0x22, 0xf7)
        else:
            self._send(0x22, 0xff)
        self._read_busy()

if __name__ == "__main__":
    from machine import Pin, SPI
    p = Pin(15, Pin.OUT)
    epdSPI = SPI(2, sck=Pin(12), mosi=Pin(11), miso=None)
    epd = EPD1IN54(rotation=90, spi=epdSPI, cs_pin=Pin(7), dc_pin=Pin(5), reset_pin=p, busy_pin=Pin(16), se_partial_buffer=False)