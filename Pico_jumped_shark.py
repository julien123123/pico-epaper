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

from machine import Pin
import framebuf
from utime import ticks_ms, ticks_diff, sleep_ms
from ustruct import pack
import gc
import micropython


def profile(func):
    def wrapper(*args, **kwargs):
        gc.collect()
        start_mem = gc.mem_free()
        start_t = ticks_ms()
        func(*args, **kwargs)
        fin_t = ticks_ms()
        fin_mem = gc.mem_free()
        print(f'{func.__name__} took: {ticks_diff(fin_t, start_t)} ms to finish')
        print(f'{func.__name__} used around {start_mem - fin_mem} B of memory')

    return wrapper


class EinkBase:
    black = const(0b00)
    white = 0
    darkgray = 0
    lightgray = 0
    RAM_BW  = const(0b01)
    RAM_RED = const(0b10)
    RAM_RBW = const(0b11)
    x_set = 0 # format to send x width to the display

    def __init__(self, rotation=0, cs_pin=None, dc_pin=None, reset_pin=None, busy_pin=None, use_partial_buffer=False, monochrome=True):
        if rotation == 0 or rotation == 180:
            self.width = self.short
            self.height = self.long
            self.buf_format = framebuf.MONO_HLSB
            self._horizontal = False
        elif rotation == 90 or rotation == 270:
            self.width = self.long
            self.height = self.short
            self.buf_format = framebuf.MONO_VLSB
            self._horizontal = True
        else:
            raise ValueError(
                f"Incorrect rotation selected ({rotation}). Valid values: 0, 90, 180 and 270.")

        self._rotation = rotation
        self.monoc = monochrome #black and white only flag

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

        #setting buffers as None initially to allow for lazy loading
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
        self.inited = False # inited flag
        self.ram_inv = False


        #self.fill()

        self._init_disp()
        sleep_ms(500)
    
    @property #for allowing to lazily load the framebuffers
    def bw(self):
        if not self._bw:
            self._buffer_bw_actual = bytearray((self.width + 17) * self.height  // 8)
            self._bw_actual = framebuf.FrameBuffer(self._buffer_bw_actual, self.width, self.height, self.buf_format)

            # Alias buffer and FrameBuffer to indicate which buffer should be treated as BW RAM buffer.
            self._buffer_bw = self._buffer_bw_actual
            self._bw = self._bw_actual
            self._bw.fill(1)
        return self._bw
    @property
    def red(self):
        if not self._red and not self.monoc:
            self._buffer_red = bytearray((self.width+7) * self.height // 8)
            self._red = framebuf.FrameBuffer(self._buffer_red, self.width, self.height, self.buf_format)
            self._red.fill(1)
        return self._red
    
    @property
    def part(self):
        if self._use_partial_buffer and not self._part:
                self._buffer_partial = bytearray((self.width + 17) * self.height // 8)
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

    def _send_command(self, command):
        raise NotImplementedError

    def _send_data(self, data):
        raise NotImplementedError

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

    def _set_frame(self, disp_x = 0):
        #disp_x = position of the buffer in the x space from the upper left corner when display is at 0 rotation
        '''Translates framebuffer frame size int display ic size'''
        if self._rotation == 0:
            self._set_window(0 + disp_x, self._virtual_width(self.width)+ disp_x - 1, 0, self.height - 1)
        elif self._rotation == 180:
            self._set_window(self._virtual_width(self.width) + disp_x - 1, 0 + disp_x, self.height - 1, 0)
        elif self._rotation == 90:
            self._set_window(self._virtual_width(self.height) + disp_x-1 , 0 + disp_x, 0 , self.width )
        elif self._rotation == 270:
            self._set_window(0 + disp_x, self._virtual_width(self.height) - 1 + disp_x, self.width - 1, 0)
        else:
            raise ValueError(f"Incorrect rotation selected")
        
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
        if self._rotation == 0: #les seq pour direct draw
            seq = 0x03
        elif self._rotation == 180:
            seq = 0x01
        elif self._rotation == 90:
            seq = 0x02 #2
        elif self._rotation == 270:
            seq = 0x01
        else:
            raise ValueError(f"Incorrect rotation selected")

        self._send(0x11, seq)

        # Set border.
        self._send(0x3c, 0x03)

        # Booster Soft-start Control.
        self._send(0x0c, pack("5B", 0xae, 0xc7, 0xc3, 0xc0, 0xc0))

        # Internal sensor on.
        self._send(0x18, 0x80)

        self._set_VCOM()

        self.inited = True

    # --------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------

    def reinit(self):
        """Public method for screen reinitialisation."""
        self._init_disp()

    def partial_mode_on(self, width= None, height= None, pingpong = True): 
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

    def zero(self,x =  None, y = None, lut=0):
        '''Translating buffer coordinates for cursor into display ic coordinates'''
        # This kind of thing id done a few times. Maybe the if part could be a function by itself

        if self._rotation == 0:
            self._set_cursor(0, 0) if not x else self._set_cursor(x, y)
        elif self._rotation == 180:
            self._set_cursor(self._virtual_width(self.width) - 1, self.height - 1) if not x else self._set_cursor(self._virtual_width(x) - 1, y - 1)
        elif self._rotation == 90:
            self._set_cursor(self._virtual_width(self.height) - 1, 0) if not x else self._set_cursor(self._virtual_width(y) - 1, x)
        else:
            self._set_cursor(0, self.width - 1) if not x else self._set_cursor(self._virtual_width(y), x - 1)

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


class Framebuf_mode(EinkBase):
    def __init__(self):
        pass


class Direct_mode(EinkBase):
    
    # This mode has not transparency, if you need it, use Framebuf_mode, at least for the first full update.
    
    def __init__(self):
        pass

    def _send_bw(self, buff):
        self._send_command(0x24)
        self._send_data(buff)

    def _send_red(self, buff):
        self._send_command(0x26)
        self._send_data(buff)

    def _disp_xy(self, x, y):
        if self._rotation == 0 or 180:
            return x, y
        else:
            return y, x
    # --------------------------------------------------------
    # Drawing routines (directly to the display).
    # --------------------------------------------------------
    #
    # bw_ram parameter can be False to use 2 different buffers under monochrome (self.monoc) mode or to send the drawing
    # to the differential (eraser) buffer under partial update mode.
    
    def fill(self, c=None, bw_ram = True):
        c = self.white if not c else c
        bbytes = 0xff if c & 1 else 0x00
        self._send_bw(bytearray([bbytes]* ((self.long+7)*self.short//8))) if bw_ram else None
        if not self._partial and not self.monoc or not bw_ram:
            rbytes = 0xff if c >> 1 else 0x00
            self._send_red(bytearray([bbytes]* ((self.long+7)*self.short//8)))

    def pixel(self, x, y, c=black):
        pass

    def hline(self, x, y, w, c=black):
        pass

    def vline(self, x, y, h, c=black):
        pass

    def line(self, x1, y1, x2, y2, c=black):
        pass

    def rect(self, x, y, w, h, c=black, f=False):
        pass

    def ellipse(self, x, y, xr, yr, c=black, f=False, m=15):
        pass

    def poly(self, x, y, coords, c=black, f=False):
        pass

    def text(self, text, font, x, y, c=black):
        # you need to give a font as the display doesn't have one by default
        # more like a squential img() function
        pass

    def img(self, buff, x, y):
        #very similar to buff mode show(x,y)
        # set frame
        # set cursor
        # send buff
        pass

    # function for setting x y and cursor every time

    def show(self): #previously show_ram
        self._ld_norm_lut()
        self._send_command(0x20)
        self._read_busy()


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
        if self._horizontal:
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
    
    def send_diff_buff(self,buff):
        self._send_command(0x26)
        self._send_buffer(buff)
    
    def get_buff(self):
        return self._buffer_bw_actual
    
    def invert_ram(self,bw=True, red=True):
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
    def show(self, x = None, y = None, lut=0, buff= None): #buff = bytearray to send directly
        self._set_frame() if not self.wndw_set else None
        self._updt_ctrl_2()
        super().zero(x,y,lut)

        self._send_command(0x24)
        self._send_buffer(self._buffer_bw) if not buff else self._send_buffer(buff)
        #self.invert_ram()
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
        self.width = self.long
        self.height = self.short
        s = (self.long+7)*self.short//8
        self._set_frame()
        self._updt_ctrl_2()
        self.zero(0, 0, 0)
        self._send_command(0x24)
        self._send_data(bytearray([0xff] *s))
        self._send_command(0x26)
        self._send_data(bytearray([0xff] *s))
        self.show_ram(0)

    #@profile
    def quick_buf(self, w, h, x, y, buff, diff=None, invert=False):
        ''' Directly pass a buffer to part update
            For now Y has to be a multiple of 8
            you can send character by character
        '''
        self.width = w if w <= x or x == 0 else w + x # if x is under the width of the buffer, we have to do some hack
        self.height = h
        self.partial_mode_on() if not self._partial else None
        self._set_frame(y) if not self.wndw_set else None
        self._updt_ctrl_2()
        self.zero(x,y+h,0)
        self._send_command(0x24)
        self._send_data(buff)
        if diff:
            self._send_command(0x26)
            self._send_data(diff)
            self.invert_ram() if invert else None
        else:
            self.invert_ram() if invert else None

    def eco_show(self,w = None, h = None, x = None, y = None, new_buff = None, diff_buff = None): #Work in progress
        ''' method to allow partial update after epd sleep or mcu deepsleep
            by default, it'll make a full frame partial update over the last full update'''
        if self.inited:
            raise Exception('must be used after sleep() method')
        else:
            self.reinit()
            self.partial_mode_on() if not w else self.partial_mode_on(w, h)
            # method for automatically toggling buffers after epd.sleep
            diff_buff = diff_buff if diff_buff else self._buffer_bw_actual #if differential buffer not specified, will take the last available full buffer
            self._set_frame() if not self.wndw_set else None
            self.send_diff_buff(diff_buff)

            self.show() if not x else self.show(x, y)
            self.partial_mode_off()
            self.sleep()

class EPDPico(Eink): #SSD1677

    white =     0b11
    darkgray =  0b01
    lightgray = 0b10
    x_set = '2H'
        
    def __init__(self, spi=None, *args, **kwargs):
        self.long = 480
        self.short = 280

        self._luts = (EPD_3IN7_lut_4Gray_GC,
                EPD_3IN7_lut_1Gray_GC,
                EPD_3IN7_lut_1Gray_DU,
                EPD_3IN7_lut_1Gray_A2)

        super().__init__(spi, *args, **kwargs)
    
    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("hB", 479, 0)) # 1= mirror

    def _set_voltage(self):
        # Set gate voltage.
        self._send(0x03, 0x00)
        # Set source voltage.
        self._send(0x04, pack("3B", 0x41, 0xa8, 0x32))

    def _set_VCOM(self):
        self._send(0x2c, 0x44)

    def _virtual_width(self, num = None):
        ''' returns width the way it shoulf be sent to the chip'''
        return self.width if not num else num
    
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

    def _ld_norm_lut(self,l):
        self._load_LUT(l) if l else self._load_LUT(0) if not self.monoc else self._load_LUT(1)
        
    def _ld_part_lut(self):
        self._load_LUT(2)

class EPD2IN9(Eink): #SSD1680
    white =     0b01
    darkgray =  0b10
    lightgray = 0b11
    x_set = '2B'

    def __init__(self, spi=None, *args, **kwargs):
        self.long = 296
        self.short = 128
        super().__init__(spi, *args, **kwargs)

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("3B", 0x27, 0x01, 0x00))

    def _virtual_width(self, num = None):
        ''' returns width the way it is sent to the chip'''
        return self.width // 8 if not num else num // 8

    def _clear_ram(self, bw=True, red=True): #0k, modifié la commande pour 0xe5
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

class EPD4_2(Eink): #SSD1683

    def __init__(self, spi=None, *args, **kwargs):
        self.long = 400
        self.short = 300
        super().__init__(spi, *args, **kwargs)

class EPD1_54(Eink): #SSD1681
    x_set = '2B'
    white =     0b01
    darkgray =  0b10
    lightgray = 0b11
    
    def __init__(self, spi=None, *args, **kwargs):
        self.long = 200
        self.short = 200
        super().__init__(spi, *args, **kwargs)

    def _clear_ram(self, bw=True, red=True): #0k, modifié la commande pour 0xe5
        if red:
            self._send(0x46, 0x55)
            self._read_busy()
        if bw:
            self._send(0x47, 0x55)
            self._read_busy()

    def _set_gate_nb(self):
        # Set gate number.
        self._send(0x01, pack("3B", 0xC7, 0x00, 0x00))

    def _virtual_width(self, num = None):
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
    from machine import SPI
    import os
    device = "1IN54"
    if os.uname().sysname == 'nrf52':
        p = Pin(2, Pin.OUT)
        epdSPI = SPI(2, sck=Pin(45), baudrate=400000, mosi=Pin(47), miso=0)
        epd = EPD2IN9(rotation=90, spi=epdSPI, cs_pin=Pin(3), dc_pin=Pin(29), reset_pin=p, busy_pin=Pin(5), use_partial_buffer=True)

    if device == "pico":
        p = Pin(2, Pin.OUT) #To restet the epd
        epdSPI = SPI(2, sck=Pin(12), baudrate=400000, mosi=Pin(13), miso=None) #SPI instance fpr E-paper display (miso Pin necessary for SoftSPI, but not needed)
        epd = EPDPico(rotation=90, spi=epdSPI, cs_pin=Pin(10), dc_pin=Pin(9), reset_pin=p, busy_pin=Pin(11), use_partial_buffer=False) #Epaper setup (instance of EINK)
    if device == "1IN54":
        p = Pin(15, Pin.OUT)
        epdSPI = SPI(2, sck=Pin(12), mosi = Pin(11), miso = None)
        epd = EPD1_54(rotation=90, spi=epdSPI, cs_pin=Pin(7), dc_pin=Pin(5), reset_pin=p, busy_pin=Pin(16), use_partial_buffer=False)

    #import numr110VR
    import temp43VR #, numr110V, numr110
    '''
    c = numr110V.get_ch('5')
    epd.partial_mode_on(c[2], c[1])
    epd._buffer_bw = bytearray(c[0])
    epd.show(100,10)
    epd.sleep()
    '''
    
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
    '''
    @profile
    def draw_scr():         
        direct_text(epd, temp43VR, "26.1°C", 33, 10, 56)
        direct_text(epd, temp43VR, "6%", 33, 10, 8)
        direct_text(epd, temp43VR, "1013hPa", 33, 230, 8)
        direct_text(epd, numr110VR, '23:45', 74, 10, 136)
    #draw_scr()
    '''
    #direct_text(epd, numr110VR, 'W4', 74, 0, 0)
    #epd.show_ram(1)
    
    epd.clear()
    #epd.sleep()
    direct_text(epd, temp43VR, '8', 50, 0, 0)
    epd.show_ram(1)
    #direct_text(epd, numr110VR, '123',74, 0, 0)
    #epd.show_ram(1)

        
    '''
    d = numr110VR.get_ch('1')
    #epd.reinit()
    ff = d[0]
    dd = bytearray(len(ff))
    for i, v in enumerate(ff):
                dd[i] = 0xFF & ~ v
    epd.quick_buf(d[2], d[1],200, 136, dd)

    epd.quick_buf(d[2], d[1],274, 136, dd)
    '''
    #epd.show_ram(2) # This is waaaayyyy quicker
    '''
    epd.partial_mode_off()
    epd.reinit() # ça marche après reinit
    epd.text(' nfdfn',10,10) # petit en bas. peut-être que ça a besoin d'être ré-coordoné?
    #la seq 02 fonctionne!
    epd.show(300,100)
    '''
    
    



'''note to self:
The y setting is adjustable,, but the image will always be written to the side of the display
to adjust the x, (i'm talking in 90 rotation), you just have to select the right cursor and have the buffer the right height or width, i'm not sure yet. for 90 rotation, the buffer would have to be vlsb to be directly sent to the display.
*********** Après tests, curseur contrôle les x et window contrôle les y dans 0 et 180 **************

right seq for direct reversed bits/vertically map font for 90 deg = 00 -for just V, 02 aussi
'''


'''
Special thanks to this article : https://arthy.org/blog/sleep_epd/ by Michael Rao?
this article https://bitbanksoftware.blogspot.com/2022/10/using-e-paper-displays-on-resource.html & https://bitbanksoftware.blogspot.com/2024/09/bufferless-e-paper.html from Larrry Bank
'''