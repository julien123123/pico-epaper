from core.EinkBase import EinkBase
import core.draw as draw
# --------------------------------------------------------
# Drawing routines (directly to the display).
# --------------------------------------------------------
#
# bw_ram parameter can be False to use 2 different buffers under monochrome (self.monoc) mode or to send the drawing
# to the differential (eraser) buffer under partial update mode.

# self._sqr = image width square to byte layout of gates of the display
# not self._sqr = image width aligned with the bytes of the display
# bytes of the display are usually aligned with the side where the chip is (the mirror rectangle in the white goo)

BW1B = const(0) # black and white with 1 buffer in black and white ram

BW2X = const(1) # black and white with 2 copy of the same buffer in black and white ram and red ram

BW2B = const(2) # black and white with 2 different buffers in black and white and red ram
# BW2B works with ping pong buffers, where 2 buffers get shown and updated alternately, and partial mode, where red ram
# is used to erase the black ram. In that case, red ram is not necessarily updated.

G2B = const(3)  # grayscale with 2 different buffers in black and white and red ram

class DirectMode:

    def __init__(self, eink, mode):
        self.Eink = eink
        self.ram_fl= 0
        self.mode = mode

    def _set_frame(self):
        minx, maxx = draw.Drawable.xspan
        miny, maxy = draw.Drawable.yspan
        self.Eink._set_window(minx, maxx-1, miny, maxy)
        self.Eink._set_cursor(minx+1, miny)

    def _color_sort(self, key):
        self.Eink._send_command(0x24)
        if self.mode == BW2X:
            buf = bytearray()
            for chunk in draw.Drawable.draw_all(self.Eink.width, self.Eink.height, full= True, black_ram=True, k=key):
                buf.extend(chunk)
            self.Eink._send_buffer(buf)
            self.Eink._send_command(0x26)
            self.Eink._send_buffer(buf)
        else:
            if self.ram_fl & 0b01:
                for ba in draw.Drawable.draw_all(self.Eink.width, self.Eink.height, full=not self.Eink._partial, black_ram=True, k=key):
                    self.Eink._send_data(ba)
            if self.ram_fl & 0b10:
                draw.Drawable.second_color() if self.mode is G2B else None
                draw.Drawable.reset() if self.ram_fl & 0b01 else None
                self.Eink._send_command(0x26)
                for ba in draw.Drawable.draw_all(self.Eink.width, self.Eink.height, full=not self.Eink._partial, red_ram=True, k=key):
                    self.Eink._send_data(ba)

    def _ram_logic(self, obj, diff):
        if self.mode in (BW1B, G2B, BW2X) or (self.mode is BW2B and not diff):
            obj.ram_flag |= 0b01
            self.ram_fl |= 0b01
        if self.mode is G2B or (self.mode is BW2B and diff):
            obj.ram_flag |= 0b10
            self.ram_fl |= 0b10

    #To be rewritten
    @micropython.native
    def fill(self, c=None, bw_ram=True):
        c = 1 if not c else c
        bbytes = 0xff if c & 1 else 0x00
        self._send_bw(bytearray([bbytes] * ((self.sqr_side + 7) * self.ic_side // 8))) if bw_ram else None
        if not self._partial and not self.monoc or not bw_ram:
            rbytes = 0xff if c >> 1 else 0x00
            self._send_red(bytearray([bbytes] * ((self.sqr_side + 7) * self.ic_side // 8)))

    def pixel(self, x, y, c=None, diff = False):
        c = self.Eink.black if not c else c
        d = draw.Pixel(x, y, c, not self.Eink._sqr)
        self._ram_logic(d, diff)

    def hline(self, x, y, w, c=None, diff = False):
        c = self.Eink.black if not c else c
        d = draw.StrLine(x, y, w, c, 'h', not self.Eink._sqr)
        self._ram_logic(d, diff)

    def vline(self, x, y, h, c=None, diff = False):
        c = self.Eink.black if not c else c
        d = draw.StrLine(x, y, h, c, 'v', not self.Eink._sqr)
        self._ram_logic(d, diff)

    def line(self, x1, y1, x2, y2, c=None, diff = False):
        c = self.Eink.black if not c else c
        d = draw.ABLine(x1, y1, x2, y2, c, not self.Eink._sqr)
        self._ram_logic(d, diff)

    def rect(self, x, y, w, h, c=None, f=False, diff = False):
        c = self.Eink.black if not c else c
        d = draw.Rect(x, y, w, h, c, not self.Eink._sqr, f)
        self._ram_logic(d, diff)

    def ellipse(self, x, y, xr, yr, c=None, f=False, m=15, diff = False):
        c = self.Eink.black if not c else c
        d = draw.Ellipse(x, y, xr, yr, c, not self.Eink._sqr, f, m)
        self._ram_logic(d, diff)

    def poly(self, x, y, coords, c=None, f=False):
        raise NotImplementedError
        #c = self.Eink.black if not c else c
        #pass

    def text(self, text, font, x, y, c=None, spacing = False, fixed_width = False, diff = False, invert = True):
        #x y are always at the top left of the text line
        c = self.Eink.black if not c else c
        d = draw.ChainBuff(text, font, x, y, hor = not self.Eink._sqr, spacing = spacing, fixed_w = fixed_width, color = c, invert = invert)
        self._ram_logic(d, diff)

    def img(self, x, y, buf, w, h, ram = 0, invert= False, diff = False):
        d = draw.Prerendered(x, y, h, w, buf, not self.Eink._sqr, 1)
        self._ram_logic(d, diff)

    def show(self, flush = True, key = -1):  # previously show_ram
        self._set_frame()
        self._color_sort(key)
        self.Eink._updt_ctrl_2()
        self.Eink._ld_norm_lut(0)
        self.Eink._send_command(0x20)
        self.Eink._read_busy()
        self.ram_fl = 0
        draw.Drawable.flush() if flush else None
