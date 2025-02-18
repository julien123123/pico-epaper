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
# This mode might only work because in normal update mode, the white in bw ram is opaque, and the black is
# transparent to what's in the red ram voiding red ram achieves the same thing. Many of the drivers I found
# used this formula for full updates. That's why I included it here.

BW2B = const(2) # black and white with 2 different buffers in black and white and red ram
# BW2B works with ping pong buffers, where 2 buffers get shown and updated alternately, and partial mode, where red ram
# is used to erase the black ram. In that case, red ram is not necessarily updated.

G2B = const(3)  # grayscale with 2 different buffers in black and white and red ram

class DirectMode:

    def __init__(self, eink, mode):
        self.Eink = eink
        self.ram_fl= 0
        self.mode = mode

    def _set_frame(self, full):
        minx, maxx = draw.Drawable.xspan if not full else (0, self.Eink.width//8)
        miny, maxy = draw.Drawable.yspan if not full else (0, self.Eink.height)
        self.Eink._set_window(self.Eink._virtual_width(minx*8), self.Eink._virtual_width(maxx*8)-1, miny, maxy)
        self.Eink._set_cursor(self.Eink._virtual_width(minx*8), miny)

    def _color_sort(self, full, key):
        self.Eink._send_command(0x24)
        if self.mode == BW2X:
            buf = bytearray()
            for chunk in draw.Drawable.draw_all(self.Eink.width, self.Eink.height, key, full, black_ram=True):
                buf.extend(chunk)
            self.Eink._send_data(buf)
            self.Eink._send_command(0x26)
            self.Eink._send_data(buf)
        else:
            if self.ram_fl & 0b01:
                for ba in draw.Drawable.draw_all(self.Eink.width, self.Eink.height, full=full, black_ram=True, k=key):
                    self.Eink._send_data(ba)
            if self.ram_fl & 0b10:
                draw.Drawable.second_color() if self.mode is G2B else None
                draw.Drawable.reset() if self.ram_fl & 0b01 else None
                self.Eink._send_command(0x26)
                for ba in draw.Drawable.draw_all(self.Eink.width, self.Eink.height, full=full, red_ram=True, k=key):
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

    def blit(self, x, y, buf, w, h, ram = 0, invert= False, diff = False):
        d = draw.Prerendered(x, y, h, w, buf, not self.Eink._sqr, 1)
        self._ram_logic(d, diff)

    def show(self,full = False, flush = True, key = -1):
        self._set_frame(full)
        self._color_sort(full,key)
        self.Eink._updt_ctrl_2()
        self.Eink._ld_norm_lut() if not self.Eink._partial else self.Eink._ld_part_lut()
        self.Eink._send_command(0x20)
        self.Eink._read_busy()
        setattr(self, 'ram_fl', 0) if flush else None
        draw.Drawable.flush() if flush else None

    def export(self, full = False, flush = True, key = -1, bw = True, red = False):
        """Returns the results of Drawable.draw_all in a buffer"""
        buf_bw = (bytearray(b''.join(draw.Drawable.draw_all(self.Eink.width, self.Eink.height, key, full, black_ram=True))), draw.Drawable.c_width(), draw.Drawable.c_height()) if bw else False
        buf_red = (bytearray(b''.join(draw.Drawable.draw_all(self.Eink.width, self.Eink.height, key, full, red_ram=True))), draw.Drawable.c_width(), draw.Drawable.c_height()) if red else False

        setattr(self, 'ram_fl', 0) if flush else None
        draw.Drawable.flush() if flush else None
        return buf_bw, buf_red

    def send_to_disp(self, full= False, flush = True, key = -1):
        """Function to send the current buffer to the display without triggering an update"""
        self._set_frame(full)
        self._color_sort(full, key)
        setattr(self, 'ram_fl', 0) if flush else None
        draw.Drawable.flush() if flush else None
