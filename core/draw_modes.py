from core.EinkBase import EinkBase
import core.draw as draw
import framebuf

"""Direct draw should have a option to send the buffers to ram instead of the display"""

RAM_BW  = const(0b01)
RAM_RED = const(0b10)
RAM_RBW = const(0b11)

class DrawMode:
    def __init__(self, Eink):
        self.Eink = Eink

    def fill(self):
        raise NotImplementedError

    def pixel(self):
        raise NotImplementedError

    def hline(self):
        raise NotImplementedError

    def vline(self):
        raise NotImplementedError

    def line(self):
        raise NotImplementedError

    def rect(self):
        raise NotImplementedError

    def ellipse(self):
        raise NotImplementedError

    def text(self):
        raise NotImplementedError

class FbfMode(DrawMode):
    def __init__(self, eink):
        if self.Eink._sqr:
            self.width = self.Eink.ic_side
            self.height = self.Eink.sqr_side
            self.buf_format = framebuf.MONO_HLSB
        else:
            self.width = self.Eink.sqr_side
            self.height = self.Eink.ic_side
            self.buf_format = framebuf.MONO_VLSB
        super().__init__(self, eink)

    @property  # for allowing to lazily load the frame buffers
    def bw(self):
        if not self._bw:
            pad = 0 if self.width in (self.Eink.sqr_side, self.Eink.ic_side) else 17
            self._buffer_bw_actual = bytearray((self.width + pad) * self.height // 8)
            self._bw_actual = framebuf.FrameBuffer(self._buffer_bw_actual, self.width, self.height, self.buf_format)
            # Alias buffer and FrameBuffer to indicate which buffer should be treated as BW RAM buffer.
            self._buffer_bw = self._buffer_bw_actual
            self._bw = self._bw_actual
            self._bw.fill(1)
        return self._bw

    @property
    def red(self):
        if not self._red and not self.Eink.monoc:
            pad = 0 if self.width in (self.Eink.sqr_side, self.Eink.ic_side) else 7
            self._buffer_red = bytearray((self.width + pad) * self.height // 8)
            self._red = framebuf.FrameBuffer(self._buffer_red, self.width, self.height, self.buf_format)
            self._red.fill(1)
        return self._red

    @property
    def part(self):
        if self._use_partial_buffer and not self._part:
            pad = 0 if self.width in (self.Eink.sqr_side, self.Eink.ic_side) else 17
            self._buffer_partial = bytearray((self.width + pad) * self.height // 8)
            self._part = framebuf.FrameBuffer(self._buffer_partial, self.width, self.height, self.buf_format)
            self._part.fill(1)
        return self._part
    # --------------------------------------------------------
    # Drawing routines (wrappers for FrameBuffer methods).
    # --------------------------------------------------------

    def fill(self, c=None):
        c = self.Eink.white if not c else c
        self.bw.fill(c & 1)
        if not self._partial and not self.monoc:
            self.red.fill(c >> 1)

    def pixel(self, x, y, c=None):
        c = self.Eink.black if not c else c
        self.bw.pixel(x, y, c & 1)
        if not self._partial:
            self.red.pixel(x, y, c >> 1)

    def hline(self, x, y, w, c=None):
        c = self.Eink.black if not c else c
        self.bw.hline(x, y, w, c & 1)
        if not self._partial and not self.monoc:
            self.red.hline(x, y, w, c >> 1)

    def vline(self, x, y, h, c=None):
        c = self.Eink.black if not c else c
        self.bw.vline(x, y, h, c & 1)
        if not self._partial:
            self.red.vline(x, y, h, c >> 1)

    def line(self, x1, y1, x2, y2, c=None):
        c = self.Eink.black if not c else c
        self.bw.line(x1, y1, x2, y2, c & 1)
        if not self._partial and not self.monoc:
            self.red.line(x1, y1, x2, y2, c >> 1)

    def rect(self, x, y, w, h, c=None, f=False):
        c = self.Eink.black if not c else c
        self.bw.rect(x, y, w, h, c & 1, f)
        if not self._partial and not self.monoc:
            self.red.rect(x, y, w, h, c >> 1, f)

    def ellipse(self, x, y, xr, yr, c=None, f=False, m=15):
        c = self.Eink.black if not c else c
        self.bw.ellipse(x, y, xr, yr, c & 1, f, m)
        if not self._partial and not self.monoc:
            self.red.ellipse(x, y, xr, yr, c >> 1, f, m)

    def poly(self, x, y, coords, c=None, f=False):
        c = self.Eink.black if not c else c
        self.bw.poly(x, y, coords, c & 1, f)
        if not self._partial and not self.monoc:
            self.red.poly(x, y, coords, c >> 1, f)

    def text(self, text, x, y, c=None):
        c = self.Eink.black if not c else c
        self.bw.text(text, x, y, c & 1)
        if not self._partial and not self.monoc:
            self.red.text(text, x, y, c >> 1)

    def blit(self, fbuf, x, y, key=-1, palette=None, ram=RAM_RBW):
        if ram & 1 == 1 or self._partial:
            self.bw.blit(fbuf, x, y, key, palette)
        if (ram >> 1) & 1 == 1:
            self.red.blit(fbuf, x, y, key, palette)

# --------------------------------------------------------
# Drawing routines (directly to the display).
# --------------------------------------------------------
#
# bw_ram parameter can be False to use 2 different buffers under monochrome (self.monoc) mode or to send the drawing
# to the differential (eraser) buffer under partial update mode.

# self._sqr = image width square to byte layout of gates of the display
# not self._sqr = image width aligned with the bytes of the display
# bytes of the display are usually aligned with the side where the chip is (the mirror rectangle in the white goo)

class DirectMode(DrawMode):

    # This mode has no transparency, if you need it, use Framebuf_mode, at least for the first full update.
    # In desparation you can always do a partial update to create the overlap of shapes
    """
    Works to show stuff in partial mode, but nothing is showing proprely; the dimmensions are off. ok, stuff shows proprely
    when it's at 0,0, but non multiples of 8 don't show proprely. Maybe ther's something related to me changing the width and stuff
    ellipse funtion says it can't allocate memory with draw2 and draw22.
    Ping pong should be disabled in partial update for this mode as it prevents us from using a differential image.

    Ah, seems that height and width properties are in pixels, not bytes. maybe I should add a property for the width in bytes
    """

    def __init__(self, eink):
        super().__init__(eink)

    def _set_frame(self, x, y, h, w):
        """Setting the ram frame for each element"""
        absx, absy = self._abs_xy(x, y)
        self.Eink._set_window(self.Eink._virtual_width(absx), self.Eink._virtual_width(absx+w), absy, absy+h) #This is a test, just to try the rest of this library
        '''
        self.Eink._set_frame(absx, absy, h, w) # ça serait plus _set_window(), mais il faut que ça se traduit de relatif à ab
        # ou changer pour _set_frame et setter le widh et height de la classe Eink
        '''
        self.Eink._set_cursor(absx, absy)

    def _send_bw(self, buff):
        self.Eink._send_command(0x24)
        self.Eink._send_data(buff)

    def _send_red(self, buff):
        self.Eink._send_command(0x26)
        self.Eink._send_data(buff)

    def _color_sort(self,buf, c, diff):
        self._send_bw(buf) if not diff else None
        if diff or (not self.Eink._partial and not self.Eink.monoc):
            self._send_red(buf)

    def _to_disp(self,buf, x, y, h, w, c, diff):
        self._set_frame(x, y, h, w)
        self._color_sort(buf, c, diff)

    def _to_ram(self):
        pass

    def _abs_xy(self, rel_x, rel_y):
        """:returns absolute display coordinates"""
        x, y = (rel_y, rel_x) if (self.Eink.cur_seq >> 2) & 1 else (rel_x, rel_y)
        seq = self.Eink.cur_seq & 0b11
        abs_x, abs_y = 0, 0
        if not seq:
            abs_x = self.Eink.ic_side - x
            abs_y = self.Eink.sqr_side - y
        elif seq == 1:
            abs_x = x
            abs_y = self.Eink.sqr_side - y
        elif seq == 2:
            abs_x = self.Eink.ic_side - x
            abs_y = y
        else:  # seq == 3
            abs_x = x
            abs_y = y
        return abs_x, abs_y

    @micropython.native
    def fill(self, c=None, bw_ram=True):
        c = self.white if not c else c
        bbytes = 0xff if c & 1 else 0x00
        self._send_bw(bytearray([bbytes] * ((self.sqr_side + 7) * self.ic_side // 8))) if bw_ram else None
        if not self._partial and not self.monoc or not bw_ram:
            rbytes = 0xff if c >> 1 else 0x00
            self._send_red(bytearray([bbytes] * ((self.sqr_side + 7) * self.ic_side // 8)))

    def pixel(self, x, y, c=None, diff = False):
        c = self.Eink.black if not c else c
        ob = draw.Pixel(x, y, c, not self.Eink._sqr)
        d = ob.draw()
        self._to_disp(d, x, y, ob.height, ob.width, c, diff)

    def hline(self, x, y, w, c=None, diff = False):
        c = self.Eink.black if not c else c
        ob = draw.StrLine(x, y, w, c, 'h', not self.Eink._sqr)
        d = ob.draw()
        self._to_disp(d, x, y, ob.height, ob.width, c, diff)

    def vline(self, x, y, h, c=None, diff = False):
        c = self.Eink.black if not c else c
        ob = draw.StrLine(x, y, h, c, 'v', not self.Eink._sqr)
        d = ob.draw()
        self._to_disp(d, x, y, ob.height, ob.width, c, diff)

    def line(self, x1, y1, x2, y2, c=None, diff = False):
        c = self.Eink.black if not c else c
        ob = draw.ABLine(x1, y1, x2, y2, c, not self.Eink._sqr)
        d = ob.draw()
        self._to_disp(d, x, y, ob.height, ob.width, c, diff)

    def rect(self, x, y, w, h, c=None, f=False, diff = False):
        c = self.Eink.black if not c else c
        ob = draw.Rect(x, y, w, h, c, not self.Eink._sqr, f)
        d = ob.draw()
        b = bytearray()
        for i in d:
            b.extend(i)
        self._to_disp(b, x, y, ob.height, ob.width, c, diff)

    def ellipse(self, x, y, xr, yr, c=None, f=False, m=15, diff = False):
        c = self.Eink.black if not c else c
        ob = draw.Ellipse(x, y, xr, yr, c, not self.Eink._sqr, f, m)
        d = ob.draw22() # need to try before commiting to one of the draw methods
        b = bytearray()
        for i in range(ob.height):
            b.extend(next(d))
        #for i in d:
        #    b.extend(i)
        self._to_disp(b, x, y, ob.height, ob.width, c, diff)

    def poly(self, x, y, coords, c=None, f=False):
        c = self.Eink.black if not c else c
        pass

    def text(self, text, font, x, y, c=None, spacing = False, fixed_width = False, diff = False):
        #x y are always at the top left of the text line
        c = self.Eink.black if not c else c
        ob = draw.ChainBuff(text, font, x, y, not self.Eink._sqr,  spacing, fixed_width)
        d = ob.draw()
        b = bytearray()
        for i in d:
            b.extend(i)
        self._to_disp(b, x, y, ob.bheight, ob.bwidth, c, diff)

    def img(self, x, y, buf, w, h, ram = RAM_BW, invert= False, diff = False):
        sh_buf = False

        if self.Eink._sqr:
            first = y % 8
            rem = (w + first)%8
            actual_x = y - first
            width = h + first + rem
            actual_y = x
            height = w
        else:
            first = x % 8
            rem = (w + first)%8
            actual_x = x - first
            width = w + first + rem
            actual_y = y
            height = h

        if first:
            l = draw.l_by_l(buf, w, h)
            sh_buf = bytearray()
            for ln in range(height):
                sh_buf.extend(draw.shiftr(next(l), first))

        self.Eink._set_frame(actual_x, actual_y, width, height)
        self.Eink._set_cursor(actual_x, actual_y)

        if ram & 1 and not diff:
            self._send_bw(buf) if not sh_buf else self._send_bw(sh_buf)
        if diff or (ram >> 1 & 1):
            self._send_red(buf) if not sh_buf else self._send_red(sh_buf)


    # function for setting x y and cursor every time

    def show(self):  # previously show_ram
        self.Eink._updt_ctrl_2()
        self.Eink._ld_norm_lut(0)
        self.Eink._send_command(0x20)
        self.Eink._read_busy()
