# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# LUTs have been copied from original example for Waveshare Pico e-Paper 3.7,
# which can be found here:
# https://github.com/waveshare/Pico_ePaper_Code/blob/main/python/Pico-ePaper-3.7.py
#
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


EPD_3IN7_lut_4Gray_GC = bytes([
    0x2A, 0x06, 0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 1
    0x28, 0x06, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 2
    0x20, 0x06, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 3
    0x14, 0x06, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 4
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 5
    0x00, 0x02, 0x02, 0x0A, 0x00, 0x00, 0x00, 0x08, 0x08, 0x02,  # 6
    0x00, 0x02, 0x02, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 7
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 8
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 9
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 10
    0x22, 0x22, 0x22, 0x22, 0x22
])

EPD_3IN7_lut_1Gray_GC = bytes([
    0x2A, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 1
    0x05, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 2
    0x2A, 0x15, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 3
    0x05, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 4
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 5
    0x00, 0x02, 0x03, 0x0A, 0x00, 0x02, 0x06, 0x0A, 0x05, 0x00,  # 6
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 7
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 8
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 9
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 10
    0x22, 0x22, 0x22, 0x22, 0x22
])

EPD_3IN7_lut_1Gray_DU = bytes([
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 1
    0x01, 0x2A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x0A, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 3
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 5
    0x00, 0x00, 0x05, 0x05, 0x00, 0x05, 0x03, 0x05, 0x05, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 7
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 9
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x22, 0x22, 0x22, 0x22, 0x22
])

EPD_3IN7_lut_1Gray_A2 = bytes([
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 1
    0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 2
    0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 3
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 4
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 5
    0x00, 0x00, 0x03, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 6
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 7
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 8
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 9
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 10
    0x22, 0x22, 0x22, 0x22, 0x22
])
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from core.Eink import Eink
from struct import pack, unpack

class EPDPico(Eink):  # SSD1677

    white = 0b11
    darkgray = 0b01
    lightgray = 0b10
    x_set = '2H'

    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 480
        self.ic_side = 280
        self._seqs = (0x03, 0x02, 0x01, 0x01)  # structure ( 0°, 90°, 180°, 270°)
        self._luts = (EPD_3IN7_lut_4Gray_GC,
                      EPD_3IN7_lut_1Gray_GC,
                      EPD_3IN7_lut_1Gray_DU,
                      EPD_3IN7_lut_1Gray_A2)

        super().__init__(spi, *args, **kwargs)

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("hB", 479, 0))  # 1= mirror

    def _set_voltage(self):
        # Set gate voltage.
        self._send(0x03, 0x00)
        # Set source voltage.
        self._send(0x04, pack("3B", 0x41, 0xa8, 0x32))

    def _set_VCOM(self):
        self._send(0x2c, 0x44)

    def _virtual_width(self, num=None):
        ''' returns width the way it shoulf be sent to the chip'''
        return self.width if num is None else 0 if num is 0 else num

    def _updt_ctrl_2(self):
        # Set Display Update Control 2
        if not self._partial:
            self._send(0x22, 0xc7)
        else:
            self._send(0x22, 0xcf)

    def _clear_ram(self, bw=True, red=True):
        if red:
            self._send(0x46, 0xf7)
            self._read_busy()
        if bw:
            self._send(0x47, 0xf7)
            self._read_busy()

    def _ld_norm_lut(self, lut=False):
        self._load_LUT(lut) if lut else self._load_LUT(0) if not self.monoc else self._load_LUT(1)

    def _ld_part_lut(self):
        self._load_LUT(2)

if __name__ == "__main__":
    from machine import SPI, Pin
    # Hor _part worlk, hor full shifts the cursor in a weird way. Vertical still needs work
    
    p = Pin(2, Pin.OUT)  # To restet the epd
    epdSPI = SPI(2, sck=Pin(12), baudrate=400000, mosi=Pin(13), miso=None)  # SPI instance fpr E-paper display (miso Pin necessary for SoftSPI, but not needed)
    epd = EPDPico(rotation=0, spi=epdSPI, cs_pin=Pin(10), dc_pin=Pin(9), reset_pin=p, busy_pin=Pin(11))  # Epaper setup (instance of EINK)
    epd.clear()
    import core.draw_modes as md
    from core.draw import Drawable as DR
    import numr110

    epd.draw.rect(0,0, 50, 50, f=True)
    epd.draw.show()

    epd.opmode(2, True, True, True)
    epd.draw.text('33', numr110, 134, 88, c=1)
    # objects too far in the last bit on the right throw off the alignement
    #like anything that touches the rightmost side, the lines get missaligned even if I print the buffer and it looks like it should
    
    epd.draw.rect(224,430,50,50, f=True)
    #print(next(DR.draw_all(280, 480, -1, True, black_ram = True)))
    # DR.reset()
    epd.draw.show()
    epd.sleep()