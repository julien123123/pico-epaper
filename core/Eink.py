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

    def _void_ram(self, bw = False, red = False):
        '''voids the ram'''
        b = 0
        b += 1 << 2 if bw else 0
        b += 1 << 6 if red else 0
        self._send(0x21, b)

    # --------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------
    def invert_ram(self, bw=True, red=True):
        '''invert 1 and 0s in the ram'''
        b = 0
        b += 1 << 3 if bw else 0
        b += 1 << 7 if red else 0
        self._send(0x21, b)

    def show_ram(self):
        self._updt_ctrl_2()
        self._send_command(0x20)
        self._read_busy()

    def clear(self):
        '''Clears the display'''
        self.__call__(1, self.norm, False, False)
        self.draw.pixel(10, 1, diff= True)
        self.show(full= True, clear = True, key=1)

    def show(self, full = False, flush = True, key = -1, clear = False):
        ''' This makes it easier to update the display'''
        self._sort_ram()
        self._clear_ram() if clear else None
        self.draw.show(full, flush, key)