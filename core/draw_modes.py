from core.EinkBase import EinkBase
import core.draw as draw
import framebuf

class Framebuf_mode(EinkBase):

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

# --------------------------------------------------------
# Drawing routines (directly to the display).
# --------------------------------------------------------
#
# bw_ram parameter can be False to use 2 different buffers under monochrome (self.monoc) mode or to send the drawing
# to the differential (eraser) buffer under partial update mode.

# self._sqr = image width square to byte layout of gates of the display
# not self._sqr = image width aligned with the bytes of the display
# bytes of the display are usually aligned with the side where the chip is (the mirror rectangle in the white goo)

class Direct_mode(EinkBase):
    #import core.draw as draw
    # This mode has no transparency, if you need it, use Framebuf_mode, at least for the first full update.
    # In desparation you can always do a partial update to create the overlap of shapes

    def __init__(self):
        pass

    def _set_pframe(self, x, y, h, w):
        pass

    def _send_bw(self, buff):
        self._send_command(0x24)
        self._send_data(buff)

    def _send_red(self, buff):
        self._send_command(0x26)
        self._send_data(buff)

    def _color_sort(self, c):
        if c >> 1:
            pass
        else:
            pass

    def _disp_xy(self, x, y):
        if self._rotation == 0 or 180:
            return x, y
        else:
            return y, x

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
        if not self._sqr:
            draw.elps(xr,yr,f,m)
        else:
            draw.elps(yr, xr, f, m)

    def poly(self, x, y, coords, c=black, f=False):
        pass

    def text(self, text, font, x, y, c=black):
        # you need to give a font as the display doesn't have one by default
        # more like a sequential img() function
        # takes font_to_py fonts
        pass

    def img(self, x, y, buf, w, h, dif = None, invert= False):
        # very similar to buff mode show(x,y)
        # set frame
        # set cursor
        # send buff
        self.width = w if w <= x or x == 0 else w + x
        pass

    # function for setting x y and cursor every time

    def show(self):  # previously show_ram
        self._ld_norm_lut()
        self._send_command(0x20)
        self._read_busy()
