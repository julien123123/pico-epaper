from machine import Pin
import framebuf
from utime import sleep_ms
from ustruct import pack

class EinkBase:
    black = const(0b00)
    white = 0
    darkgray = 0
    lightgray = 0
    RAM_BW = const(0b01)
    RAM_RED = const(0b10)
    RAM_RBW = const(0b11)
    x_set = 0  # format to send x width to the display

    def __init__(self, rotation=0, cs_pin=None, dc_pin=None, reset_pin=None, busy_pin=None, use_partial_buffer=False,
                 monochrome=True):
        if rotation == 0 or rotation == 180: #this should now go in frambuf mode... not so usefull here
            self.width = self.ic_side
            self.height = self.sqr_side
            self.buf_format = framebuf.MONO_HLSB
            self._sqr = False
        elif rotation == 90 or rotation == 270:
            self.width = self.sqr_side
            self.height = self.ic_side
            self.buf_format = framebuf.MONO_VLSB
            self._sqr = True #srq = square rotations
        else:
            raise ValueError(
                f"Incorrect rotation selected ({rotation}). Valid values: 0, 90, 180 and 270.")

        self._rotation = rotation
        self.monoc = monochrome  # black and white only flag
        self.cur_seq = self._seqs[int(rotation/90)]

        if reset_pin is None:
            self._rst = Pin(12, Pin.OUT, value=0)
        else:
            self._rst = reset_pin
            self._rst.init(Pin.OUT, value=0)

        if dc_pin is None:
            self._dc = Pin(8, Pin.OUT, value=0)
        else:
            self._dc = dc_pin
            self._dc.init(Pin.OUT, value=0)

        if cs_pin is None:
            self._cs = Pin(9, Pin.OUT, value=1)
        else:
            self._cs = cs_pin
            self._cs.init(Pin.OUT, value=1)

        if busy_pin is None:
            self._busy = Pin(13, Pin.IN, Pin.PULL_UP)
        else:
            self._busy = busy_pin
            self._busy.init(Pin.IN)

        # setting buffers as None initially to allow for lazy loading
        self._buffer_bw_actual = None
        self._buffer_red = None
        self._bw_actual = None
        self._red = None
        self._buffer_partial = None
        self._part = None

        # Don't start in partial mode.
        self._partial = False
        self._use_partial_buffer = use_partial_buffer

        # Alias buffer and FrameBuffer to indicate which buffer should be treated as BW RAM buffer.
        self._buffer_bw = self._buffer_bw_actual
        self._bw = self._bw_actual

        # Flag to tell if the window size instruction was sent
        self.wndw_set = False
        self.inited = False  # inited flag
        self.ram_inv = False

        # self.fill()

        self._init_disp()
        sleep_ms(500)

    @property  # for allowing to lazily load the framebuffers
    def bw(self):
        if not self._bw:
            pad = 0 if self.width in (self.sqr_side, self.ic_side) else 17
            self._buffer_bw_actual = bytearray((self.width + pad) * self.height // 8)
            self._bw_actual = framebuf.FrameBuffer(self._buffer_bw_actual, self.width, self.height, self.buf_format)

            # Alias buffer and FrameBuffer to indicate which buffer should be treated as BW RAM buffer.
            self._buffer_bw = self._buffer_bw_actual
            self._bw = self._bw_actual
            self._bw.fill(1)
        return self._bw

    @property
    def red(self):
        if not self._red and not self.monoc:
            pad = 0 if self.width in (self.sqr_side, self.ic_side) else 7
            self._buffer_red = bytearray((self.width + pad) * self.height // 8)
            self._red = framebuf.FrameBuffer(self._buffer_red, self.width, self.height, self.buf_format)
            self._red.fill(1)
        return self._red

    @property
    def part(self):
        if self._use_partial_buffer and not self._part:
            pad = 0 if self.width in (self.sqr_side, self.ic_side) else 17
            self._buffer_partial = bytearray((self.width + pad) * self.height // 8)
            self._part = framebuf.FrameBuffer(self._buffer_partial, self.width, self.height, self.buf_format)
            self._part.fill(1)
        return self._part

    def _reset(self):
        self._rst(1)
        sleep_ms(30)
        self._rst(0)
        sleep_ms(3)
        self._rst(1)
        sleep_ms(30)

    def _send(self, command, data):
        self._send_command(command)
        self._send_data(data)

    def _read_busy(self):
        while self._busy.value() == 1:
            sleep_ms(10)
        sleep_ms(200)

    def _load_LUT(self, lut=0):
        self._send(0x32, self._luts[lut])

    def _set_cursor(self, x, y):
        self._send(0x4e, pack("h", x))
        self._send(0x4f, pack("h", y))

    def _set_window(self, start_x, end_x, start_y, end_y):
        self._send(0x44, pack(self.x_set, start_x, end_x))
        self._send(0x45, pack("2h", start_y, end_y))

    def _set_frame(self, disp_x=0):
        '''
        sets the window according to the origin point of the display mode; uses absolute display ram addresses
        :param disp_x = position of the buffer in the x space from the upper left corner when display is at 0 rotation
        left most bit (horrizontal/vertical) is ignored
        '''
        x, y = (self.width, self.height) if not self._sqr else (self.height, self.width)
        if self.cur_seq & 0b11 == 0: #bottom left
            self._set_window(self._virtual_width(x) + disp_x - 1, 0 + disp_x, y-1, 0)
        elif self.cur_seq & 0b11 == 1: #bottom right
            self._set_window(0 + disp_x, self._virtual_width(x) + disp_x - 1, y-1, 0)
        elif self.cur_seq & 0b11 == 2: #top right
            self._set_window(self._virtual_width(x) + disp_x -1, 0 + disp_x, 0, y - 1)
        elif self.cur_seq & 0b11 == 3: #top left
            self._set_window(0 + disp_x, self._virtual_width(x) +disp_x - 1, 0, y - 1 )
        else:
            raise ValueError(f'Incorrect rotation or display mode selected')

        self.wndw_set = True

    def _init_disp(self):
        # HW reset.
        self._reset()

        # SW reset.
        self._send_command(0x12)
        sleep_ms(20)

        # Clear BW and RED RAMs.
        self._clear_ram()

        # Set gate/voltages according to each display
        self._set_gate_nb()
        self._set_voltage()

        # Set Data Entry mode.
        self._send(0x11, self.cur_seq)

        # Set border.
        self._send(0x3c, 0x03)

        # Booster Soft-start Control.
        self._send(0x0c, pack("5B", 0xae, 0xc7, 0xc3, 0xc0, 0xc0))

        # Internal sensor on.
        self._send(0x18, 0x80)

        self._set_VCOM()

        self.inited = True

    # --------------------------------------------------------
    # Dummy Methods that get overridden by child classes
    # --------------------------------------------------------
    def _send_command(self, command):
        raise NotImplementedError

    def _send_data(self, data):
        raise NotImplementedError

    def _clear_ram():
        raise NotImplementedError

    def _set_gate_nb():
        raise NotImplementedError

    def _set_voltage(self):
        pass

    def _set_VCOM(self):
        pass

    def _virtual_width():
        raise NotImplementedError

    def _updt_ctrl_2(self):
        pass

    # --------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------

    def reinit(self):
        """Public method for screen reinitialisation."""
        self._init_disp()

    def partial_mode_on(self, width=None, height=None, pingpong=True):
        self.width = width or self.width
        self.height = height or self.height
        pp = 0x4f if pingpong else 0xf
        self._send(0x37, pack("10B", 0x00, 0xff, 0xff, 0xff, 0xff, pp, 0xff, 0xff, 0xff, 0xff))
        self._clear_ram()
        if self._use_partial_buffer:
            self.bw
            self.part
            self._buffer_bw = self._buffer_partial
            self._bw = self._part
            self._part.fill(1)
        else:
            self.bw.fill(1) if self._bw else None
        self._partial = True

    def partial_mode_off(self):
        self._send(0x37, pack("10B", 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00))
        self._clear_ram()
        if self._use_partial_buffer:
            self._buffer_bw = self._buffer_bw_actual
            self._bw = self._bw_actual
        self._partial = False

    def zero(self, abs_x=None, abs_y=None, lut=0):
        """Pointing the zero of the buffer in absolute display coordinate"""
        x, y = (self.width, self.height) if not self._sqr else (self.height, self.width)
        if self.cur_seq & 0b11 == 0:
            self._set_cursor(self._virtual_width(x)-1, y-1) if not abs_x or abs_y else self._set_cursor(self._virtual_width(x-abs_x)-1, abs_y)
        elif self.cur_seq & 0b11 == 1:
            self._set_cursor(0,y-1) if not abs_x or abs_y else self._set_cursor(self._virtual_width(abs_x)-1, y-abs_y-1)
        elif self.cur_seq & 0b11 == 2:
            self._set_cursor(self._virtual_width(x)-1, 0) if not abs_x or abs_y else self._set_cursor(self._virtual_width(x-abs_x) -1, abs_y - 1)
        else:
            self._set_cursor(0,0) if not abs_x or abs_y else self._set_cursor(self._virtual_width(abs_x) -1, abs_y - 1)

    def sleep(self):
        self._send(0x10, 0x03)
        self.inited = False
        self.wndw_set = False
        self.ram_inv = False

    # --------------------------------------------------------
    # Drawing routines (wrappers for FrameBuffer methods).
    # --------------------------------------------------------

    def fill(self, c=None):
        c = self.white if not c else c
        self.bw.fill(c & 1)
        if not self._partial and not self.monoc:
            self.red.fill(c >> 1)

    def pixel(self, x, y, c=black):
        self.bw.pixel(x, y, c & 1)
        if not self._partial:
            self.red.pixel(x, y, c >> 1)

    def hline(self, x, y, w, c=black):
        self.bw.hline(x, y, w, c & 1)
        if not self._partial and not self.monoc:
            self.red.hline(x, y, w, c >> 1)

    def vline(self, x, y, h, c=black):
        self.bw.vline(x, y, h, c & 1)
        if not self._partial:
            self.red.vline(x, y, h, c >> 1)

    def line(self, x1, y1, x2, y2, c=black):
        self.bw.line(x1, y1, x2, y2, c & 1)
        if not self._partial and not self.monoc:
            self.red.line(x1, y1, x2, y2, c >> 1)

    def rect(self, x, y, w, h, c=black, f=False):
        self.bw.rect(x, y, w, h, c & 1, f)
        if not self._partial and not self.monoc:
            self.red.rect(x, y, w, h, c >> 1, f)

    def ellipse(self, x, y, xr, yr, c=black, f=False, m=15):
        self.bw.ellipse(x, y, xr, yr, c & 1, f, m)
        if not self._partial and not self.monoc:
            self.red.ellipse(x, y, xr, yr, c >> 1, f, m)

    def poly(self, x, y, coords, c=black, f=False):
        self.bw.poly(x, y, coords, c & 1, f)
        if not self._partial and not self.monoc:
            self.red.poly(x, y, coords, c >> 1, f)

    def text(self, text, x, y, c=black):
        self.bw.text(text, x, y, c & 1)
        if not self._partial and not self.monoc:
            self.red.text(text, x, y, c >> 1)

    def blit(self, fbuf, x, y, key=-1, palette=None, ram=RAM_RBW):
        if ram & 1 == 1 or self._partial:
            self.bw.blit(fbuf, x, y, key, palette)
        if (ram >> 1) & 1 == 1:
            self.red.blit(fbuf, x, y, key, palette)