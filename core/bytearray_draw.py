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

def square(x, y, w, h, c, fill):
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

if __name__ is '__main__':
   
    fa = aligned_l(1,2,200,1)
    si = sqr_l(29, 40, 100, 1)
    la = square(1,4, 170, 50, 1, True)
    sol = pixl(10, 101, 1)
    while True:
        try:
            value = next(la)
            print(value)
        except StopIteration as e:
            return_value = e.value
            print("Return value:", return_value)
            break
        
