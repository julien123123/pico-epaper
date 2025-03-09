"""
# Epd4IN2 definitions
seq = breg[0:4] = b'\x03\x01\x00\x02'
clr_ram_blk = breg[4] = 0xe6
clr_ram_wt = breg[5] = 0x66
gate_nb = breg[6:9] = b'+\x01\x00'
gate_v = breg[9] = 0xff
source_v = breg[10:13] = 255
st_vcom = breg[13] = 0xff
soft_start = breg[14:19] = 255
upd2_norm = breg[19] = 0xf7
lut_norm = breg[20] = 0xff
upd2_part = breg[21] = 0xff
lut_part = breg[22] = 0xff
wr_temp_quick = breg[23] = 0x6e
ld_temp_quick = breg[24] = 0x91
upd2_quick = breg[25] = 0xc7
lut_quick = breg[26] = 0xff
wr_temp_gr = breg[27] = 0x5a
ld_temp_gr = breg[28] = 0x91
upd2_gr = breg[29] = 0xcf
lut_gr = breg[30] = 0xff
breg = bytearray(b'\x03\x01\x00\x02\xe6f+\x01\x00\xff\xff\x00\x00\xff\xff\x00\x00\x00\x00\xf7\xff\xff\xffn\x91\xc7\xffZ\x91\xcf\xff')
"""

import framebuf
from core.Eink import Eink
from ustruct import pack

class EPD4IN2(Eink): #SSD1683 GDEY042T81 GY-E042A87 (not for the T2)
    x_set = '2B'
    white = 0b01
    darkgray = 0b10
    lightgray = 0b11
    breg = b'\x03\x01\x00\x02\xe6f+\x01\x00\xff\xff\x00\x00\xff\xff\x00\x00\x00\x00\xf7\xff\xff\xffn\x91\xc7\xffZ\x91\xcf\xff\x01'
    def __init__(self, spi=None, *args, **kwargs):
        self.sqr_side = 300
        self.ic_side = 400
        super().__init__(spi, *args, **kwargs)

if __name__ == "__main__":
    from machine import Pin, SPI
    import numr110H, numr110V, freesans20, freesans20V, time
    from core.draw import Drawable as DR
    import framebuf as fb


    p = Pin(27, Pin.OUT)
    epdSPI = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    epd = EPD4IN2(rotation=180, spi=epdSPI, cs_pin=Pin(1), dc_pin=Pin(26), reset_pin=p, busy_pin=Pin(28))

    big = numr110H if not epd._sqr else numr110V
    smol = freesans20 if not epd._sqr else freesans20V

    epd.draw.text(' Mercredi 20 dec 2025', smol, 0,10, c=0)
    epd.draw.text('3', big, 230, 100, c = 0)
    epd.draw.rect(350,250,50,50)
    epd.draw.fill(c=3, diff=True, key = 1, invert = False)
    epd.show()
    epd(1, mode = epd.quick)
    epd.draw.text('44', big, 0 , 0)
    epd.draw.ellipse(90, 70, 120, 100, f= True)
    #epd.draw.fill(c=20, invert=True, diff = True)
    epd.show(key = 0)
    """
    epd(mode = epd.part, pingpong = False)
    epd.draw.fill(c=11,key = -1, diff =True) 
    epd.draw.text('SY', big, 20, 20)
    epd.show()
    epd.draw.text('hello?', smol, 100, 20)
    epd.show()
    epd.show_ram()
    
    epd(1, mode = epd.quick)
    epd.sleep()
    epd.reinit()
    epd.draw.ellipse(10,10, 40, 100)
    epd.show(clear=True)
    epd(2, mode = epd.part)
    manx = 6
    k=0
    epd.draw.rect(100, 60, 40, 40, f=True, c = 0)
    epd.draw.pixel(10,10)
    epd.draw.text('42:48', big, manx,80)
    epd.draw.text(' Mercredi 20 dec 2025', smol, manx,10, c=0)

    epd.draw.ellipse(100, 70, 79, 80, f= True)
    print(DR.blkl[-1].height)

    epd.draw.show(key=k)
    epd.sleep()

    # Yup, we are sleeping babe
    epd.reinit()
    epd(2, mode = epd.part, pingpong = True)

    epd.draw.text('42:48', big, manx,80, diff=True)
    epd.draw.text('22:45', big, manx,80)
    epd.draw.show(key=k)
    epd.draw.text('WN:DW', big, manx, 80)
    epd.draw.show(key=k)
    epd.show_ram()
    epd(1, mode = epd.quick)
    #epd.show(True, key =0)
    #epd.show(key = 0)
    epd.reinit()
    cd = bytearray((50+7)*50//8)
    f = fb.FrameBuffer(cd, 50, 50, framebuf.MONO_HLSB)
    f.fill(1)
    f.text('salut', 0, 0, 0)
    epd.draw.blit(20,30, cd, 50, 50)
    epd.show(clear=True)
    """
    #epd.show_ram()
    epd.sleep()

    

 