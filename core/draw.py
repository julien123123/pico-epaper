import utime

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
    def __init__(self, x, y, hor):
        self.x = x
        self.y = y
        self.actual_x = 0
        self.actual_y = 0
        self.hor = hor

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


class Pixel(Drawable):
    def __init__(self, x, y, color, hor):
        super().__init__(x, y, hor)
        self.byte = 0
        self.actual_x = self.x - self.x%8 if self.hor else self.x
        self.actual_y = self.y - self.y%8 if not self.hor else self.y
        self.c = color & 1
        self.setup()

    @property
    def width(self):
        return 8 if self.hor else 1

    @property
    def height(self):
        return 1 if self.hor else 8

    def setup(self):
        sh = self.x%8 if self.hor else self.y%8
        self.byte = 0xff ^ (1 << (7-sh)) if not self.c else 1 << (7-sh)

    def draw(self):
        return bytearray([self.byte])


class StrLine(Drawable):
    # Still have to do the vertical version
    def __init__(self, x, y, span, c, orientation, hor):
        super().__init__(x, y, hor)
        self.span = span
        self.color = c & 1
        self.orientation = orientation
        if self.orientation not in ('h', 'v'):
            raise ValueError('orientation must be either "h" or "v"')
        self.funct = self.aligned_l if self.orientation == 'h' and self.hor or self.orientation == 'v' and not self.hor else self.sqr_l
        self.first = self.x % 8 if self.hor else self.y % 8
        self.actual_x = self.x - bool(self.first)*8 if self.hor else self.x
        self.actual_y = self.y - bool(self.first)*8 if not self.hor else self.y
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

    @timed_function
    @micropython.viper
    def aligned_l(self)-> object:
        line = bytearray()
        first = int(self.first)
        col = int(self.color)
        sp = int(self.span)
        
        if first:
            a = 0
            for i in range(first):
                a |= col << i
            line.append(a)
        if sp - first:
            full = (sp-first)//8
            b = 0xff if col else 0x00
            for i in range(full):
                line.append(b)
        rem = (sp - first)%8
        if rem:
            a = 0
            for i in range(rem):
                a |= col <<(7-i)
            line.append(a)
        return line

    def sqr_l(self) -> object:
        # lines perpendicular to the display bytes
        b = self.color << ( 7 - self.first )
        return bytearray([b]*self.span)

    def draw(self):
        return self.funct()


class ABLine(Drawable):
    # Lacks the possibility of drawing lines in different quadrants
    def __init__(self, x1, y1, x2, y2, c, hor):
        super().__init__(x1, y1, hor)
        self.x2 = x2
        self.y2 = y2
        self.w = x2 - x1
        self.h = y2 - y1
        self.color = c & 1
        self.first = x1 % 8 if hor else y1 % 8
        self.rem = (x2 - x1 - self.first) % 8 if hor else (y2 - y1 - self.first) % 8
        self.actual_x = x1 - self.first if hor else x1
        self.actual_y = y1 if hor else y1 - self.first

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
        bkgrd = 0 if self.color == 1 else 0xff
        byte_width = self.width // 8 if self.hor else self.height // 8
        for x_points in grouped_points:
            if x_points:
                bline = bytearray([bkgrd] * byte_width)
                for pt in x_points:
                    if self.hor:
                        bline[pt // 8] |= 1 << (pt % 8)
                    else:
                        bline[pt//8] |= 1 << ( 7 - ( pt % 8 ))
                yield bline


class Rect(Drawable):
    # not working for vertical rectangles yet
    def __init__(self, x, y, height, width, color, hor, f= True):
        super().__init__(x, y, hor)
        self.h = height
        self.w = width
        self.c = color & 1
        self.f = f
        self.first = self.x % 8 if self.hor else self.y % 8
        self.rem = (self.w - self.first)%8 if self.hor else (self.h - self.first)%8
        self.actual_x = self.x - self.first if self.hor else self.x
        self.actual_y = self.y - self.first if not self.hor else self.y
        self.setup()

    @property
    def width(self):
        return self.w - self.first- self.rem + bool(self.rem) + bool(self.first) if self.hor else self.w

    @property
    def height(self):
        return self.h if self.hor else self.h - self.first- self.rem + bool(self.rem) + bool(self.first)

    def setup(self):
        pass

    def draw(self):
        fline = bytearray()
        if self.first:
            a = 0
            for i in range(8-self.first):
                a |= self.c << i
            fline.append(a)
        if self.w-self.first:
            full = (self.w-self.first)//8
            b = 0xff if self.c else 0x00
            for i in range(full):
                fline.append(b)
        if self.rem:
            a = 0
            for i in range(self.rem):
                a |= self.c << (8-i)
            fline.append(a)
        mid = self.h-2
        yield fline
        if not self.f:
            line = bytearray()
            line.append(self.c << (8-self.first))
            for byte in range(full):
                line.append(0x00) if self.c else line.append(0xff)
            line.append(self.c << self.rem)

            if mid:
                for i in range(mid):
                    yield line
        else:
            for i in range(mid):
                yield fline
        yield fline
        #yield bytearray([0x00]*((self.w+7)//8+1)) Je ne sais pas pourquoi j'ai mis ça là

@micropython.viper
def pixl(x:int,y:int,c:int)->object:
    c = c&1
    bitpos = x%8
    b = c << bitpos
    return bytearray([b])


class Ellipse(Drawable):
    def __init__(self,xradius, yradius, x, y, color, hor, f = False, m = 0b1111):
        self.xr = xradius
        self.yr = yradius
        self.fill = f
        self.c =color
        self.m = m
        super().__init__(x, y, hor)
        self.setup()

    @property
    def width(self):
        return 2*self.xr+1 if self.hor else 2*self.yr+1

    @property
    def height(self):
        return 2*self.yr+1 if self.hor else 2*self.xr+1

    def setup(self):
        """:returns a list of coordinates"""

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
                        yield self.xr + px, self.yr - y # removed parenthesis
                    if in_quadrant(px, -y, self.m):
                        yield self.xr + px, self.yr + y
            else:
                # Draw boundary points
                if in_quadrant(x, y, self.m):
                    yield self.xr + x, self.yr - y
                if in_quadrant(-x, y, self.m):
                    yield self.xr - x, self.yr - y
                if in_quadrant(x, -y, self.m):
                    yield self.xr + x, self.yr + y
                if in_quadrant(-x, -y, self.m):
                    yield self.xr - x, self.yr + y

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
                        yield self.xr + px, self.yr - y
                    if in_quadrant(px, -y, self.m):
                        yield self.xr + px, self.yr + y
            else:
                # Draw boundary points
                if in_quadrant(x, y, self.m):
                    yield self.xr + x, self.yr - y
                if in_quadrant(-x, y, self.m):
                    yield self.xr - x, self.yr - y
                if in_quadrant(x, -y, self.m):
                    yield self.xr + x, self.yr + y
                if in_quadrant(-x, -y, self.m):
                    yield self.xr - x, self.yr + y

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

    def setup2(self):
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
        """
        Convert an ellipse to a bytearray representation.
        """
        row_size = (self.width + 7) // 8  # Number of bytes per row (rounded up)
        result = bytearray(row_size * self.height)  # Preallocate the entire buffer

        for x, y in self.setup():
            # Compute the byte and bit index for the point
            byte_index = (y * row_size) + (x // 8)
            bit_index = 7 - (x % 8)  # Bits are stored MSB first
            result[byte_index] |= (1 << bit_index)  # Set the bit
        return result

    @micropython.native
    def draw2(self):
        points = [p for p in self.setup()]
        max_y = max(y for _, y in points)
        grpt = [[] for _ in range(max_y+1)]
        for x, y in points:
            grpt[y].append(x)
        bkgrd = 0 if self.c == 1 else 0xff
        byte_width = (self.width+7)//8
        for x_points in grpt:
            if x_points:
                bline = bytearray([bkgrd]*byte_width)
                for pt in x_points:
                    bline[pt//8] |= 1<<(7-(pt%8))
                yield bline

    @micropython.native
    def draw22(self):
        points = self.setup2()

        bkgrd = 0 if self.c == 1 else 0xff
        byte_width = (self.width + 7) // 8
        for x_points in points:
            if x_points:
                bline = bytearray([bkgrd] * byte_width)
                for pt in x_points:
                    bline[pt // 8] |= 1 << (7 - (pt % 8))
                yield bline


class ChainBuff(Drawable): #mainly for writing fonts

    """ajouter implémentation de fixed width pour vertical"""
    def __init__(self, st, font, x, y, hor = False, spacing = 2, fixed_w = False):
        self.st = st
        self.x = x
        self.y = y
        self.spacing = spacing
        self.fixed_w = fixed_w if fixed_w != 'max' else font.max_width()
        self.font = font
        self.hor = hor
        self.chr_l = []
        self.w_l = bytearray()
        self.shift = self.x%8 if self.hor else self.y%8
        
        if self.fixed_w and self.fixed_w < self.font.max_width():
            raise ValueError(f"fixed_width should be equal to or greater than the font's max_width, use 'max' to use that value instead")

        self.setup()

    @property
    def width(self):
        return sum(self.w_l)+(len(self.w_l)-1)*self.spacing if self.hor else self.font.height()

    @property
    def height(self):
        return self.font.height() if self.hor else sum(self.w_l)+(self.spacing*(len(self.st)-1)) #or fixed width*len(self.st)

    def setup(self):
        for ltr in self.st:
            gl = self.font.get_ch(ltr)
            self.chr_l.append(l_by_l(gl[0], gl[2], gl[1])) if self.hor else self.chr_l.append(
                l_by_l(gl[0], gl[1], gl[2]))
            self.w_l.append(gl[2])

    def draw(self):
        """
        assemble lines of string
        """
        if self.hor: #HORRIZONTAL
            for ln in range(self.height):
                args = []
                for index, elem in enumerate(self.chr_l):
                    args.append(next(elem))
                yield self.linec(self.shift, *args)

        else: #VERTICAL
            b_width = self.width//8 + bool(self.width%8)

            for e, elem in enumerate(self.chr_l):
                delta = self.fixed_w - self.w_l[e] if self.fixed_w else 0
                for line in elem:
                    yield bytearray(line) if not self.shift else shiftr(bytearray(line), self.shift)

                if bool(self.spacing+delta) & bool(e < len(self.chr_l) - 1):
                    for _ in range(self.spacing+delta): #plus delta
                        yield bytearray(b_width)


    @micropython.native
    def linec(self, shift, *linesw: object)-> object:
        cursor = 0
        fl = bytearray() # final line
        for ndx,lines in enumerate(linesw):
            width = self.w_l[ndx]
            if len(fl):
                delta_fw = self.fixed_w - self.w_l[ndx] if self.fixed_w else 0
                ttl_spc = delta_fw + self.spacing
                width += ttl_spc
                shbit = ( cursor + ttl_spc ) %8
                shbyte = (cursor%8 + ttl_spc)//8
                fl.extend(bytearray(shbyte)) if shbyte else None

                if shbit:
                    lines = shiftr(bytearray(lines), int(cursor % 8))
                    merge = fl[-1] | lines[0]
                    fl[-1] = merge
                    fl.extend(lines[1:-1])
                else:
                    fl.extend(lines)
            else:
                width += shift
                fl.extend(shiftr(lines, shift)) if shift else fl.extend(lines)
            cursor += int(width)
        return fl

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

if __name__ is '__main__':
    @timed_function
    def draw1(obj):
        a = obj.draw()
        print(f'len = {len(a)}')
        print(a)
    @timed_function
    def draw2(obj):
        a = bytearray().join(obj.draw2())
        print(f'len = {len(a)}')
        print(a)
    @timed_function
    def draw22(obj):
        a = bytearray().join(obj.draw22())
        print(f'len = {len(a)}')
        print(a)

    import numr110H, numr110V
    '''
    el = Ellipse(100, 90, 0, 0, 1,True, True)
    ec = Ellipse(100, 90, 0, 0, 1,True, True)
    ed = Ellipse(100, 90, 0, 0, 1, True, True)
    draw1(el)
    draw2(ec)
    draw22(ed) # Winner winner chicken dinner

    bl = StrLine(0, 0, 100, 1, 'v', True).draw()
    print(bl)
    
    al = ABLine(0, 0, 100, 4, 1, True).draw()
    for v in al:
        print(v)

    r = Rect(3, 0, 10, 100, 1, True).draw()
    for v in r:
        print(v)
    '''
    
    txt = ChainBuff('46', numr110V, 3, 4, False, 0, False)
    bb = txt.draw()
    for i in bb:
        print(i)
