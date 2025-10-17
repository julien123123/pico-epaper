# Make your own driver

If your display has a driver that starts with SSD, you can most probably use this library to drive your e-paper display 
too. 

## Instructions
1. Copy the part in quotations in `epd_maker.py`, and paste it right before the quotations, and populate it with your own values. 
Those values can usually be sourced from example code or arduino drivers.
```python

"""
[insert name] = Epdreg(
	name= ,
	seq = ,# span = 4
	clr_ram_blk = ,# span = 1
	clr_ram_wt = ,# span = 1
	gate_nb = ,# span = 3
	gate_v = ,# span = 1
	source_v = ,# span = 3
	st_vcom = ,# span = 1
	soft_start = ,# span = 5
	upd2_norm = ,# span = 1
	lut_norm = ,# span = 1
	upd2_part = ,# span = 1
	lut_part = ,# span = 1
	wr_temp_quick = ,# span = 1
	ld_temp_quick = ,# span = 1
	upd2_quick = ,# span = 1
	lut_quick = ,# span = 1
	wr_temp_gr = ,# span = 1
	ld_temp_gr = ,# span = 1
	upd2_gr = ,# span = 1
	lut_gr = ,# span = 1
	v_width = ,# span = 1
)
"""
```

2. When you filled all those values, execute the file and copy the `breg` value under the name you gave to your display

3. In the `Eink.py` file inside the uEPD folder, go at the bottom, and make a `Eink` subclass for your display with the `breg`
you just copied as a class attribute.
```python
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
```
4. Now you can set your subclass attributes. If your display's luts are not in the OTP of the display driver, you may add them as a tuple in the `self._luts` attribute.

   * `x_set` is the byte format used by the display to set the x start and stop. It's either '2B' or '2H'. The wrong value
   can make you display work unproprely. (see 0x44 instruction in datasheet)
   * `white`, `darkgray`, `lightgray` represent how the driver resolve the colours in it's ram. You usually can find that
   informaiton in the datasheet. The righthand bit represent the value in the black and white ram, the lefthand one represents
   the value in the red ram. If your display has other colours than black and white, you can probably play with those values
   * `sqr_side` is the amount of pixels on the side perpendicular to where the mirror chip is on your display.
   * `ic_side` is the amount of pixels on the same side as the mirror rectangle IC on your display

5. Once this is all done write your display's class name in \__all\__ in the \__init\__.py 

You can now import your display in another file

---
## Params of epd_maker

* `name` Pretty self-explanatory
* `seq` [breg[0:4]][span = 4] The scan recipe for your display (see instruction 0x11 in the datasheet for details). the 
first byte represents the seq number for 0 degrees, the second, for 90 degrees, the third for 180 degrees, and the 
fourth for 270 degrees. Start with one of the displays already there if you don't know what value to use.
* `clr_ram_blk`  [breg[4]][span = 1] The number you need to give the ic to clear ram to black (or 0) (see command 0x46, 
0x47 in datasheet)
* `clr_ram_wt`  [breg[5]][span = 1] The number you need to give the ic to clear ram to white (or 1) (see command 0x46, 
0x47 in datasheet)
* `gate_nb`  [breg[6:9]][span = 3] the number of gates, third byte mirrors the display when == 1(see command 0x1 in the 
datasheet)
* `gate_v`  [breg[9]][span = 1] set gate voltage if needed, set to 0xff if not (see command 0x3 in datasheet)
* `source_v`  [breg[10:13]][span = 1]  set source voltage if needed, set to 0xff if note (see command 0x4)
* `st_vcom`  [breg[13]][span = 1] Set vcom if needed, set to 0xff if not (see command 0x2c in datasheet)
* `soft_start`  [breg[14:19]][span = 5] set soft start control if needed, set to 0xff if not (see command 0xc in datasheet)
* `upd2_norm`  [breg[19]][span = 1] Display update control 2 command for normal mode (see command 0x22 in datasheet) examples
and/or other libraries often have this number.
* `lut_norm`  [breg[20]][span = 1] If the display needs to load a lut for normal mode, this byte is it's index in the tuple
* `upd2_part`  [breg[21]][span = 1] Display update control 2 command for the partial/differential mode (see command 0x22 in datasheet)
* `lut_part`  [breg[22]][span = 1] Index of part LUT in lut tuple (if needed)
* `wr_temp_quick`  [breg[23]][span = 1]  Temperature value for quick mode (see 0x1A for more info) 
* `ld_temp_quick`  [breg[24]][span = 1] Load temperature value from internal sensor if needed, else write 0xff
* `upd2_quick`  [breg[25]][span = 1] Display update control 2 command for the quick mode (see command 0x22 in datasheet)
* `lut_quick`  [breg[26]][span = 1] Index of Quick LUT in lut tuple (if needed)
* `wr_temp_gr`  [breg[27]][span = 1] Temperature value for shades of gray mode (see 0x1A for more info) 
* `ld_temp_gr`  [breg[28]][span = 1] Load temperature value from internal sensor if needed, else write 0xff
* `upd2_gr`  [breg[29]][span = 1] Display update control 2 command for the shades of gray mode (see command 0x22 in datasheet)
* `lut_gr` [breg[30]][span = 1] Index of Quick LUT in lut tuple (if needed)
* `v_width`  [breg[31]][span = 1] > 1 if width of the display's coordinates is in bytes, 0 if in absolute numbers