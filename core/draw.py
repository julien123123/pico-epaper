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

def imgx():
    pass

if __name__ is '__main__':
   
    fa = aligned_l(1,2,200,1)
    si = sqr_l(29, 40, 100, 1)
    #la = square(1,4, 170, 50, 1, True)
    sol = pixl(10, 101, 1)
    while True:
        try:
            value = next(la)
            print(value)
        except StopIteration as e:
            return_value = e.value
            print("Return value:", return_value)
            break
        
