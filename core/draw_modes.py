from core.EinkBase import EinkBase
import core.draw as draw
import framebuf

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

    @property  # for allowing to lazily load the framebuffers
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

    def __init__(self, eink):
        import core.draw as draw

        super().__init__(self,eink)

    def _set_frame(self, x, y, h, w):
        """Setting the ram frame for each element"""
        absx, absy = self._abs_xy(x, y)
        self.Eink._set_frame(absx, absy, h, w)
        self.Eink._set_cursor(absx, absy)

    def _send_bw(self, buff):
        self.Eink._send_command(0x24)
        self.Eink._send_data(buff)

    def _send_red(self, buff):
        self.Eink._send_command(0x26)
        self.Eink._send_data(buff)

    def _color_sort(self, c):
        if c >> 1:
            pass
        else:
            pass

    def _abs_xy(self, rel_x, rel_y):
        """:returns absolute display coordinates"""
        x, y = (rel_y, rel_x) if (self.cur_seq >> 2) & 1 else (rel_x, rel_y)
        seq = self.Eink.cur_seq & 0b11
        abs_x, abs_y = 0, 0
        if not seq:
            abs_x = self.ic_side - x
            abs_y = self.sqr_side - y
        elif seq == 1:
            abs_x = x
            abs_y = self.sqr_side - y
        elif seq == 2:
            abs_x = self.ic_side - x
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

    def pixel(self, x, y, c=black):
        # 1 byte, trouver bonne gate de 8 bit
        # utiliser le << pour tourner le bon pixel
        
        #specify width and height and cursor and stuff
        if self._sqr:
            d = draw.pxl(x, y, False)
            d = d ^ 0xff if c & 1 else d
            self_send_bw(d)
        else:
            d = draw.pxl(x, y, True)

    def hline(self, x, y, w, c=black):
        if not self._sqr:
            self._send_bw(draw.aligned_l(x, y, w, c)) if #colorsort????
        else:
            draw.sqr_l(x,y,w,c)

        # wrapper pour choix fonction ligne dépendament de la rotation dans bytearraydraw
        pass

    def vline(self, x, y, h, c=black):
        if self._sqr:
            draw.aligned_l(x, y, h, c)
        else:
            draw.sqr_l(x, y, h, c)

    def line(self, x1, y1, x2, y2, c=black):
        pass

    def rect(self, x, y, w, h, c=black, f=False):
        pass

    def ellipse(self, x, y, xr, yr, c=black, f=False, m=15):
        if not self.Eink._sqr:
            draw.elps(xr,yr,f,m)
        else:
            draw.elps(yr, xr, f, m)

    def poly(self, x, y, coords, c=black, f=False):
        pass

    def text(self, text, font, x, y, c=black, spacing = False, fixed_width = False):
        #x y are always at the top left of the text line
        t = draw.ChainBuff(text, font, x, y, not self.Eink._sqr,  spacing, fixed_width)

    def img(self, x, y, buf, w, h, dif = None, invert= False):
        # very similar to buff mode show(x,y)
        # set frame
        # set cursor
        # send buff
        self.width = w if w <= x or x == 0 else w + x
        pass

    # function for setting x y and cursor every time

    def show(self):  # previously show_ram
        self.Eink._updt_ctrl_2()
        self.Eink._ld_norm_lut()
        self.Eink._send_command(0x20)
        self.Eink._read_busy()
