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
            cls.xspan = [0, screen_w//8]
            cls.yspan = [0, screen_h]
        else:
            # making sure the span is within the screen
            cls.xspan[0] = max(cls.xspan[0], 0)
            cls.xspan[1] = min(cls.xspan[1], screen_w // 8)
            cls.yspan[0] = max(cls.yspan[0], 0)
            cls.yspan[1] = min(cls.yspan[1], screen_h)

        print(f"x span = {cls.xspan}, y span = {cls.yspan}")

        background = 0xff if background else 0x00

        row_w = screen_w//8 if full else cls.c_width()
        total_height = cls.c_height() if not full else screen_h
        cls.main_row_pointer = cls.yspan[0]
        for line in range(total_height):
            row = bytearray([background]*row_w)
            for obj in cls.blkl:
                if (obj.ram_flag & ram_chk) and obj.y + obj.row_pointer == cls.main_row_pointer and obj.row_pointer < obj.height:
                    first_x = max(0, obj.actual_x // 8) if full else max(0, obj.actual_x //8 - cls.xspan[0])
                    key_m[k+1](row, next(obj._gen), first_x)
                    obj.row_pointer += 1
            for obj in cls.whtl:
                if (obj.ram_flag & ram_chk) and obj.y + obj.row_pointer == cls.main_row_pointer and obj.row_pointer < obj.height:
                    first_x = max(0, obj.actual_x // 8) if full else max(0, obj.actual_x //8 - cls.xspan[0])
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

    def __init__(self, x, y, hor, color):
        self.x = x
        self.y = y
        self.c = color
        self.cc = color & 1
        self.actual_x = x - x%8 if hor else y - y%8
        self.actual_y = y if hor else x
        self.hor = hor
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
        if Drawable.xspan[1] is None or (self.actual_x + self.x%8 + self.width + 7) // 8 > Drawable.xspan[1]:
            Drawable.xspan[1] = (self.actual_x + self.x%8 + self.width + 7) // 8
        if Drawable.yspan[0] is None or self.y < Drawable.yspan[0]:
            Drawable.yspan[0] = self.actual_y
        if Drawable.yspan[1] is None or self.y + self.height > Drawable.yspan[1]:
            Drawable.yspan[1] = self.actual_y + self.height

class Pixel(Drawable):
    def __init__(self, x, y, color, hor):
        super().__init__(x, y, hor, color)
        self.byte = 0
        self.actual_x = self.x - self.x%8 if self.hor else self.x
        self.actual_y = self.y - self.y%8 if not self.hor else self.y
        self.setup()
        self._parse()

    @property
    def width(self):
        return 8 if self.hor else 1

    @property
    def height(self):
        return 1 if self.hor else 8

    def setup(self):
        sh = self.x%8 if self.hor else self.y%8
        self.byte = 0xff ^ (1 << (7-sh)) if not self.cc else 1 << (7-sh)

    def draw(self):
        yield bytearray([self.byte])

class StrLine(Drawable):
    # Still have to do the vertical version
    def __init__(self, x, y, span, c, orientation, hor):
        super().__init__(x, y, hor, c)
        self.span = span
        self.orientation = orientation
        if self.orientation not in ('h', 'v'):
            raise ValueError('orientation must be either "h" or "v"')
        self.fn = self.aligned_l() if self.orientation.lower() == 'h' and self.hor or self.orientation.lower() == 'v' and not self.hor else self.sqr_l()
        print(self.fn)
        self.first = self.x % 8 if self.hor else self.y % 8
        self.actual_x = self.x - bool(self.first)*8 if self.hor else self.x
        self.actual_y = self.y - bool(self.first)*8 if not self.hor else self.y
        self._parse()
        #self.setup()

    def setup(self):
        pass

    @property
    def height(self): # absolute
        if self.hor:
            if self.orientation is 'h':
                return 1
            if self.orientation is 'v':
                return self.span
        if not self.hor:
            if self.orientation is 'h':
                return 8
            if self.orientation is 'v':
                return self.span//8+bool(self.span%8)
        return None

    @property
    def width(self): # absolute
        if self.hor:
            if self.orientation is 'h':
                return self.span//8+bool(self.span%8)
            if self.orientation is 'v':
                return 8
        if not self.hor:
            if self.orientation is 'h':
                return self.span
            if self.orientation is 'v':
                return 1
        return None

    @micropython.native
    def aligned_l(self)-> object:
        line = bytearray()
        first = int(self.first)
        
        if first:
            a = 0 if self.cc else 0xff
            for i in range(first):
                if self.cc:
                    a |= 1 << i
                else:
                    a ^= 1 << i
            line.append(a)
        if sp - first:
            full = (self.span-first)//8
            b = 0x00 if self.cc else 0xff
            for i in range(full):
                line.append(b)
        rem = (self.span - first)%8
        if rem:
            a = 0 if self.cc else 0xff
            for i in range(rem):
                if self.cc:
                    a |= 1 << (7-i)
                else:
                    a ^= 1 << (7-i)
            line.append(a)
        yield line

    def sqr_l(self) -> object:
        # lines perpendicular to the display bytes
        b = self.cc << ( 7 - self.first ) if not self.cc else 0xff ^ (7-self.first)
        for i in range(self.span):
            yield bytearray([b])

    def draw(self):
        yield from self.fn


class ABLine(Drawable):
    # Lacks the possibility of drawing lines in different quadrants
    def __init__(self, x1, y1, x2, y2, c, hor):
        super().__init__(x1, y1, hor, c)
        self.x2 = x2
        self.y2 = y2
        self.w = x2 - x1
        self.h = y2 - y1
        self.first = x1 % 8 if hor else y1 % 8
        self.rem = (x2 - x1 - self.first) % 8 if hor else (y2 - y1 - self.first) % 8
        self.actual_x = x1 - self.first if hor else x1
        self.actual_y = y1 if hor else y1 - self.first
        self._parse()

    @property
    def width(self):
        return self.w - self.first - self.rem + (bool(self.first) + bool(self.rem)) * 8 if self.hor else self.w

    @property
    def height(self):
        return self.h if self.hor else self.h - self.first - self.rem + (bool(self.first) + bool(self.rem)) * 8

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
            if self.hor:
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
        byte_width = self.width // 8 if self.hor else self.height // 8
        for x_points in grouped_points:
            if x_points:
                bline = bytearray([bkgrd] * byte_width)
                for pt in x_points:
                    if self.hor:
                        bline[pt // 8] = bline[pt // 8] | 1 << (pt % 8) if self.cc else bline[pt // 8] ^ 1 << (pt % 8)
                    else:
                        bline[pt//8] = bline[pt // 8] | 1 << ( 7 - ( pt % 8 )) if self.cc else bline[pt//8] ^ 1 << ( 7 - ( pt % 8 ))
                yield bline


class Rect(Drawable):
    # not working for vertical rectangles yet
    def __init__(self, x, y, height, width, color, hor, f= True):
        super().__init__(x, y, hor, color)
        self.h = height
        self.w = width
        self.f = f
        self.first = self.x % 8 if self.hor else self.y % 8
        self.rem = (self.w - self.first)%8 if self.hor else (self.h - self.first)%8
        self.actual_x = self.x - self.first if self.hor else self.x
        self.actual_y = self.y - self.first if not self.hor else self.y
        self.setup()
        self._parse()

    @property
    def width(self):
        return self.w - self.first- self.rem + bool(self.rem)*8 + bool(self.first)*8 if self.hor else self.w

    @property
    def height(self):
        return self.h if self.hor else self.h - self.first- self.rem + bool(self.rem) + bool(self.first)

    def setup(self):
        pass

    def draw(self):
        fline = bytearray()
        full = (self.w - self.first) // 8

        if self.first:
            a = 0 if self.cc else 0xff
            for i in range(8-self.first+1):
                if self.cc:
                    a |= 1 << i
                else:
                    a ^= 1 << i
            fline.append(a)
        if self.w-self.first:
            b = 0xff if self.cc else 0x00
            for i in range(full):
                fline.append(b)
        if self.rem:
            a = 0 if self.cc else 0xff
            for i in range(8-self.rem+1):
                a = a | 1 << (8-i) if self.cc else a ^ 1 <<(8-i)
            fline.append(a)
        mid = self.h-2
        yield fline
        if not self.f:
            line = bytearray()
            line.append(1 << (8-self.first) if self.cc else 0xff ^ 1 << (8-self.first))
            for byte in range(full):
                line.append(0x00) if self.cc else line.append(0xff)
            line.append(1 << self.rem if self.cc else 0xff ^ 1 << self.rem)

            if mid:
                for i in range(mid):
                    yield line
        else:
            for i in range(mid):
                yield fline
        yield fline
        #yield bytearray([0x00]*((self.w+7)//8+1)) Je ne sais pas pourquoi j'ai mis ça là

class Ellipse(Drawable):
    def __init__(self,xradius, yradius, x, y, color, hor, f = False, m = 0b1111):
        self.xr = xradius
        self.yr = yradius
        self.fill = f
        self.m = m
        super().__init__(x, y, hor, color)
        #self.setup()
        self._parse()

    @property
    def width(self):
        return 2*self.xr+1 if self.hor else 2*self.yr+1

    @property
    def height(self):
        return 2*self.yr+1 if self.hor else 2*self.xr+1

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
    def __init__(self, st, font, x, y, hor, spacing = 2, fixed_w = False, color = 0, invert = True):
        super().__init__(x, y, hor, color)
        self.st = st
        self.spacing = spacing
        self.fixed_w = fixed_w if fixed_w != 'max' else font.max_width()
        self.font = font
        self.chr_l = []
        self.w_l = bytearray()
        self.shift = self.x%8 if self.hor else self.y%8
        self.invert = invert

        if self.fixed_w and self.fixed_w < self.font.max_width():
            raise ValueError(f"fixed_width should be equal to or greater than the font's max_width, use 'max' to use that value instead")

        self.setup()
        self._parse()

    @property
    def width(self):
        ttl = 0 if self.hor else self.font.height()
        if self.hor:
            nb = int(len(self.w_l)/2)
            ttl+= sum(unpack(f'{int(nb)}H', self.w_l)) if not self.fixed_w else self.fixed_w*nb
            ttl += self.spacing * (nb-1)
        return ttl

    @property
    def height(self):
        ttl = 0 if not self.hor else self.font.height()
        if not self.hor:
            nb = int(len(self.w_l) / 2)
            ttl += sum(unpack(f'{nb}H', self.w_l)) if not self.fixed_w else self.fixed_w * nb
            ttl += self.spacing * (nb - 1)
        return ttl

    @property
    def bwidth(self): # just width works if x is not already a multiple of 8
        """ byte width """
        return ((self.shift+self.width+7)//8)*8 if self.hor else self.font.height()

    @property
    def bheight(self):
        """ byte height """
        return self.font.height() if self.hor else ((self.shift+self.height+7)//8)*8

    def setup(self):
        for ltr in self.st:
            gl = self.font.get_ch(ltr)
            self.chr_l.append(gl[0])
            self.w_l.extend(pack('H', gl[2]))

    def draw(self):
        if self.hor:
            for ln in range(self.height):
                args = []
                for f in range(len(self.chr_l)):
                    w = (unpack('H',self.w_l[f*2:f*2+2])[0]+7)//8
                    line = memoryview(self.chr_l[f][ln*w:ln*w+w])
                    args.append(line)
                yield self.linec(*args)
        else: # Vertical
            for e, elem in enumerate(self.chr_l):
                delta = self.fixed_w - self.w_l[e*2:e*2+2] if self.fixed_w else 0
                for line in l_by_l(elem, self.font.height(), unpack('H', self.w_l[e*2:e*2+2])[0]): #TODO
                    if self.invert:
                        line = self.invert_bytes(line)
                    yield line if not self.shift else shiftr(line, self.shift)

                if bool(self.spacing + delta ) & bool(e < len(self.chr_l) -1 ):
                    for _ in range(self.spacing + delta):
                        yield bytearray(self.bwidth)

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
    def __init__(self, x, y, h, w, buff, hor, color):
        super().__init__(x, y, hor, color)
        self.buff = buff
        self.h = h
        self.w = w
        self.setup()
        self.first = self.x % 8 if self.hor else self.y % 8
        self.rem = (self.w - self.first) % 8 if self.hor else (self.h - self.first) % 8
        self.actual_x = self.x - self.first if self.hor else self.x
        self.actual_y = self.y - self.first if not self.hor else self.y
        self._parse()

    @property
    def width(self):
        return self.w + self.first + self.rem if self.hor else self.h + self.first + self.rem

    @property
    def height(self):
        return self.h if self.hor else self.w

    def setup(self):
        pass

    def draw(self):
        yield shiftr(l_by_l(self.buff, self.w, self.h), self.first) if self.hor else shiftr(l_by_l(self.buff, self.h, self.w), self.first)

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

def grid_print(row: list):
    """ For testing purposes """
    for byte in row:
        for bit in range(8):
            print('□' if byte & (1 << (7 - bit)) else '■', end='')
    print()

if __name__ is '__main__':
    import numr110H, freesans20

    txt = ChainBuff("20 mai 1993", freesans20, 11, 20, True, 0, False, invert = True)
    txt.ram_flag = 1
    #lll = Ellipse(10, 10, 100,0, 0,True, False)
    #lll.ram_flag = 1
    #ln = Rect(3, 10, 39, 20, 0, 0, True)
    #ln.ram_flag = 1
    lin= StrLine(45, 10,40, 0, 'v', True)
    lin.ram_flag = 1
    d = Drawable.draw_all(480,280, black_ram = True)
    #d = lin.draw()
    for i in d:
        grid_print(i)