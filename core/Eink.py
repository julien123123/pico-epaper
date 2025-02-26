from core.EinkBase import EinkBase
import micropython

class Eink(EinkBase):
    from machine import SPI

    def __init__(self, spi=None, *args, **kwargs):
        if spi is None:
            self._spi = self.SPI(1, baudrate=20_000_000)
        else:
            self._spi = spi
        super(Eink, self).__init__(*args, **kwargs)

    def _send_command(self, command):
        self._dc(0)
        self._cs(0)
        if isinstance(command, int):
            self._spi.write(bytes([command]))
        elif isinstance(command, (bytes, bytearray)):
            self._spi.write(command)
        else:
            raise ValueError  # For now
        self._cs(1)

    def _send_data(self, data):
        self._dc(1)
        self._cs(0)
        if isinstance(data, int):
            self._spi.write(bytes([data]))
        elif isinstance(data, (bytes, bytearray)):
            self._spi.write(data)
        else:
            raise ValueError  # For now
        self._cs(1)

    @micropython.viper
    def _reverse_bits(self, num: int) -> int:
        result = 0
        for i in range(8):
            result = (result << 1) | ((num >> i) & 1)
        return result

    def _send_buffer(self, buffer):
        if self._sqr:
            self._send_data(bytes(map(self._reverse_bits, buffer)))
        else:
            self._send_data(buffer)

    def _void_ram(self, bw = False, red = False):
        '''voids the ram'''
        b = 0
        b += 1 << 2 if bw else 0
        b += 1 << 6 if red else 0
        self._send(0x21, b)

    def _ld_norm_lut(self, lut=False):
        pass

    def _ld_part_lut(self):
        pass

    # --------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------
    def invert_ram(self, bw=True, red=True):
        '''invert 1 and 0s in the ram'''
        b = 0
        if not self.ram_inv:
            b += 1 << 3 if bw else 0
            b += 1 << 7 if red else 0
            self.ram_inv = True
        else:
            self.ram_inv = False
        self._send(0x21, b)

    def show_ram(self, lut=0):
        ''' convinience function for testing '''
        self._ld_norm_lut(lut)
        self._send_command(0x20)
        self._read_busy()

    def clear(self):
        '''Clears the display'''
        self.partial_mode_off() if self._partial else None
        self.width, self.height = (self.sqr_side, self.ic_side) if self._sqr else (self.ic_side, self.sqr_side)
        s = (self.sqr_side + 7) * self.ic_side // 8
        self._set_frame()
        self._updt_ctrl_2()
        self.zero(0, 0, 0)
        self._send_command(0x24)
        self._send_data(bytearray([0xff] * s))
        self._send_command(0x26)
        self._send_data(bytearray([0xff] * s))
        self.show_ram(0)

    def show(self, full = False, flush = True, key = -1, clear = False):
        ''' This makes it easier to update the display'''
        self._clear_ram() if clear else None
        self.draw.show(full, flush, key)