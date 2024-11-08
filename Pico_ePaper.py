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

    def _set_frame(self, disp_x = 79): #disp_x = position of the buffer in the x space from the upper left corner when display is at 0 rotation
        '''Translates framebuffer frame size int display ic size'''
        if self._rotation == 0:
            self._set_window(0 + disp_x, self._virtual_width(self.width)+ disp_x - 1, 0, self.height - 1) # disp_x peut être enlevé pour revenir en arière
        elif self._rotation == 180:
            self._set_window(self._virtual_width(self.width) + disp_x - 1, 0 + disp_x, self.height - 1, 0)
        elif self._rotation == 90:
            self._set_window(self._virtual_width(self.height) - 1 + disp_x, 0 + disp_x, 0, self.width - 1)
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
        if self._rotation == 0:
            seq = 0x03
        elif self._rotation == 180:
            seq = 0x00
        elif self._rotation == 90:
            seq = 0x06
        elif self._rotation == 270:
            seq = 0x05
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

    def partial_mode_on(self, width= None, height= None):
        self.width = width or self.width
        self.height = height or self.height
        print(self.width, ' x ', self.height)
        self._send(0x37, pack("10B", 0x00, 0xff, 0xff, 0xff, 0xff, 0x4f, 0xff, 0xff, 0xff, 0xff))
        self._clear_ram()
        if self._use_partial_buffer:
            self.bw
            self.part
            self._buffer_bw = self._buffer_partial
            self._bw = self._part
            self._part.fill(1)
        else:
            self.bw.fill(1)
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

    def clear(self): #clear de display
        self.partial_mode_off() if self._partial else None
        self._clear_ram()
        self.show_ram()

    def eco_show(self,w = None, h = None, x = None, y = None, new_buff = None, diff_buff = None): #Work in progress
        ''' method to allow update after epd sleep or mcu deepsleep
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

class EPDPico(Eink):

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
        self._send(0x01, pack("hB", 479, 0))

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
        self._load_LUT(l)
        
    def _ld_part_lut(self):
        self._load_LUT(2)

class EPD2IN9(Eink):
    
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

'''
# Unfortunatly, I cannot maintain this.
class EinkPIO(EinkBase):
    from machine import mem32

    def __init__(self, sm_num=0, dma=5, *args, **kwargs):
        self._sm_num = sm_num
        self._dma = int(dma * 0x40 + 0x50000030)
        self._sm = None
        self._sm_shiftctrl = (0x502000d0 + 0x100000 * (self._sm_num // 4)
                              + 0x18 * (self._sm_num % 4))
        self._dma_write_addr = (0x50200010 + 0x100000 * (self._sm_num // 4)
                                + 0x4 * (self._sm_num % 4))
        dreq = self._sm_num % 4 + 8 * (self._sm_num // 4)
        self._dma_ctrl = dreq << 15 | 1 << 4 | 1
        self._pio_setup()
        super(EinkPIO, self).__init__(*args, **kwargs)

    def _pio_setup(self):
        from rp2 import asm_pio, PIO, StateMachine

        @asm_pio(out_init=PIO.OUT_LOW,
                 sideset_init=PIO.OUT_LOW,
                 autopull=True,
                 pull_thresh=8,
                 out_shiftdir=PIO.SHIFT_LEFT)
        def pio_serial_tx():
            out(pins, 1).side(0)
            nop().side(1)

        self._sm = StateMachine(self._sm_num, pio_serial_tx, freq=40_000_000,
                                sideset_base=Pin(10), out_base=Pin(11))
        self._sm.active(1)

    def _reversed_output(self):
        self.mem32[self._sm_shiftctrl + 0x2000] = 1 << 19

    def _normal_output(self):
        self.mem32[self._sm_shiftctrl + 0x3000] = 1 << 19

    def _send_command(self, command):
        self._dc(0)
        self._cs(0)
        if isinstance(command, int):
            self._sm.put(command, 24)
        elif isinstance(command, (bytes, bytearray)):
            for cmd in command:
                self._sm.put(cmd, 24)
        else:
            raise ValueError
        self._cs(1)

    def _send_data(self, data):
        self._dc(1)
        self._cs(0)
        if isinstance(data, int):
            self._sm.put(data, 24)
        elif isinstance(data, (bytes, bytearray)):
            for cmd in data:
                self._sm.put(cmd, 24)
        else:
            raise ValueError
        self._cs(1)

    @micropython.viper
    def _dma_start(self, buffer):
        dma_ptr = ptr32(self._dma)
        dma_ptr[0] = int(self._dma_ctrl)
        dma_ptr[1] = int(self._dma_write_addr)
        dma_ptr[2] = int(len(buffer))
        dma_ptr[3] = int(ptr32(buffer))

    @micropython.viper
    def _check_dma_busy(self, a: ptr32) -> int:
        return (a[0] >> 24) & 1

    def _send_buffer(self, buffer):
        if self._horizontal:
            self._reversed_output()

        self._dc(1)
        self._cs(0)

        self._dma_start(buffer)
        dma_ctrl = self._dma

        start = ticks_ms()
        while self._check_dma_busy(dma_ctrl) and ticks_diff(ticks_ms(), start) < 5000:
            pass
        self._cs(1)
        if ticks_diff(ticks_ms(), start) >= 5000:
            print('loading data took too long')

        if self._horizontal:
            self._normal_output()
    # --------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------

    # @profile
    def show(self, lut=0):
        super().show()
        self._send_command(0x24)
        self._send_buffer(self._buffer_bw)
        if self._partial:
            self._load_LUT(2)
        else:
            self._send_command(0x26)
            self._send_buffer(self._buffer_red)
            self._load_LUT(lut)

        self._send_command(0x20)
        self._read_busy()
'''

if __name__ == "__main__":
    from machine import SPI
    import os
    if os.uname().sysname == 'nrf52':
        p = Pin(2, Pin.OUT)
        epdSPI = SPI(2, sck=Pin(45), baudrate=400000, mosi=Pin(47), miso=0)
        epd = EPD2IN9(rotation=90, spi=epdSPI, cs_pin=Pin(3), dc_pin=Pin(29), reset_pin=p, busy_pin=Pin(5), use_partial_buffer=True)

    else:
        p = Pin(2, Pin.OUT) #To restet the epd
        epdSPI = SPI(2, sck=Pin(12), baudrate=400000, mosi=Pin(13), miso=None) #SPI instance fpr E-paper display (miso Pin necessary for SoftSPI, but not needed)
        epd = EPDPico(rotation=90, spi=epdSPI, cs_pin=Pin(10), dc_pin=Pin(09), reset_pin=p, busy_pin=Pin(11), use_partial_buffer=True) #Epaper setup (instance of EINK)
    
    import time
    
    '''   
    epd.text('hello', 19, 19)
    epd.ellipse(200, 200, 90, 90, f=True)
    #epd.invert_ram()
    epd.show()
    time.sleep(3)
    epd.partial_mode_on()
    epd.text('PIPI CACA', 30, 30)
    epd.show()
    epd.fill()
    epd.ellipse(60,60,10,10,f = True)
    epd.show(x=80, y=10)
    epd.rect(50,100,50,10,f=True)
    epd.show()
    epd.partial_mode_off()
    epd.sleep()
    time.sleep(2)
    epd.part.text('SAPERLIPOPETE', 100, 20) #ne fonctionne pas encore
    epd.eco_show()
    '''
    import numr110V
    
    c = numr110V.get_ch('5')
    epd.partial_mode_on(c[2], c[1])
    epd._buffer_bw = bytearray(c[0])
    epd.show(179,0)







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