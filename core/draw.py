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
def pxl(x, y, horr):
    sh = x%8 if horr else y%8
    return 0xff ^ (1 << sh)

@timed_function
@micropython.viper
def aligned_l( x: int, y: int, w: int, c: int)-> object:
    line = bytearray()
    c = c&1
    first = x%8
    
    if first:
        a = 0
        for i in range(first):
            a |= c << i
        line.append(a)
    if w - first:
        full = (w-first)//8
        b = 0xff if c else 0x00
        for i in range(full):
            line.append(b)
    rem = (w - first)%8
    if rem:
        a = 0
        for i in range(rem):
            a |= c<<(8-i)
        line.append(a)
        
    return line

@timed_function
@micropython.viper
def sqr_l(x: int, y:int, h:int, c:int) -> object:
    # lines perpendicular to the display bytes
    c = c & 1
    line = bytearray()
    allign = x%8
    
    for i in range(h):
        b = 0
        b |= c << allign
        line.append(b)
    
    return line

def ab_l(x1, y1, x2, y2):
    #Bresenham's line algorithm
    pass

def rect(x, y, w, h, c, fill=True):
    # yields a quare
    # the fuction uses parameter tu to return a tuple with aligned coordinates (bytes alligned x, y, actyal bytearray width, height)
    fline = bytearray()
    c = c & 1
    left_sp = x%8
    
    if left_sp:
        a = 0
        for i in range(8-left_sp):
            a |= c << i
        fline.append(a)
    if w-left_sp:
        full = (w-left_sp)//8
        b = 0xff if c else 0x00
        for i in range(full):
            fline.append(b)
    rem = (w-left_sp)%8
    if rem:
        a = 0
        for i in range(rem):
            a |= c << (8-i)
        fline.append(a)
    mid = h-2
    
    yield fline
    if not fill:
        line = bytearray()
        line.append(c << (8-left_sp))
        for byte in range(full):
            line.append(0x00)
        line.append(c << rem)
        
        if mid:
            for i in range(mid):
                yield line
    else:
        for i in range(mid):
            yield fline
    yield fline
    yield bytearray([0x00]*((w+7)//8+1))
    return ( x-left_sp, y, len(fline), h)
@micropython.viper
def pixl(x:int,y:int,c:int)->object:
    c = c&1
    bitpos = x%8
    b = c << bitpos
    return bytearray([b])

def create_ellipse(x_radius, y_radius, fill=False, m=0b1111, horizontal=False):

    width = 2 * x_radius + 1
    height = 2 * y_radius + 1

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
    x, y = 0, y_radius
    x_radius2 = x_radius * x_radius
    y_radius2 = y_radius * y_radius
    x_radius2y_radius2 = x_radius2 * y_radius2
    dx = 2 * y_radius2 * x
    dy = 2 * x_radius2 * y

    # Region 1
    d1 = y_radius2 - (x_radius2 * y_radius) + (0.25 * x_radius2)
    while dx < dy:
        if fill:
            # Fill horizontal line between points
            for px in range(-x, x + 1):
                if in_quadrant(px, y, m):
                    yield (x_radius + px, y_radius - y)
                if in_quadrant(px, -y, m):
                    yield (x_radius + px, y_radius + y)
        else:
            # Draw boundary points
            if in_quadrant(x, y, m):
                yield (x_radius + x, y_radius - y)
            if in_quadrant(-x, y, m):
                yield (x_radius - x, y_radius - y)
            if in_quadrant(x, -y, m):
                yield (x_radius + x, y_radius + y)
            if in_quadrant(-x, -y, m):
                yield (x_radius - x, y_radius + y)

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
        if fill:
            # Fill horizontal line between points
            for px in range(-x, x + 1):
                if in_quadrant(px, y, m):
                    yield (x_radius + px, y_radius - y)
                if in_quadrant(px, -y, m):
                    yield (x_radius + px, y_radius + y)
        else:
            # Draw boundary points
            if in_quadrant(x, y, m):
                yield (x_radius + x, y_radius - y)
            if in_quadrant(-x, y, m):
                yield (x_radius - x, y_radius - y)
            if in_quadrant(x, -y, m):
                yield (x_radius + x, y_radius + y)
            if in_quadrant(-x, -y, m):
                yield (x_radius - x, y_radius + y)

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
def elps(x_radius, y_radius, fill=False, m=0b1111):
    """
    Convert an ellipse to a bytearray representation.
    
    Parameters:
        x_radius (int): Horizontal radius of the ellipse.
        y_radius (int): Vertical radius of the ellipse.
        fill (bool): Whether to fill the ellipse (default: False).
        m (int): Mask to restrict drawing to certain quadrants (default: 0b1111).

    Returns:
        bytearray: The bytearray representation of the ellipse.
    """
    width = 2 * x_radius + 1  # Total width of the ellipse
    height = 2 * y_radius + 1  # Total height of the ellipse
    row_size = (width + 7) // 8  # Number of bytes per row (rounded up)
    result = bytearray(row_size * height)  # Preallocate the entire buffer

    for x, y in create_ellipse(x_radius, y_radius, fill, m):
        # Compute the byte and bit index for the point
        byte_index = (y * row_size) + (x // 8)
        bit_index = 7 - (x % 8)  # Bits are stored MSB first
        result[byte_index] |= (1 << bit_index)  # Set the bit

    return result

class Mulbuff: #mainly for writing fonts

    """Il me resterait à ajouter les éléments pour le spacing et de vérifier le vertical avec le spacing"""
    def __init__(self, str, x, y, spacing = 2):
        self.width= 0
        self.height = 0
        self.str = str
        self.x = x
        self.y = y
        self.spacing = spacing

    def assem(self, font, hor = False):
        """
        assemble lines of string
        """
        shift = self.x%8 if hor else self.y%8
        chr_l = []
        w_l = []
        for ltr in self.str:
            gl = font.get_ch(ltr)
            chr_l.append(self.l_by_l(gl[0], gl[2], gl[1]))
            w_l.append(gl[2])

        if hor:
            self.height = font.height()
            self.width = sum(w_l)
            for ln in range(self.height):
                #line = bytearray()
                args = []
                for index, elem in enumerate(chr_l):
                    chunk = next(elem)
                    char_w = w_l[index]
                    args.append((chunk, char_w))
                yield self.linec(*args) if not shift else self.shiftr(self.linec(*args), shift)

        else:
            self.height = sum(w_l)
            self.width = font.height()
            for ln in range(self.height):
                line = bytearray()
                for elem in chr_l:
                    for line in elem:
                        yield bytearray(line) if not shift else self.shiftr(bytearray(line), shift)

    #@micropython.viper
    def linec(self, *linesw: object)-> object:
        cursor = 0
        fl = bytearray() # final line
        for lines in linesw:
            bline, width = lines
            if cursor%8:
                bline = self.shiftr(bytearray(bline), int(cursor%8))
            if len(fl):
                merge = fl[-1] | bline[0]
                fl[-1] = merge
                fl.extend(bline[1:-1])
            else:
                fl.extend(bline)
            cursor += int(width)
        return fl

    @micropython.native
    def l_by_l(self, buf, w, h):
        width = w//8 if w%8 == 0 else w//8+1
        for i in range(h):
            yield buf[i*width:i*width+width]

    @micropython.viper
    def shiftr(self, ba: object, val: int) -> object:
        if val <0:
            raise ValueError('Number of bits must be positive')
        if val == 0:
            return ba #return a copy if no shift
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
    import numr110H
    txt = Mulbuff('3:12', 0, 0)
    bb = txt.assem(numr110H, True)
    for i in bb:
        print(i)