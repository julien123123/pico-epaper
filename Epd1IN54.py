# code works for driving te display, but still have the right modes / luts to figure out as images in the bw buffer in the
# the display shows as light gray (which is what happened the first time I drove all the other displays). Seems like it
# is using a different formula for the coordinates than all the other displays.

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
        self._seqs = (0x03, 0x06, 0x00, 0x05) # structure ( 0°, 90°, 180°, 270°) framebuf mode good vals (3, 6, 0, 5)
        super().__init__(spi, *args, **kwargs)

    def _clear_ram(self, bw=True, red=True):  # 0k, modifié la commande pour 0xe5
        if red:
            self._send(0x46, 0xe5) #peut être 0x55
            self._read_busy()
        if bw:
            self._send(0x47, 0xe5)
            self._read_busy()

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("3B", 0xC7, 0x00, 0x00))

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
    p = Pin(15, Pin.OUT)
    epdSPI = SPI(2, sck=Pin(12), mosi=Pin(11), miso=None)
    epd = EPD1IN54(rotation=0, spi=epdSPI, cs_pin=Pin(7), dc_pin=Pin(5), reset_pin=p, busy_pin=Pin(16), use_partial_buffer=False)
    epd.text('heller', 0, 0)
    epd.show()
    