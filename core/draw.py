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
'''
pense que j'ai trouvé comment
def imgx():
    #this is what chat gpt gave me
    def draw_glyphs_on_line(display_width, glyphs, start_positions, line, get_glyph_row):
        """
        Renders glyphs on a single display line and transmits it.

        :param display_width: Width of the display in pixels (e.g., 400).
        :param glyphs: List of glyph identifiers to render.
        :param start_positions: List of bit start positions for each glyph.
        :param line: The specific line of the glyphs to render (0-indexed).
        :param get_glyph_row: Function to retrieve a memoryview for a glyph's row.
                              Expected signature: `get_glyph_row(glyph, line)`.
        """
        display_line = bytearray(display_width // 8)  # Allocate display buffer for the current line

        for glyph, bit_start in zip(glyphs, start_positions):
            glyph_row = get_glyph_row(glyph, line)  # Retrieve the memoryview for the glyph's row
            glyph_width = len(glyph_row) * 8  # Each byte in glyph_row represents 8 pixels

            # Determine where the glyph should start in the display buffer
            byte_offset = bit_start // 8
            bit_offset = bit_start % 8

            # Write the glyph row into the display line buffer
            for i, byte in enumerate(glyph_row):
                if byte_offset + i < len(display_line):
                    display_line[byte_offset + i] |= byte >> bit_offset
                if byte_offset + i + 1 < len(display_line) and bit_offset > 0:
                    display_line[byte_offset + i + 1] |= (byte << (8 - bit_offset)) & 0xFF

        # Transmit the constructed line to the display
        transmit_display_line(display_line)

    def transmit_display_line(line_data):
        """
        Stub function to represent transmitting a line of data to the display.
        Replace this with your display driver's implementation.
        """
        # Example: Send the line_data over SPI or I2C
        pass
'''
class Mulbuff: #mainly for writing fonts
    def __init__(self, str, x, y):
        self.width= 0
        self.height = 0
        self.str = str
        self.x = x
        self.y = y

    def assem(self, font, hor = False):
        shift = self.x%8 if hor else self.y%8
        chr_l = []
        wi = 0
        for ltr in self.str:
            gl = font.get_ch(ltr)
            chr_l.append(self.l_by_l(gl[0], gl[2], gl[1]))
            wi += gl[2]

        if hor:
            self.height = font.height()
            self.width = wi
            for ln in range(self.height):
                line = bytearray()
                for elem in chr_l:
                    chunk = next(elem)
                    line.extend(bytearray(chunk))
                yield line if not shift else self.shiftr(line, shift)

        else:
            self.height = wi
            self.width = font.height()
            for ln in range(wi):
                line = bytearray()
                for elem in chr_l:
                    for line in elem:
                        yield bytearray(line) if not shift else self.shiftr(bytearray(line), shift)

    def l_by_l(self, buf, w, h):
        width = w//8
        for i in range(h):
            yield buf[i*width:i*width+width]

    def shiftr(self, ba, val):
        if val <0:
            raise ValueError('Number of bits must be positive')
        if val == 0:
            return ba[:] #return a copy if no shift
        byteshift = val//8
        bitshift = val % 8

        result = bytearray(len(ba)+byteshift+ (1 if bitshift > 0 else 0))
        carry = 0

        for i in range(len(ba)):
            result[i + byteshift] = (ba[i] >> bitshift) | carry
            carry = (ba[i] & ((1 << bitshift) -1)) << (8-bitshift)

        if carry > 0:
            result[len(ba)+byteshift] = carry

        return result


if __name__ is '__main__':
   
    pass