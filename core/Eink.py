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

    def _ld_norm_lut(self, lut):
        pass

    def _ld_part_lut(self):
        pass

    # --------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------

    def send_diff_buff(self, buff):
        self._send_command(0x26)
        self._send_buffer(buff)

    def get_buff(self):
        return self._buffer_bw_actual

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

    # @profile
    def show(self, x=None, y=None, lut=0, buff=None):  # buff = bytearray to send directly
        self._set_frame() if not self.wndw_set else None
        self._updt_ctrl_2()
        super().zero(x, y, lut)

        self._send_command(0x24)
        self._send_buffer(self._buffer_bw) if not buff else self._send_buffer(buff)
        # self.invert_ram()
        if self._partial:
            self._ld_part_lut()
        else:
            self._send_command(0x26)
            self._send_buffer(self._buffer_red) if not self.monoc else self._send_buffer(self._buffer_bw)
            self._ld_norm_lut(lut)

        self._send_command(0x20)
        self._read_busy()

    def show_ram(self, lut=0):
        ''' convinience function for testing '''
        self._ld_norm_lut(lut)
        self._send_command(0x20)
        self._read_busy()

    def clear(self):
        '''Clears the display'''
        self.partial_mode_off() if self._partial else None
        self.width, self.height = (self.long, self.short) if self._sqr else (self.short, self.long)
        s = (self.long + 7) * self.short // 8
        self._set_frame()
        self._updt_ctrl_2()
        self.zero(0, 0, 0)
        self._send_command(0x24)
        self._send_data(bytearray([0xff] * s))
        self._send_command(0x26)
        self._send_data(bytearray([0xff] * s))
        self.show_ram(0)

    # @profile
    def quick_buf(self, w, h, x, y, buff, diff=None, invert=False):
        ''' Directly pass a buffer to part update
            For now Y has to be a multiple of 8
            you can send character by character
        '''
        self.width = w if w <= x or x == 0 else w + x  # if x is under the width of the buffer, we have to do some hack
        self.height = h
        #self.partial_mode_on() if not self._partial else None
        self._set_frame(y) if not self.wndw_set else None
        self._updt_ctrl_2()
        self.zero(x, y + h, 0)
        self._send_command(0x24)
        self._send_data(buff)
        if diff:
            self._send_command(0x26)
            self._send_data(diff)
            self.invert_ram() if invert else None
        else:
            self.invert_ram() if invert else None

    def eco_show(self, w=None, h=None, x=None, y=None, new_buff=None, diff_buff=None):  # Work in progress
        ''' method to allow partial update after epd sleep or mcu deepsleep
            by default, it'll make a full frame partial update over the last full update'''
        if self.inited:
            raise Exception('must be used after sleep() method')
        else:
            self.reinit()
            self.partial_mode_on() if not w else self.partial_mode_on(w, h)
            # method for automatically toggling buffers after epd.sleep
            diff_buff = diff_buff if diff_buff else self._buffer_bw_actual  # if differential buffer not specified, will take the last available full buffer
            self._set_frame() if not self.wndw_set else None
            self.send_diff_buff(diff_buff)

            self.show() if not x else self.show(x, y)
            self.partial_mode_off()
            self.sleep()