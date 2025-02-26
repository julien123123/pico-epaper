import core.draw as draw
from core.draw import Drawable

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

    def __init__(self, eink, mode, hor):
        self.Eink = eink
        self.ram_fl= 0
        self.mode = mode
        self.hor = hor

        draw.Drawable.hor = self.hor

    def _set_frame(self):
        """Note: The -1 are to account for the 1 pixel having address 0 (instead of 1 like when we count pixels)"""
        seq = self.Eink.cur_seq & 0b11
        xspan = draw.Drawable.xspan
        yspan = draw.Drawable.yspan

        # xspan is already in bytes, no need for *8 multiplication
        minx = xspan[0]
        maxx = xspan[1]

        if seq == 0:  # bottom right (180)
            minx, maxx = self.Eink._virtual_width(self.Eink.ic_side - 1 - minx * 8), self.Eink._virtual_width(self.Eink.ic_side - 1 - maxx * 8)
            miny, maxy = self.Eink.sqr_side - 1 - yspan[0], self.Eink.sqr_side - 1 - yspan[1]
        elif seq == 1:  # bottom left (270)
            minx, maxx = self.Eink._virtual_width(minx * 8), self.Eink._virtual_width(maxx * 8)
            miny, maxy = self.Eink.sqr_side - 1 - yspan[0], self.Eink.sqr_side - 1 - yspan[1]
        elif seq == 2:  # top right (90)
            minx, maxx = self.Eink._virtual_width(self.Eink.ic_side - 1 - minx * 8), self.Eink._virtual_width(self.Eink.ic_side - 1 - maxx * 8)
            miny, maxy = yspan[0], yspan[1]
        else:  # 3 top left (0)
            minx, maxx = self.Eink._virtual_width(minx * 8), self.Eink._virtual_width(maxx * 8)
            miny, maxy = yspan[0], yspan[1]

        self.Eink._set_window(minx, maxx, miny, maxy)
        self.Eink._set_cursor(minx, miny)

    def _color_sort(self, key):
        self.Eink._send_command(0x24)
        if self.mode == BW2X:
            buf = bytearray()
            for chunk in draw.Drawable.draw_all(key, black_ram=True):
                buf.extend(chunk)
            self.Eink._send_data(buf)
            self.Eink._send_command(0x26)
            self.Eink._send_data(buf)
        else:
            if self.ram_fl & 0b01:
                for ba in draw.Drawable.draw_all(key, black_ram=True):
                    self.Eink._send_data(ba)
            if self.ram_fl & 0b10:
                draw.Drawable.second_color() if self.mode is G2B else None
                draw.Drawable.reset() if self.ram_fl & 0b01 else None
                self.Eink._send_command(0x26)
                for ba in draw.Drawable.draw_all(key, red_ram=True):
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
    def fill(self,x = None, y = None, w =None, h = None, c = 1, key=-1, invert = False, diff = True):
        d = None
        if c in (0,1):
            Drawable.background[diff] = 0xff if c else 0
        else:
            d = draw.Filler(x , y , w , h , color= c, key=key, invert= invert) #send this to the display
        if d is not None:
            self._ram_logic(d, diff)

    def pixel(self, x, y, c=None, diff = False):
        c = self.Eink.black if not c else c
        d = draw.Pixel(x, y, c)
        self._ram_logic(d, diff)

    def hline(self, x, y, w, c=None, diff = False):
        c = self.Eink.black if not c else c
        d = draw.StrLine(x, y, w, c, 'h')
        self._ram_logic(d, diff)

    def vline(self, x, y, h, c=None, diff = False):
        c = self.Eink.black if not c else c
        d = draw.StrLine(x, y, h, c, 'v')
        self._ram_logic(d, diff)

    def line(self, x1, y1, x2, y2, c=None, diff = False):
        c = self.Eink.black if not c else c
        d = draw.ABLine(x1, y1, x2, y2, c)
        self._ram_logic(d, diff)

    def rect(self, x, y, w, h, c=None, f=False, diff = False):
        c = self.Eink.black if not c else c
        d = draw.Rect(x, y, w, h, c, f)
        self._ram_logic(d, diff)

    def ellipse(self, x, y, xr, yr, c=None, f=False, m=15, diff = False):
        c = self.Eink.black if not c else c
        d = draw.Ellipse(x, y, xr, yr, c, f, m)
        self._ram_logic(d, diff)

    def poly(self, x, y, coords, c=None, f=False):
        raise NotImplementedError
        #c = self.Eink.black if not c else c
        #pass

    def text(self, text, font, x, y, c=None, spacing = False, fixed_width = False, diff = False, invert = True, v_rev = True):
        #x y are always at the top left of the text line
        c = self.Eink.black if not c else c
        d = draw.ChainBuff(text, font, x, y, spacing = spacing, fixed_w = fixed_width, color = c, invert = invert, v_rev=v_rev)
        self._ram_logic(d, diff)

    def blit(self, x, y, buf, w, h, ram = 0, invert= False, diff = False, reverse = False):
        d = draw.Prerendered(x, y, h, w, buf, 1, invert=invert, reverse=reverse)
        self._ram_logic(d, diff)

    def show(self,full = False, flush = True, key = -1):
        draw.Drawable.set_span(self.Eink.ic_side, self.Eink.sqr_side, full)
        self._set_frame()
        self._color_sort(key)
        self.Eink._updt_ctrl_2()
        self.Eink._ld_norm_lut() if not self.Eink._partial else self.Eink._ld_part_lut()
        self.Eink._send_command(0x20)
        self.Eink._read_busy()
        setattr(self, 'ram_fl', 0) if flush else None
        draw.Drawable.flush() if flush else None

    def export(self, full = False, flush = True, key = -1, bw = True, red = False):
        """Returns the results of Drawable.draw_all in a buffer"""
        draw.Drawable.set_span(self.Eink.ic_side, self.Eink.sqr_side, full)
        buf_bw = (bytearray(b''.join(draw.Drawable.draw_all(key, black_ram=True))), draw.Drawable.c_width(), draw.Drawable.c_height()) if bw else False
        buf_red = (bytearray(b''.join(draw.Drawable.draw_all(key, red_ram=True))), draw.Drawable.c_width(), draw.Drawable.c_height()) if red else False

        setattr(self, 'ram_fl', 0) if flush else None
        draw.Drawable.flush() if flush else None
        return buf_bw, buf_red

    def send_to_disp(self, full= False, flush = True, key = -1):
        """Function to send the current buffer to the display without triggering an update"""
        draw.Drawable.set_span(self.Eink.ic_side, self.Eink.sqr_side, full)
        self._set_frame()
        self._color_sort(key)
        setattr(self, 'ram_fl', 0) if flush else None
        draw.Drawable.flush() if flush else None
