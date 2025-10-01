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
    hor = True
    blkl = []
    whtl = []
    fll = []
    main_row_pointer = 0
    xspan = [None, None]
    yspan = [None, None]
    background = [0xff, 0xff]
    set = False

    @classmethod
    def c_width(cls):
        return cls.xspan[1] - cls.xspan[0]

    @classmethod
    def c_height(cls):
        return cls.yspan[1] - cls.yspan[0]

    @classmethod
    def draw_all(cls,  k: int = -1, red_ram: bool = False, black_ram: bool = False)-> object:
        key_m = (cls.k_none, cls.k_0, cls.k_1)
        if red_ram and black_ram:
            raise ValueError('Cannot draw on both red and black ram at the same time')
        ram_chk = black_ram + (red_ram << 1) # reducing the amount of checks for ram
        for fil in cls.fll:
            fil.setup() if fil.ram_flag & ram_chk else None
        print(f"x span = {cls.xspan}, y span = {cls.yspan}")
        row_w = cls.c_width()+1
        total_height = cls.c_height()
        cls.main_row_pointer = cls.yspan[0]

        for line in range(total_height):
            row = bytearray([cls.background[0 if black_ram else 1]]*row_w)
            for obj in cls.blkl + cls.whtl + cls.fll:
                if (obj.ram_flag & ram_chk) and obj.actual_y + obj.row_pointer == cls.main_row_pointer and obj.row_pointer < obj.height:
                    first_x = max(0, obj.actual_x // 8 - cls.xspan[0])
                    nxt = next(obj._gen)
                    key_m[k + 1](row, row_w, nxt, len(nxt), first_x)
                    obj.row_pointer += 1
            cls.main_row_pointer += 1
            yield row

    @micropython.viper
    @staticmethod
    def k_none(row: ptr8, lenro:int, objline: ptr8, lenob:int, first_x: int) -> ptr8:
        for ind in range(lenob):
            if int(first_x + ind) >= lenro:
                break
            row[first_x + ind] = objline[ind]

    @micropython.viper
    @staticmethod
    def k_0(row: ptr8, lenro:int, objline: ptr8, lenob:int, first_x: int) -> ptr8:
        for ind in range(lenob):
            if int(first_x + ind) >= lenro:
                break
            row[first_x + ind] = int(row[first_x + ind]) & objline[ind]

    @micropython.viper
    @staticmethod
    def k_1(row: ptr8, lenro:int, objline: ptr8, lenob:int, first_x: int) -> ptr8:
        for ind in range(lenob):
            if int(first_x + ind) >= lenro:
                break
            row[first_x + ind] = row[first_x + ind] | objline[ind]

    @micropython.viper
    @classmethod
    def draw_all_into(cls, buf:ptr8, lenbuf:int, k:int, red_ram:bool, black_ram:bool) -> int:
        """Draw into an object with buffer protocl. Can be re-run until epmty"""
        key_m = (cls.ik_none, cls.ik_0, cls.ik_1)
        if int(red_ram) and int(black_ram):
            raise ValueError('Cannot draw on both red and black ram at the same time')
        ram_chk = int(black_ram) + (int(red_ram) << 1)  # reducing the amount of checks for ram
        if not cls.set:
            for fil in cls.fll:
                fil.setup() if int(fil.ram_flag) & int(ram_chk) else None
            cls.main_row_pointer = cls.yspan[0]
        print(f"x span = {cls.xspan}, y span = {cls.yspan}")
        row_w = int(cls.c_width()) + 1
        total_height = int(cls.c_height())
        bufh = lenbuf // row_w
        max_buf_h = min(int(bufh), total_height-int(cls.main_row_pointer))
        xspan0 = int(cls.xspan[0])
        cls.set = True

        for line in range(int(max_buf_h)):
            lnst = line*row_w
            for b in range(row_w):
                buf[lnst+b] = int(cls.background[0 if black_ram else 1])
            for obj in cls.blkl + cls.whtl + cls.fll:
                if (int(obj.ram_flag) & ram_chk) and int(obj.actual_y) + int(obj.row_pointer) == int(cls.main_row_pointer) and int(obj.row_pointer) < int(obj.height):
                    first_x = max(0, int(obj.actual_x) // 8 - xspan0)
                    nxt = next(obj._gen)
                    key_m[k + 1](buf, lnst, row_w, nxt, len(nxt), first_x)
                    obj.row_pointer = int(obj.row_pointer) + 1
            cls.main_row_pointer = int(cls.main_row_pointer) + 1
        return row_w*int(max_buf_h)

    @micropython.viper
    @staticmethod
    def ik_none(buf: ptr8, rost:int, lenro:int, objline: ptr8, lenob:int, first_x: int) -> ptr8:
        objst = rost+first_x
        for ind in range(lenob):
            if int(ind) >= lenro:
                break
            buf[objst + ind] = objline[ind]

    @micropython.viper
    @staticmethod
    def ik_0(buf: ptr8, rost:int, lenro:int, objline: ptr8, lenob:int, first_x: int) -> ptr8:
        objst = rost + first_x
        for ind in range(lenob):
            if int(ind) >= lenro:
                break
            buf[objst + ind] = int(buf[objst + ind]) & objline[ind]

    @micropython.viper
    @staticmethod
    def ik_1(buf: ptr8, rost:int, lenro:int, objline: ptr8, lenob:int, first_x: int) -> ptr8:
        objst = rost + first_x
        for ind in range(lenob):
            if int(ind) >= lenro:
                break
            buf[objst + ind] = buf[objst + ind] | objline[ind]

    @classmethod
    def flush(cls):
        cls.blkl = []
        cls.whtl = []
        cls.fll = []
        cls.main_row_pointer = 0
        cls.xspan = [None, None]
        cls.yspan = [None, None]
        cls.background = [0xff, 0xff]
        cls.set = False

    @classmethod
    def reset(cls):
        cls.main_row_pointer = 0
        for obj in cls.blkl:
            obj.reset_draw()
        for obj in cls.whtl:
            obj.reset_draw()
        for fl in cls.fll:
            fl.reset_draw()

    @classmethod
    def second_color(cls):
        for obj in cls.blkl:
            obj.cc = obj.c >> 1 & 1
        for obj in cls.whtl:
            obj.cc = obj.c >> 1 & 1

    @classmethod
    def set_span(cls, screen_w, screen_h, full):
        if full:
            cls.xspan = [0, screen_w//8-1]
            cls.yspan = [0, screen_h-1]
        else:
            # making sure the span is within the screen
            cls.xspan[0] = max(cls.xspan[0], 0)
            cls.xspan[1] = min(cls.xspan[1], screen_w // 8-1)
            cls.yspan[0] = max(cls.yspan[0], 0)
            cls.yspan[1] = min(cls.yspan[1], screen_h-1)

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
        reverse_bits(fline, len(fline)) if not Drawable.hor else None
        yield fline

    def sqr_l(self) -> object:
        # lines perpendicular to the display bytes
        for i in range(self.span):
            b = bytearray([1 << (7-self.shift)]) if self.cc else bytearray([0xff ^ (1 << (7-self.shift))])
            reverse_bits(b, len(b)) if not Drawable.hor else None
            yield b

    def draw(self):
        yield from self.fn

class Poly(Drawable):
    def __init__(self, vert, c, fill, parse = True):
        self.p = vert
        self.xs, self.ys = zip(*self.p)
        self.x = min(self.xs) if Drawable.hor else min(self.ys)
        self.y = min(self.ys) if Drawable.hor else min(self.xs)
        self.fill = fill
        self.nedges = len(self.p)
        super().__init__(self.x , self.y, c)
        self.bwidth = (self.shift + self.width + 7)//8
        #self._fill_polygon()
        self._parse() if parse else None

    @property
    def width(self):
        return max(self.xs) - self.x if Drawable.hor else max(self.ys) - self.y

    @property
    def height(self):
        return max(self.ys) - self.y if Drawable.hor else max(self.xs) - self.x

    def setup(self):
        pass

    def _bresenham_line(self, x0, y0, x1, y1):
        """Bresenham's line algorithm for drawing edges."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            print(x0, y0)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def _fill_polygon(self):
        """Fill polygon using scanline algorithm with an edge table."""
        min_y = self.y
        max_y = max(self.ys)
        edge_table = [[] for _ in range(max_y - min_y + 1)]

        # Build edge table
        for i in range(self.nedges):
            x0, y0 = self.p[i]
            x1, y1 = self.p[(i + 1) % self.nedges]
            if y0 == y1:  # Skip horizontal lines
                continue
            if y0 > y1:  # Ensure y0 < y1
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            dx = (x1 - x0) / (y1 - y0)
            edge_table[y0 - min_y].append((x0, dx, y1))
        # Scanline fill
        active_edges = []
        for y in range(min_y, max_y + 1):
            active_edges.extend(edge_table[y - min_y])
            active_edges = [(x, dx, y_max) for x, dx, y_max in active_edges if y < y_max]
            active_edges.sort()

            for i in range(0, len(active_edges), 2):
                line = bytearray([0 if self.cc else 0xff]*self.bwidth)
                x_start, _, _ = active_edges[i]
                x_end, _, _ = active_edges[i + 1]
                self.linec_fill(line, int(x_start), int(x_end)+1)
                yield line


            active_edges = [(x + dx, dx, y_max) for x, dx, y_max in active_edges]

    @micropython.viper
    def linec_fill(self, line:ptr8, x_start:int, x_end:int)->object:
        start_byte = int(x_start) // 8
        end_byte = int(x_end) // 8
        start_bit = int(x_start) % 8
        end_bit = int(x_end) % 8
        if start_byte == end_byte:
            # Both points are in the same byte
            mask = ((1 << (end_bit - start_bit + 1)) - 1) << (7 - end_bit)
            line[start_byte] = int(line[start_byte]) | mask if int(self.cc) else int(line[start_byte]) ^ mask
        else:
            # Fill first byte
            first_mask = ((1 << (8 - start_bit)) - 1)
            line[start_byte] = line[start_byte] | first_mask if self.cc else line[start_byte] ^ first_mask
            for byte in range(start_byte + 1, end_byte):
                line[byte] = 0xFF if self.cc else 0
            if end_bit > 0:
                last_mask = ~((1 << (7 - end_bit)) - 1)
                line[end_byte] = line[end_byte] | last_mask if self.cc else line[end_byte] ^ last_mask

    @micropython.viper
    def linec_fill7(self, line:ptr8, xst:int, xend:int)->ptr8:
        xbit = xst%8
        xb = xst//8
        line[xb] = int(line[xb]) ^ (1 << (7-xbit))  # Flip bit at xst position

        if xst != xend:
            xebit = xend%8
            xeb = xend//8
            line[xeb] = int(line[xeb]) ^ (1 << (7-xebit))  # Flip bit at xend position

    def draw(self):
        yield from self._fill_polygon()


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
        return self.w if Drawable.hor else self.h

    @property
    def height(self):
        return self.h if Drawable.hor else self.w

    def setup(self):
        pass

    def bresenham(self):
        """
        Bresenham's Line Algorithm yielding one bytearray per row.
        """
        dx = abs(self.x2 - self.x)
        dy = abs(self.y2 - self.y)
        sx = 1 if self.x < self.x2 else -1
        sy = 1 if self.y < self.y2 else -1
        err = dx - dy
        x1, y1 = self.x, self.y

        bkgrd = 0 if self.cc else 0xff
        byte_width = (self.shift + self.width + 7) // 8 if Drawable.hor else (self.shift + self.height + 7) // 8
        current_row = -1
        bline = None

        while True:
            if Drawable.hor:
                x, y = x1 - self.actual_x, y1 - self.actual_y
            else:
                x, y = y1 - self.actual_y, x1 - self.actual_x

            if y != current_row:
                if bline is not None:
                    yield bline
                current_row = y
                bline = bytearray([bkgrd] * byte_width)

            bit_pos = 7 - (x % 8)  # Always use MSB to LSB order
            if self.cc:
                bline[x // 8] |= 1 << bit_pos
            else:
                bline[x // 8] ^= 1 << bit_pos

            if x1 == self.x2 and y1 == self.y2:
                if bline is not None:
                    yield bline
                break

            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw(self):
        yield from self.bresenham()


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
        #reverse_bits(fline, len(fline)) if not Drawable.hor else None
        yield fline
        if not self.f and mid:
            line = bytearray([0x00 if self.cc else 0xff]*bwidth)
            line[0] = line[0] | 1 << (7-self.shift) if self.cc else line[0] ^ 1 << (7-self.shift)
            line[-1] = line[-1] | 1 << (7-(self.rem-1)%8) if self.cc else line[-1] ^ 1 << (7-(self.rem-1)%8)

            for i in range(mid):
                #reverse_bits(line, len(line)) if not Drawable.hor else None
                yield line
        else:
            for i in range(mid):
                yield fline
        yield fline


class Ellipse(Drawable):
    def __init__(self,xradius, yradius, x, y, color, f = False, m = 0b1111):
        self.xr = xradius if Drawable.hor  else yradius
        self.yr = yradius if Drawable.hor  else xradius
        self.fill = f
        self.m = m
        self.points = bytearray((2 * self.yr + 1) * ((2 * self.xr + 8) // 8))
        super().__init__(x, y, color)
        self.setup()
        self._parse()

    @property
    def width(self):
        return 2*self.xr+1
    @property
    def height(self):
        return 2*self.yr+1

    @micropython.native
    def setup(self):
        @micropython.viper
        def set_point(y_idx:int, x_pos:int):
            xr = int(self.xr)
            # Convert x,y coordinates to bit position in bytearray
            row_bytes = (2 * xr + 8) // 8
            byte_idx = y_idx * row_bytes + (xr + x_pos) // 8
            bit_pos = 7 - ((xr + x_pos) % 8)  # MSB first
            self.points[byte_idx] = int(self.points[byte_idx]) | (1 << bit_pos)

        @micropython.viper
        def in_quadrant(px:int, py:int, quadrant_mask:int)->int:
            px, py = int(px), int(py)
            if px >= 0 and py <= 0:  # Q1 (top-right)
                return quadrant_mask & 0b0001
            if px <= 0 and py <= 0:  # Q2 (top-left)
                return quadrant_mask & 0b0010
            if px <= 0 and py >= 0:  # Q3 (bottom-left)
                return quadrant_mask & 0b0100
            if px >= 0 and py >= 0:  # Q4 (bottom-right)
                return quadrant_mask & 0b1000
            return 0

        # Midpoint Ellipse Algorithm
        x, y = 0, int(self.yr)
        x_radius2 = int(self.xr) * int(self.xr)
        y_radius2 = int(self.yr) * int(self.yr)
        x_radius2y_radius2 = x_radius2 * y_radius2
        dx = 2 * y_radius2 * x
        dy = 2 * x_radius2 * y

        # Region 1
        d1 = y_radius2 - (x_radius2 * self.yr) + (0.25 * x_radius2)
        while dx < dy:
            if self.fill:
                # Fill horizontal line between points
                for px in range(-x, x + 1):
                    if in_quadrant(px, y, int(self.m)):
                        set_point(int(self.yr) - y, px)
                    if in_quadrant(px, -y, int(self.m)):
                        set_point(int(self.yr) + y, px)
            else:
                # Draw boundary points
                if in_quadrant(x, y, int(self.m)):
                    set_point(int(self.yr) - y, x)
                if in_quadrant(-x, y, int(self.m)):
                    set_point(int(self.yr) - y, -x)
                if in_quadrant(x, -y, int(self.m)):
                    set_point(int(self.yr) + y, x)
                if in_quadrant(-x, -y, int(self.m)):
                    set_point(int(self.yr) + y, -x)

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
                        set_point(self.yr - y, px)
                    if in_quadrant(px, -y, self.m):
                        set_point(self.yr + y, px)
            else:
                # Draw boundary points
                if in_quadrant(x, y, self.m):
                    set_point(self.yr - y, x)
                if in_quadrant(-x, y, self.m):
                    set_point(self.yr - y, -x)
                if in_quadrant(x, -y, self.m):
                    set_point(self.yr + y, x)
                if in_quadrant(-x, -y, self.m):
                    set_point(self.yr + y, -x)

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

    @micropython.native
    def draw(self):
        #self.setup()
        row_bytes = (2 * self.xr + 8) // 8
        bkgrd = 0 if self.cc else 0xff
        for y in range(2 * self.yr + 1):
            row = self.points[y * row_bytes:(y + 1) * row_bytes]
            if any(row):  # Only yield rows that contain points
                bline = bytearray(row)
                if not self.cc:  # Invert the bits if needed
                    invert_bytes(bline, len(bline))
                yield bline

class ChainBuff(Drawable): #mainly for writing fonts
    """ajouter implémentation de fixed width pour vertical"""
    def __init__(self, st, font, x, y, spacing = 2, fixed_w = False, color = 0, invert = True, v_rev = True):
        super().__init__(x, y, color)
        self.st = st
        self.spacing = spacing
        self.fixed_w = fixed_w if fixed_w != 'max' else font.max_width()
        self.font = font
        self.chr_l = []
        self.w_l = bytearray()
        self.invert = invert
        self.v_rev = v_rev # revert when vertical

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
        return ((self.shift+self.width+7)//8) if Drawable.hor  else self.font.height()

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
                ba = bytearray([0xff if self.cc else 0]*(self.bwidth))
                for f in range(len(self.chr_l)):
                    w = (unpack('H',self.w_l[f*2:f*2+2])[0]+7)//8
                    line = memoryview(self.chr_l[f][ln*w:ln*w+w])
                    args.append(line)
                self.linec2(args, ba)
                invert_bytes(ba, len(ba)) if self.invert else None
                yield ba
        else: # Vertical
            # Seems that since the char buffers are a memoryview, if the letters are not shifted, the only need to be
            # reverted and reversed once. If the same letter comes up again, it will be reverted and reversed again

            bkg = 0 if self.cc else 0xff
            for e, elem in enumerate(self.chr_l):
                w = unpack('H', self.w_l[e*2:e*2+2])[0]
                delta = self.fixed_w - w if self.fixed_w else 0
                for line in l_by_l(elem, self.font.height(), w):
                    line = bytearray(line)
                    reverse_bits(line, len(line)) if self.v_rev else None
                    invert_bytes(line, len(line)) if self.invert else None
                    line = shiftl(line, len(line), self.shift, self.cc) if self.shift else bytearray(line)

                    yield line

                if bool(self.spacing + delta ) & bool(e < len(self.chr_l) -1 ):
                    for _ in range(self.spacing + delta):
                        yield bytearray([bkg]*self.bwidth)


    @micropython.native
    def linec(self,*linesw:object)->object:
        cursor:int = int(self.shift)
        r:object = bytearray([0xff if self.cc else 0]*int(self.bwidth-1)) #complete row
        for dx, lines in enumerate(linesw):
            width:int = int(unpack('H', self.w_l[dx*2:dx*2+2])[0])
            if dx>0:
                cursor += int(self.spacing)
                if cursor%8:
                    row:object = shiftr(lines, len(lines), cursor%8, self.cc)
                    first:int = int(cursor)//8
                    r[first] = int(r[first]) | int(row[0]) # This works for font_to_py fonts, but might not for other fonts
                    r[first+1:first+int(len(row))] = row[1:]
                else:
                    r[cursor//8:cursor//8+int(len(lines))] = lines[:]
            else:
                row:object = shiftr(lines, len(lines), self.shift, self.cc) if self.shift else lines
                r[0:int(len(row))] = row[:]
            cursor += width if not self.fixed_w else self.fixed_w
        invert_bytes(r, len(r)) if self.invert else None # Invert the bytes in r object, no need to create a new one
        #reverse_bits(r, len(r))
        return r

    @micropython.viper
    def linec2(self,linesw:object, ba:ptr8)->object:
        ptr8(self.w_l)
        cursor:int = int(self.shift)
        for dx, lines in enumerate(linesw):
            width:int = int(self.w_l[int(dx)*2])  | int(self.w_l[int(dx)*2+1]) << 8
            if int(dx)>0:
                cursor += int(self.spacing)
                first: int = int(cursor) // 8
                if cursor%8:
                    row:object = shiftr(lines, int(len(lines)), cursor%8, self.cc)
                    ba[first] = int(ba[first]) | int(row[0]) # This works for font_to_py fonts, but might not for other fonts
                    for b in range(1, int(len(row))):
                        ba[b+first] = int(row[b])
                else:
                    for b in range(int(len(lines))):
                        ba[b+first] = int(lines[b])
            else:
                row = shiftr(lines, len(lines), self.shift, self.cc) if self.shift else lines
                for b in range(int(len(row))-1):
                    ba[b] = int(lines[b])
                    pass
                pass
            cursor += width if not self.fixed_w else int(self.fixed_w)


    def reset_draw(self):
        self.chr_l = []
        self.w_l = bytearray()
        super().reset_draw()


class Prerendered(Drawable):
    def __init__(self, x, y, h, w, buff, color, invert = False, reverse = False):
        super().__init__(x, y, color)
        self.buff = buff
        self.h = h
        self.w = w
        self.setup()
        self.rem = (self.w + self.shift) % 8 if Drawable.hor  else (self.h + self.shift) % 8
        self.inv = invert
        self.rev = reverse
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
        r = l_by_l(self.buff, self.w, self.h) if Drawable.hor else l_by_l(self.buff, self.h, self.w)
        for ln in r:
            invert_bytes(ln, len(ln)) if self.inv else None
            reverse_bits(ln, len(ln)) if self.rev else None
            yield shiftr(ln, len(ln), self.shift, self.cc) if self.shift and Drawable.hor else shiftl(ln, len(ln), self.shift, self.cc) if self.shift and not Drawable.hor else ln

class Filler(Drawable):
    def __init__(self, x = None, y = None, w = None, h = None, color = 1, key = -1, invert = False):
        self.x = x
        self.y = y
        self.c = color
        self.key = key
        self.invert = invert
        self.w = w
        self.h = h
        self.fn = None
        self.pattern = None if color < 2 else Pattern.all[color-2]
        self.ram_flag = 0b00
        Drawable.fll.append(self)

    @property
    def height(self):
        return self.h if self.fn is not self._mask or Drawable.hor else self.w

    def setup(self):
        tmp_f = self.ram_flag
        if all([self.x, self.y, self.w, self.h]):
            self.fn = self._mask()
            super().__init__(self.x, self.y, self.c)
        else:
            self.x = Drawable.xspan[0]*8
            self.w = (Drawable.c_width()+1)*8
            self.y = Drawable.yspan[0]
            self.h = Drawable.c_height()
            self.fn = self.pattern.fill(self.w//8, self.h, self.invert) if self.pattern is not None else self._fill()
            super().__init__(self.x, self.y, self.c)
        self.ram_flag = tmp_f

    def _mask(self):
        if self.key < 0 or self.key > 1:
            raise ValueError("Must have a key that is either 0 or 1")
        bwidth = (self.shift + self.w +7) // 8
        rem = (self.shift + self.w)%8
        g = self.pattern.fill(bwidth, self.h, False)
        for r in range(self.h):
            b = next(g)
            if self.shift:
                first = ((1 << self.shift) - 1) << 8 - self.shift
                b[0] = b[0] | first if not self.key else b[0] ^ first
            if rem:
                b[-1] = b[-1] | (1 << (8-rem))-1 if not self.key else b[-1] ^ (1 << (8-rem))-1
            invert_bytes(b, len(b)) if self.invert else None
            yield b

    def _fill(self):
        line = bytearray([0xff if self.c == 1 else 0] * self.w // 8)
        for i in range(self.h):
            yield line

    def draw(self):
        yield from self.fn

class Pattern:
    cl_ba = bytearray(b'\xaaU\x92I$I$\x92$\x92I\x11\x88D"\x00\xff\x00\xff\xff\xaaDD\xee\xeeDD\x11\x11\xbb\xbb\x11\x11U"'
                      b'U\x88\x88"\xaa\xaa\x00UU\x00\xaa\xaa\x00UU\xaa\xaa\xcc33\x99\xccf\x11\xaaD\xaa\x11\xaa\x11\xaaD'
                      b'\xaaD\xaaD\xaa\x00\xaa\x11\xaa\x00U\x00a\x86\x18\x92I$\x92I$a\x86\x18\x0c0\xc3\x92I$\x92I$\x0c0'
                      b'\xc33\x99\x11\x00U\x00D\xeeD\x11')
    all = []
    __slots__ = ['b','w','h']

    @classmethod
    def append(cls, ba):
        bain = len(cls.cl_ba)
        cls.cl_ba.extend(ba)
        bout = len(cls.cl_ba)
        return bain, bout

    def __init__(self, bain, baout, w, h):
        self.b = memoryview(Pattern.cl_ba[bain:baout])
        self.w = w
        self.h = h
        Pattern.all.append(self)

    def fill(self, bwdith, h, invert = False):
        invert_bytes(self.b, len(self.b)) if invert else None
        freq = h // self.h+1
        indx = 0
        for l in range(freq):
            for li in range(self.h):
                row = bytearray(bwdith)
                self.chunk(row, len(row), self.b[li*self.w:li*self.w+self.w])
                if indx == h:
                    invert_bytes(self.b, len(self.b)) if invert else None
                    break
                indx +=1
                yield row

    @micropython.viper
    def chunk(self, r:ptr8, lenr:int, byt:object)->ptr8:
        lench = int(len(byt))
        freq = lenr // lench
        for n in range(freq+1):
            for b in range(lench):
                r[n*lench+b] = int(byt[b])

# Pattern definitions
checkers = Pattern(0, 2, 1, 2)          #2
small_diags = Pattern(2, 11, 3, 3) 	  #3
big_diags = Pattern(11, 15, 1, 4) 	  #4
small_lines = Pattern(15, 17, 1, 2) 	  #5
big_lines = Pattern(17, 20, 1, 3) 	  #6
vlines = Pattern(20, 21, 1, 1) 	      #7
crosses = Pattern(21, 33, 2, 6) 	      #8
small45_sqr = Pattern(33, 37, 1, 4) 	  #9
alt_dots = Pattern(37, 39, 1, 2) 	      #10
thicks = Pattern(39, 42, 1, 3) 	      #11
alt_thicks = Pattern(42, 48, 1, 6) 	  #12
hi_checkers = Pattern(48, 52, 1, 4) 	  #13
long_checkers = Pattern(52, 54, 1, 2)    #14
wiggle = Pattern(54, 58, 1, 4) 	      #15
chevron = Pattern(58, 61, 1, 3) 	      #16
double_cross = Pattern(61, 69, 1, 8) 	  #17
fives = Pattern(69, 77, 1, 8) 	      #18
aligned_dots = Pattern(77, 79, 1, 2) 	  #19
bubbles = Pattern(79, 103, 3, 8) 	      #20
zigzag = Pattern(103, 105, 1, 2) 	      #21
tartan = Pattern(105, 109, 1, 4) 	      #22
dot_cross = Pattern(109, 113, 1, 4) 	  #23

@micropython.native
def l_by_l(buf, w, h):
    width = w//8 if w%8 == 0 else w//8+1
    for i in range(h):
        yield buf[i*width:i*width+width]

#--------------------------------------------------------------
# Bit/Byte manipulation functions
#--------------------------------------------------------------

@micropython.viper
def shiftr( ba: ptr8, lenba:int, val: int, c:int) -> object:
    if val <=0:
        raise ValueError('Number of bits must be positive and higher than 0')
    byteshift = val//8
    bitshift = val % 8
    result = bytearray(lenba+byteshift+ (1 if bitshift > 0 else 0))
    carry = 0
    for i in range(lenba):
        result[i + byteshift] = (int(ba[i]) >> bitshift) | carry
        carry = (int(ba[i]) & ((1 << bitshift) -1)) << (8-bitshift)
    if int(carry) > 0:
        result[lenba+byteshift] = carry
    if c:
        for i in range(byteshift):
            result[i] = 0xff
        result[byteshift] = int(result[byteshift]) | (1 << bitshift)-1 << (8-bitshift)
        result[-1] = int(result[-1]) | (1 << (8-bitshift))-1
    return result

@micropython.viper
def shiftl(ba:ptr8, lenba:int, val:int, c:int) -> object:
    if val <= 0:
        raise ValueError('Number of bits must be positive')
    byteshift = val // 8
    bitshift = val % 8
    lr = lenba + byteshift + (1 if bitshift > 0 else 0)
    result = bytearray(lr)
    carry = 0
    for i in range(lenba-1, -1, -1):
        result[i+byteshift+(1 if bitshift > 0 else 0)] = int(ba[i] << bitshift) | carry
        carry = int(ba[i]) >> (8 - bitshift)
    if carry:
        result[byteshift] = carry
    if c:
        for i in range(byteshift):
            result[i] = 0xff
        result[byteshift] = int(result[byteshift]) | ((1<<(8-bitshift)) -1) << bitshift
        result[-1] = int(result[-1]) | (1 << bitshift)-1
    return result

@micropython.viper
def reverse_bits(ba: ptr8, lenba:int) -> ptr8:
    for i in range(lenba):
        ba[i] = int(REVERSE_LUT[ba[i]])

@micropython.viper
def invert_bytes(ba:ptr8, lenba:int)->ptr8:
    for i in range(lenba):
        ba[i] = 255 - ba[i]  # equivalent to NOT operation because did not work on Esp32

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
    import numr110H, freesans20
    import numr110V, freesans20V
    Drawable.hor = True

    smile = bytearray([0xf0, 0xff, 0x00, 0x18, 0x00, 0x01, 0x0c, 0x00, 0x02, 0x04, 0x00, 0x06,
        0x02, 0x00, 0x04, 0xc3, 0x60, 0x04, 0x41, 0x20, 0x04, 0x01, 0x00, 0x08,
        0x01, 0x00, 0x08, 0x03, 0x06, 0x08, 0x12, 0x80, 0x08, 0x22, 0x40, 0x0c,
        0x42, 0x40, 0x04, 0xc4, 0x20, 0x06, 0x84, 0x19, 0x02, 0x08, 0x0e, 0x01,
        0x10, 0xc0, 0x00, 0x30, 0x60, 0x00, 0xe0, 0x18, 0x00, 0x80, 0x0f, 0x00])

    smol = freesans20 if Drawable.hor else freesans20V
    big = numr110H if Drawable.hor else numr110V

    plg = Poly([(20,10),(60,4),(50,50), (3,30)], 0, False)
    plg.ram_flag = 1
    #sm = Prerendered(9,10,20,20, smile, 1, invert = True, reverse = True)
    #sm.ram_flag = 1
    #br = ABLine(0,0, 30, 10, 0)
    #br.ram_flag = 1
    txt = ChainBuff("OCtoBRE1", smol, 9,0, False, False, 0, invert = True, v_rev=True)
    txt.ram_flag = 1
    #t= ChainBuff("33", big, 6, 7, False, False, invert = True, color=0)
    #t.ram_flag = 1
    #p = Pixel(90, 5, 0)
    #p.ram_flag = 1
    lll = Ellipse(100, 120, 40,20, 0,True, 0b1011)
    #print(lll.setup2())
    lll.ram_flag = 1

    f = Filler(color=9, key=1)
    f.ram_flag =1
    #ln = Rect(19, 10, 10, 20, 0, False)
    #ln.ram_flag = 1
    #lin= StrLine(10, 60,20, 0, 'h')
    #lin.ram_flag = 1
    #Drawable.set_span(50,50, True)
    #d = Drawable.draw_all(black_ram = True, k=0)
    #d = t.draw()
    @timed_function
    def generate(d):
        c = bytearray()
        for i in d:
            c.extend(i)
        return c
    @timed_function
    def genr(ba):
        d = Drawable.draw_all_into(ba,len(ba), 0, False, True)
        return d
    #generate(d)
    #Drawable.reset()
    ba = bytearray(200//8*200)
    r = genr(ba)
    for l in l_by_l(ba[:r], 32*8, 200):
        grid_print(l)
    #for i in d:
        #grid_print(i) if Drawable.hor else grid_print(i)
    """
    print()
    for p in range(len(Pattern.all)):
        d = Pattern.all[p].fill(10,10, False)
        for i in d:
            grid_print(i)
    """