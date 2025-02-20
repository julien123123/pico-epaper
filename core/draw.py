import micropython
import utime
from struct import pack, unpack

def timed_function(f, *args, **kwargs):
    print(f)
    myname = str(f).split(' ')[0]
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func

class Drawable:
    hor = True #not sure how to define it in the main Eink class, but it makes more sense to make it a class variable
    blkl = []
    whtl = []
    main_row_pointer = 0
    xspan = [None, None]
    yspan = [None, None]

    @classmethod
    def c_width(cls):
        return cls.xspan[1] - cls.xspan[0]

    @classmethod
    def c_height(cls):
        return cls.yspan[1] - cls.yspan[0]

    @classmethod
    def draw_all(cls, screen_w: int, screen_h: int, k: int = -1,  full: bool = False, background :int = 1, red_ram: bool = False, black_ram: bool = False)-> object:
        key_m = (cls.k_none, cls.k_0, cls.k_1)
        if red_ram and black_ram:
            raise ValueError('Cannot draw on both red and black ram at the same time')
        ram_chk = black_ram + (red_ram << 1) # reducing the amount of checks for ram
        if full:
            cls.xspan = [0, screen_w//8-1]
            cls.yspan = [0, screen_h-1]
        else:
            # making sure the span is within the screen
            cls.xspan[0] = max(cls.xspan[0], 0)
            cls.xspan[1] = min(cls.xspan[1], screen_w // 8-1)
            cls.yspan[0] = max(cls.yspan[0], 0)
            cls.yspan[1] = min(cls.yspan[1], screen_h-1)

        print(f"x span = {cls.xspan}, y span = {cls.yspan}")
        background = 0xff if background else 0x00
        row_w = cls.c_width()+1
        total_height = cls.c_height()+1
        cls.main_row_pointer = cls.yspan[0]

        for line in range(total_height):
            row = bytearray([background]*row_w)
            for obj in cls.blkl:
                if (obj.ram_flag & ram_chk) and obj.actual_y + obj.row_pointer == cls.main_row_pointer and obj.row_pointer < obj.height:
                    first_x = max(0, obj.actual_x //8 - cls.xspan[0])
                    key_m[k+1](row, next(obj._gen), first_x)
                    obj.row_pointer += 1
            for obj in cls.whtl:
                if (obj.ram_flag & ram_chk) and obj.actual_y + obj.row_pointer == cls.main_row_pointer and obj.row_pointer < obj.height:
                    first_x = max(0, obj.actual_x //8 - cls.xspan[0])
                    key_m[k+1](row, next(obj._gen), first_x)
                    obj.row_pointer += 1
            cls.main_row_pointer += 1
            yield row

    @micropython.viper
    @staticmethod
    def k_none(row: object, objline: object, first_x: int) -> ptr8:
        for ind in range(int(len(objline))):
            if int(first_x + ind) >= int(len(row)):
                break
            row[first_x + ind] = int(objline[ind])

    @micropython.viper
    @staticmethod
    def k_0(row: object, objline: object, first_x: int) -> ptr8:
        for ind in range(int(len(objline))):
            if int(first_x + ind) >= int(len(row)):
                break
            row[first_x + ind] = int(row[first_x + ind]) & int(objline[ind])

    @micropython.viper
    @staticmethod
    def k_1(row: object, objline: object, first_x: int) -> ptr8:
        for ind in range(int(len(objline))):
            if int(first_x + ind) >= int(len(row)):
                break
            row[first_x + ind] = int(row[first_x + ind]) | int(objline[ind])

    @classmethod
    def flush(cls):
        cls.blkl = []
        cls.whtl = []
        cls.main_row_pointer = 0
        cls.xspan = [None, None]
        cls.yspan = [None, None]

    @classmethod
    def reset(cls):
        cls.main_row_pointer = 0
        for obj in cls.blkl:
            obj.reset_draw()
        for obj in cls.whtl:
            obj.reset_draw()

    @classmethod
    def second_color(cls):
        for obj in cls.blkl:
            obj.cc = obj.c >> 1 & 1
        for obj in cls.whtl:
            obj.cc = obj.c >> 1 & 1

    # BASIC DRAWABLE CLASS TO BE INHERITED BY ALL OTHER CLASSES

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.c = color
        self.cc = color & 1
        self.shift = x%8 if Drawable.hor else y%8
        self.actual_x = x - self.shift if Drawable.hor else y - self.shift
        self.actual_y = y if Drawable.hor else x
        self.row_pointer = 0
        self._gen = self.draw()
        self.ram_flag = 0b00

    @property
    def width(self):
        raise NotImplementedError
    @property
    def height(self):
        raise NotImplementedError

    def setup(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def seek(self, point):
        if point < 0:
            raise ValueError('point must be greater than 0')
        if point > self.height:
            raise ValueError('point must be less than the height of the object')
        self.row_pointer = point

    def reset_draw(self):
        self.setup()
        self._gen = self.draw()
        self.seek(0)

    def _parse(self):
        if self.cc == 1:
            Drawable.whtl.append(self)
        else:
            Drawable.blkl.append(self)

        if Drawable.xspan[0] is None or self.actual_x // 8 < Drawable.xspan[0]:
            Drawable.xspan[0] = self.actual_x // 8
        if Drawable.xspan[1] is None or (self.actual_x + self.shift + self.width + 7) // 8 > Drawable.xspan[1]:
            Drawable.xspan[1] = (self.actual_x + self.shift + self.width + 7) // 8
        if Drawable.yspan[0] is None or self.actual_y < Drawable.yspan[0]:
            Drawable.yspan[0] = self.actual_y
        if Drawable.yspan[1] is None or self.actual_y + self.height > Drawable.yspan[1]:
            Drawable.yspan[1] = self.actual_y + self.height

class Pixel(Drawable):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.byte = 0
        self.setup()
        self._parse()

    @property
    def width(self):
        return 1

    @property
    def height(self):
        return 1

    def setup(self):
        self.byte = 0xff ^ (1 << (7-self.shift)) if not self.cc else 1 << (7-self.shift)

    def draw(self):
        yield bytearray([self.byte])

class StrLine(Drawable):
    # Still have to do the vertical version
    def __init__(self, x, y, span, c, orientation):
        super().__init__(x, y, c)
        self.span = span
        self.orientation = orientation
        self.rem = (self.span + self.shift) % 8
        if self.orientation not in ('h', 'v'):
            raise ValueError('orientation must be either "h" or "v"')
        self.fn = self.aligned_l() if self.orientation.lower() == 'h' and Drawable.hor or self.orientation.lower() == 'v' and not Drawable.hor else self.sqr_l()
        print(self.fn)
        self._parse()
        #self.setup()

    def setup(self):
        pass

    @property
    def height(self): # absolute
        if Drawable.hor:
            if self.orientation is 'h':
                return 1
            if self.orientation is 'v':
                return self.span
        if not Drawable.hor:
            if self.orientation is 'h':
                return self.span
            if self.orientation is 'v':
                return 1
        return None

    @property
    def width(self): # absolute
        if Drawable.hor :
            if self.orientation is 'h':
                return self.span
            if self.orientation is 'v':
                return 1
        if not Drawable.hor :
            if self.orientation is 'h':
                return 1
            if self.orientation is 'v':
                return self.span
        return None

    @micropython.native
    def aligned_l(self)-> object:
        bwidth = (self.shift + self.span + 7) // 8
        fline = bytearray([0 if self.cc else 0xff] * bwidth)
        first_byte_mask = ((1 << min(8 - self.shift, self.span)) - 1) << (8 - self.shift - min(8 - self.shift, self.span))
        fline[0] = first_byte_mask if self.cc else 0xff ^ first_byte_mask
        if bwidth > 1:
            if self.rem:  # Only apply mask if there are remaining bits
                last_byte_mask = (1 << self.rem) - 1 << (8 - self.rem)
                fline[-1] = last_byte_mask if self.cc else 0xff ^ last_byte_mask
            else:  # When rem=0, we want a full byte
                fline[-1] = 0xff if self.cc else 0x00
        if len(fline) > 2:
            fline[1:-1] = bytearray([0xff if self.cc else 0x00] * len(fline[1:-1]))
        yield fline if Drawable.hor else reverse_bits(fline)

    def sqr_l(self) -> object:
        # lines perpendicular to the display bytes
        for i in range(self.span):
            b = bytearray([1 << (7-self.shift)]) if self.cc else bytearray([0xff ^ (1 << (7-self.shift))])
            yield b if Drawable.hor else reverse_bits(b)

    def draw(self):
        yield from self.fn


class ABLine(Drawable):
    # Lacks the possibility of drawing lines in different quadrants
    def __init__(self, x1, y1, x2, y2, c):
        super().__init__(x1, y1, c)
        self.x2 = x2
        self.y2 = y2
        self.w = x2 - x1
        self.h = y2 - y1
        self.rem = (x2 - x1 - self.shift) % 8 if Drawable.hor else (y2 - y1 - self.shift) % 8
        self._parse()

    @property
    def width(self):
        return self.w - self.shift - self.rem + (bool(self.shift) + bool(self.rem)) * 8 if Drawable.hor  else self.w

    @property
    def height(self):
        return self.h if Drawable.hor  else self.h - self.shift - self.rem + (bool(self.shift) + bool(self.rem)) * 8

    def setup(self):
        pass

    def bresenham(self):
        """
        Bresenham's Line Algorithm.
        """
        dx = abs(self.x2 - self.x)
        dy = abs(self.y2 - self.y)
        sx = 1 if self.x < self.x2 else -1
        sy = 1 if self.y < self.y2 else -1
        err = dx - dy
        x1, y1 = self.x, self.y
        while True:
            if Drawable.hor :
                yield x1 - self.actual_x, y1 - self.actual_y  # Plot the current pixel relative to actual_x and actual_y
            else:
                yield y1 - self.actual_y, x1 - self.actual_x
            if x1 == self.x2 and y1 == self.y2:  # Exit when the end point is reached
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw(self):
        points = [p for p in self.bresenham()]
        max_y = max(y for _, y in points)
        grouped_points = [[] for _ in range(max_y + 1)]
        for x, y in points:
            grouped_points[y].append(x)
        bkgrd = 0 if self.cc else 0xff
        byte_width = self.width // 8 if Drawable.hor  else self.height // 8
        for x_points in grouped_points:
            if x_points:
                bline = bytearray([bkgrd] * byte_width)
                for pt in x_points:
                    if Drawable.hor :
                        bline[pt // 8] = bline[pt // 8] | 1 << (pt % 8) if self.cc else bline[pt // 8] ^ 1 << (pt % 8)
                    else:
                        bline[pt//8] = bline[pt // 8] | 1 << ( 7 - ( pt % 8 )) if self.cc else bline[pt//8] ^ 1 << ( 7 - ( pt % 8 ))
                yield reverse_bits(bline)


class Rect(Drawable):
    # not working for vertical rectangles yet
    def __init__(self, x, y, height, width, color, f= True):
        super().__init__(x, y, color)
        self.h = height
        self.w = width
        self.f = f
        self.rem = (self.shift+self.w)%8 if Drawable.hor  else (self.shift+self.h)%8
        self.setup()
        self._parse()

    @property
    def width(self):
        return self.w if Drawable.hor else self.h

    @property
    def height(self):
        return self.h if Drawable.hor  else self.w

    def setup(self):
        pass

    def draw(self):
        bwidth = (self.shift + self.w + 7) // 8 if Drawable.hor else (self.shift + self.h + 7) // 8
        fline = bytearray([0 if self.cc else 0xff] * bwidth)
        mid = self.h - 2 if Drawable.hor else self.w - 2

        first_byte_mask = ((1 << min(8 - self.shift, self.w)) - 1) << (8 - self.shift - min(8 - self.shift, self.w))
        fline[0] = first_byte_mask if self.cc else 0xff ^ first_byte_mask

        if bwidth > 1:
            if self.rem:  # Only apply mask if there are remaining bits
                last_byte_mask = (1 << self.rem) - 1 << (8 - self.rem)
                fline[-1] = last_byte_mask if self.cc else 0xff ^ last_byte_mask
            else:  # When rem=0, we want a full byte
                fline[-1] = 0xff if self.cc else 0x00

        if len(fline) > 2:
            fline[1:-1] = bytearray([0xff if self.cc else 0x00] * len(fline[1:-1]))

        yield fline if Drawable.hor else reverse_bits(fline)
        if not self.f and mid:
            line = bytearray([0x00 if self.cc else 0xff]*bwidth)
            line[0] = line[0] | 1 << (7-self.shift) if self.cc else line[0] ^ 1 << (7-self.shift)
            line[-1] = line[-1] | 1 << (7-(self.rem-1)%8) if self.cc else line[-1] ^ 1 << (7-(self.rem-1)%8)

            for i in range(mid):
                yield line if Drawable.hor else reverse_bits(line)
        else:
            for i in range(mid):
                yield fline if Drawable.hor else reverse_bits(fline)
        yield fline if Drawable.hor else reverse_bits(fline)


class Ellipse(Drawable):
    def __init__(self,xradius, yradius, x, y, color, f = False, m = 0b1111):
        self.xr = xradius
        self.yr = yradius
        self.fill = f
        self.m = m
        super().__init__(x, y, color)
        #self.setup()
        self._parse()

    @property
    def width(self):
        return 2*self.xr+1 if Drawable.hor  else 2*self.yr+1

    @property
    def height(self):
        return 2*self.yr+1 if Drawable.hor  else 2*self.xr+1

    def setup(self):
        """:returns a list of lists of points where y is the index of the list"""
        points = [[] for _ in range(2 * self.yr + 1)]

        def in_quadrant(px, py, quadrant_mask):
            if px >= 0 and py <= 0:  # Q1 (top-right)
                return quadrant_mask & 0b0001
            if px <= 0 and py <= 0:  # Q2 (top-left)
                return quadrant_mask & 0b0010
            if px <= 0 and py >= 0:  # Q3 (bottom-left)
                return quadrant_mask & 0b0100
            if px >= 0 and py >= 0:  # Q4 (bottom-right)
                return quadrant_mask & 0b1000
            return False

        # Midpoint Ellipse Algorithm
        x, y = 0, self.yr
        x_radius2 = self.xr * self.xr
        y_radius2 = self.yr * self.yr
        x_radius2y_radius2 = x_radius2 * y_radius2
        dx = 2 * y_radius2 * x
        dy = 2 * x_radius2 * y

        # Region 1
        d1 = y_radius2 - (x_radius2 * self.yr) + (0.25 * x_radius2)
        while dx < dy:
            if self.fill:
                # Fill horizontal line between points
                for px in range(-x, x + 1):
                    if in_quadrant(px, y, self.m):
                        points[self.yr - y].append(self.xr + px)
                    if in_quadrant(px, -y, self.m):
                        points[self.yr + y].append(self.xr + px)
            else:
                # Draw boundary points
                if in_quadrant(x, y, self.m):
                    points[self.yr - y].append(self.xr + x)
                if in_quadrant(-x, y, self.m):
                    points[self.yr - y].append(self.xr - x)
                if in_quadrant(x, -y, self.m):
                    points[self.yr + y].append(self.xr + x)
                if in_quadrant(-x, -y, self.m):
                    points[self.yr + y].append(self.xr - x)

            if d1 < 0:
                x += 1
                dx += 2 * y_radius2
                d1 += dx + y_radius2
            else:
                x += 1
                y -= 1
                dx += 2 * y_radius2
                dy -= 2 * x_radius2
                d1 += dx - dy + y_radius2

        # Region 2
        d2 = (y_radius2 * (x + 0.5) * (x + 0.5)) + (x_radius2 * (y - 1) * (y - 1)) - x_radius2y_radius2
        while y >= 0:
            if self.fill:
                # Fill horizontal line between points
                for px in range(-x, x + 1):
                    if in_quadrant(px, y, self.m):
                        points[self.yr - y].append(self.xr + px)
                    if in_quadrant(px, -y, self.m):
                        points[self.yr + y].append(self.xr + px)
            else:
                # Draw boundary points
                if in_quadrant(x, y, self.m):
                    points[self.yr - y].append(self.xr + x)
                if in_quadrant(-x, y, self.m):
                    points[self.yr - y].append(self.xr - x)
                if in_quadrant(x, -y, self.m):
                    points[self.yr + y].append(self.xr + x)
                if in_quadrant(-x, -y, self.m):
                    points[self.yr + y].append(self.xr - x)

            if d2 > 0:
                y -= 1
                dy -= 2 * x_radius2
                d2 += x_radius2 - dy
            else:
                y -= 1
                x += 1
                dx += 2 * y_radius2
                dy -= 2 * x_radius2
                d2 += dx - dy + x_radius2

        return points

    @micropython.native
    def draw(self):
        points = self.setup()
        bkgrd = 0 if self.cc else 0xff
        byte_width = (self.width + 7) // 8
        for x_points in points:
            if x_points:
                bline = bytearray([bkgrd] * byte_width)
                for pt in x_points:
                    bline[pt // 8] = bline[pt // 8] | (1 << (7 - (pt % 8))) if self.cc else bline[pt//8] ^ (1 << (7-(pt%8)))
                yield bline


class ChainBuff(Drawable): #mainly for writing fonts
    """ajouter implémentation de fixed width pour vertical"""
    def __init__(self, st, font, x, y, spacing = 2, fixed_w = False, color = 0, invert = True):
        super().__init__(x, y, color)
        self.st = st
        self.spacing = spacing
        self.fixed_w = fixed_w if fixed_w != 'max' else font.max_width()
        self.font = font
        self.chr_l = []
        self.w_l = bytearray()
        self.invert = invert

        if self.fixed_w and self.fixed_w < self.font.max_width():
            raise ValueError(f"fixed_width should be equal to or greater than the font's max_width, use 'max' to use that value instead")

        self.setup()
        self._parse()

    @property
    def width(self):
        ttl = 0 if Drawable.hor  else self.font.height()
        if Drawable.hor :
            nb = int(len(self.w_l)/2)
            ttl+= sum(unpack(f'{int(nb)}H', self.w_l)) if not self.fixed_w else self.fixed_w*nb
            ttl += self.spacing * (nb-1)
        return ttl

    @property
    def height(self):
        ttl = 0 if not Drawable.hor  else self.font.height()
        if not Drawable.hor :
            nb = int(len(self.w_l) / 2)
            ttl += sum(unpack(f'{nb}H', self.w_l)) if not self.fixed_w else self.fixed_w * nb
            ttl += self.spacing * (nb - 1)
        return ttl

    @property
    def bwidth(self): # just width works if x is not already a multiple of 8
        """ byte width """
        return ((self.shift+self.width+7)//8)*8 if Drawable.hor  else self.font.height()

    @property
    def bheight(self):
        """ byte height """
        return self.font.height() if Drawable.hor  else ((self.shift+self.height+7)//8)*8

    def setup(self):
        for ltr in self.st:
            gl = self.font.get_ch(ltr)
            self.chr_l.append(gl[0])
            self.w_l.extend(pack('H', gl[2]))

    def draw(self):
        if Drawable.hor :
            for ln in range(self.height):
                args = []
                for f in range(len(self.chr_l)):
                    w = (unpack('H',self.w_l[f*2:f*2+2])[0]+7)//8
                    line = memoryview(self.chr_l[f][ln*w:ln*w+w])
                    args.append(line)
                yield self.linec(*args)
        else: # Vertical
            bkg = 0 if self.cc else 0xff
            for e, elem in enumerate(self.chr_l):
                w = unpack('H', self.w_l[e*2:e*2+2])[0]
                delta = self.fixed_w - w if self.fixed_w else 0
                for line in l_by_l(elem, self.font.height(), w):
                    if self.invert:
                        line = self.invert_bytes(line)
                    yield line if not self.shift else shiftl(line, self.shift)

                if bool(self.spacing + delta ) & bool(e < len(self.chr_l) -1 ):
                    for _ in range(self.spacing + delta):
                        yield bytearray([bkg]*self.bwidth)

    @micropython.native
    def linec(self,*linesw:object)->object:
        cursor:int = int(self.shift)
        r:object = bytearray([0 if self.cc else 0xff]*int(self.bwidth-1)) #complete row
        for dx, lines in enumerate(linesw):
            width:int = int(unpack('H', self.w_l[dx*2:dx*2+2])[0])
            if dx>0:
                cursor += int(self.spacing)
                if cursor%8:
                    row:object = shiftr(lines, cursor%8)
                    first:int = int(cursor)//8
                    r[first] = int(r[first]) | int(row[0]) # This works for font_to_py fonts, but might not for other fonts
                    r[first+1:first+int(len(row))] = row[1:]
                else:
                    r[cursor//8:cursor//8+int(len(lines))] = lines[:]
            else:
                row:object = shiftr(lines, self.shift) if self.shift else lines
                r[0:int(len(row))] = row[:]
            cursor += width if not self.fixed_w else self.fixed_w
        ba: object = r if not self.invert else self.invert_bytes(r)
        return ba
    #@micropython.viper
    @staticmethod
    def invert_bytes(ba: object) -> object:
        return bytearray(~b & 0xFF for b in ba)

    def reset_draw(self):
        self.chr_l = []
        self.w_l = bytearray()
        super().reset_draw()


class Prerendered(Drawable):
    def __init__(self, x, y, h, w, buff, color):
        super().__init__(x, y, color)
        self.buff = buff
        self.h = h
        self.w = w
        self.setup()
        self.rem = (self.w - self.shift) % 8 if Drawable.hor  else (self.h - self.shift) % 8
        self._parse()

    @property
    def width(self):
        return self.w + self.shift + self.rem if Drawable.hor  else self.h + self.shift + self.rem

    @property
    def height(self):
        return self.h if Drawable.hor  else self.w

    def setup(self):
        pass

    def draw(self):
        yield shiftr(l_by_l(self.buff, self.w, self.h), self.shift) if Drawable.hor  else shiftr(l_by_l(self.buff, self.h, self.w), self.shift)

@micropython.native
def l_by_l(buf, w, h):
    width = w//8 if w%8 == 0 else w//8+1
    for i in range(h):
        yield buf[i*width:i*width+width]

@micropython.viper
def shiftr( ba: object, val: int) -> object:
    if val <0:
        raise ValueError('Number of bits must be positive')
    if val == 0:
        return ba
    byteshift = val//8
    bitshift = val % 8
    lenba = int(len(ba))
    result = bytearray(lenba+byteshift+ (1 if bitshift > 0 else 0))
    carry = 0
    for i in range(lenba):
        result[i + byteshift] = (int(ba[i]) >> bitshift) | carry
        carry = (int(ba[i]) & ((1 << bitshift) -1)) << (8-bitshift)
    if int(carry) > 0:
        result[lenba+byteshift] = carry
    return result

@micropython.viper
def shiftl(ba:object, val:int) -> object:
    if val < 0:
        raise ValueError('Number of bits must be positive')
    if val == 0:
        return ba
    byteshift = val // 8
    bitshift = val % 8
    lenba = int(len(ba))
    result = bytearray(lenba + byteshift + (1 if bitshift > 0 else 0))
    carry = 0
    for i in range(lenba):
        result[i + byteshift] = (int(ba[i]) << bitshift) | carry
        carry = int(ba[i]) >> (8 - bitshift)
    if carry:
        result[lenba + byteshift] = carry
    return result

@micropython.viper
def reverse_bits(ba: object) -> object:
    r = bytearray(int(len(ba)))
    for i in range(int(len(ba))):
        r[i] = REVERSE_LUT[int(ba[i])]
    return r

def grid_print(row: list):
    """ For testing purposes """
    for byte in row:
        for bit in range(8):
            print('□' if byte & (1 << (7 - bit)) else '■', end='')
    print()

# LUT for inverting bytes
REVERSE_LUT = b'\x00\x80\x40\xc0\x20\xa0\x60\xe0\x10\x90\x50\xd0\x30\xb0\x70\xf0' \
              b'\x08\x88\x48\xc8\x28\xa8\x68\xe8\x18\x98\x58\xd8\x38\xb8\x78\xf8' \
              b'\x04\x84\x44\xc4\x24\xa4\x64\xe4\x14\x94\x54\xd4\x34\xb4\x74\xf4' \
              b'\x0c\x8c\x4c\xcc\x2c\xac\x6c\xec\x1c\x9c\x5c\xdc\x3c\xbc\x7c\xfc' \
              b'\x02\x82\x42\xc2\x22\xa2\x62\xe2\x12\x92\x52\xd2\x32\xb2\x72\xf2' \
              b'\x0a\x8a\x4a\xca\x2a\xaa\x6a\xea\x1a\x9a\x5a\xda\x3a\xba\x7a\xfa' \
              b'\x06\x86\x46\xc6\x26\xa6\x66\xe6\x16\x96\x56\xd6\x36\xb6\x76\xf6' \
              b'\x0e\x8e\x4e\xce\x2e\xae\x6e\xee\x1e\x9e\x5e\xde\x3e\xbe\x7e\xfe' \
              b'\x01\x81\x41\xc1\x21\xa1\x61\xe1\x11\x91\x51\xd1\x31\xb1\x71\xf1' \
              b'\x09\x89\x49\xc9\x29\xa9\x69\xe9\x19\x99\x59\xd9\x39\xb9\x79\xf9' \
              b'\x05\x85\x45\xc5\x25\xa5\x65\xe5\x15\x95\x55\xd5\x35\xb5\x75\xf5' \
              b'\x0d\x8d\x4d\xcd\x2d\xad\x6d\xed\x1d\x9d\x5d\xdd\x3d\xbd\x7d\xfd' \
              b'\x03\x83\x43\xc3\x23\xa3\x63\xe3\x13\x93\x53\xd3\x33\xb3\x73\xf3' \
              b'\x0b\x8b\x4b\xcb\x2b\xab\x6b\xeb\x1b\x9b\x5b\xdb\x3b\xbb\x7b\xfb' \
              b'\x07\x87\x47\xc7\x27\xa7\x67\xe7\x17\x97\x57\xd7\x37\xb7\x77\xf7' \
              b'\x0f\x8f\x4f\xcf\x2f\xaf\x6f\xef\x1f\x9f\x5f\xdf\x3f\xbf\x7f\xff'

if __name__ is '__main__':
    import numr110V, freesans20V
    Drawable.hor = False
    br = ABLine(0,0, 30, 10, 0)
    br.ram_flag = 1
    #txt = ChainBuff("Allo", freesans20V, 0, 0, False, False, 0, invert = False)
    #txt.ram_flag = 1
    #t= ChainBuff("33", numr110V, 4, 48, False, 0, invert = True)
    #t.ram_flag = 1
    #p = Pixel(90, 5, 0)
    #p.ram_flag = 1
    #lll = Ellipse(20, 10, 7,0, 0,False, 15)
    #lll.ram_flag = 1
    #ln = Rect(19, 10, 10, 20, 0, False)
    #ln.ram_flag = 1
    #lin= StrLine(0, 0,20, 0, 'h')
    #lin.ram_flag = 1
    d = Drawable.draw_all(100,100, full= False, black_ram = True)
    #d = t.draw()
    for i in d:
        grid_print(i) if Drawable.hor else grid_print(reversed(i))