# This file is used to translate epd data into bytearrays that are consistant for all types of displays

from struct import pack, unpack
class Epdreg:
    #spans
    _spans = [
        ('seq', 4),
        ('clr_ram_blk', 1),
        ('clr_ram_wt', 1),
        ('gate_nb',3),
        ('gate_v',1),
        ('source_v',3),
        ('st_vcom',1),
        ('soft_start', 5),
        ('upd2_norm', 1),
        ('lut_norm', 1),
        ('upd2_part', 1),
        ('lut_part', 1),
        ('wr_temp_quick', 1),
        ('ld_temp_quick', 1),
        ('upd2_quick',1),
        ('lut_quick',1),
        ('wr_temp_gr', 1),
        ('ld_temp_gr', 1),
        ('upd2_gr',1),
        ('lut_gr',1),
        ('v_width', 1)
    ]

    @classmethod
    def geninit(cls):
        """creates an init function from _spans dict"""
        first = "def __init__(self, name, "
        det = "\tself.name = name\n"
        for k, sp in cls._spans:
            first += k + ", "
            det += f"\tself.{k} = {k}\n"
        first = first.rstrip(", ") + "):"
        print(first)
        print(det)

    @classmethod
    def newobj(cls):
        print("[insert name] = Epdreg(\n\tname= ,")
        for k, sp in cls._spans:
            print(f"\t{k} = ,# span = {sp}")
        print(")")

    def __init__(self, name, seq, clr_ram_blk, clr_ram_wt, gate_nb, gate_v, source_v, st_vcom, soft_start, upd2_norm, lut_norm, upd2_part, lut_part, wr_temp_quick,
                 ld_temp_quick, upd2_quick, lut_quick, wr_temp_gr, ld_temp_gr, upd2_gr, lut_gr, v_width):
        self.name = name
        self.seq = seq
        self.clr_ram_blk = clr_ram_blk
        self.clr_ram_wt = clr_ram_wt
        self.gate_nb = gate_nb
        self.gate_v = gate_v
        self.source_v = source_v
        self.st_vcom = st_vcom
        self.soft_start = soft_start
        self.upd2_norm = upd2_norm
        self.lut_norm = lut_norm
        self.upd2_part = upd2_part
        self.lut_part = lut_part
        self.wr_temp_quick = wr_temp_quick
        self.ld_temp_quick = ld_temp_quick
        self.upd2_quick = upd2_quick
        self.lut_quick = lut_quick
        self.wr_temp_gr = wr_temp_gr
        self.ld_temp_gr = ld_temp_gr
        self.upd2_gr = upd2_gr
        self.lut_gr = lut_gr
        self.v_width = v_width
        self._checklen()
        self.genindices()

    def _checklen(self):
        for name, span in Epdreg._spans:
            dt = getattr(self, name)
            if isinstance(dt, (bytes, bytearray)):
                if len(getattr(self, name)) > span:
                    raise ValueError(f"{name} is longer than {span}")
            elif isinstance(dt, int):
                if dt > 255:
                    raise ValueError(f"{name} is bigger than one byte")
            else:
                raise TypeError(f"{name} is type {type(name)} currently only int, bytes, and bytearrays are accepted")

    def genindices(self):
        start_index = 0
        print(f"# {self.name} definitions")
        mainba = bytearray()
        for name, span in Epdreg._spans:
            data = getattr(self, name)
            end_index = start_index + span
            if span == 1:
                print(f"{name} = breg[{start_index}] = {hex(data)}")
            else:
                print(f"{name} = breg[{start_index}:{end_index}] = {data}")
            if isinstance(data, (bytes, bytearray)):
                delta = max(span - len(data), 0)
                data = bytearray(data) + bytearray(delta) if delta else data
            elif isinstance(data, int):
                ba = bytearray(span)
                ba[0] = data
                data = ba
            mainba.extend(data)
            start_index = end_index
        print(f"breg = {mainba}")

Epdreg.newobj()

Epd4IN2 = Epdreg(
    name='Epd4IN2',
	seq = b'\x03\x01\x00\x02',# span = 4
	clr_ram_blk = 0xe6,# span = 1
	clr_ram_wt = 0x66,# span = 1
	gate_nb = pack('hB', 299, 0),# span = 3
	gate_v = 0xff,# span = 1
	source_v = 0xff,# span = 3
	st_vcom = 0xff,# span = 1
    soft_start= 0xff,#span = 5
	upd2_norm = 0xf7,# span = 1
	lut_norm = 0xff,# span = 1
	upd2_part = 0xff,# span = 1
	lut_part = 0xff,# span = 1
	wr_temp_quick = 0x6e,# span = 1
	ld_temp_quick = 0x91,# span = 1
	upd2_quick =  0xc7,# span = 1
	lut_quick =  0xff,# span = 1
	wr_temp_gr =  0x5a,# span = 1
	ld_temp_gr =  0x91,# span = 1
	upd2_gr =  0xcf,# span = 1
	lut_gr =  0xff,# span = 1
    v_width= 1
)

Epd3IN7 = Epdreg(
    name = 'Epd3IN7',
	seq = b'\x03\x02\x00\x01',# span = 4
	clr_ram_blk = 0xe6,# span = 1
	clr_ram_wt = 0xf7,# span = 1
	gate_nb = pack('hB', 479, 0),# span = 3
	gate_v = 0,# span = 1
	source_v = b"\x41\xa8\x32",# span = 3
	st_vcom = 0x44,# span = 1
    soft_start= b'\xae\xc7\xc3\xc0\xc0',#span = 5
	upd2_norm = 0xf7,# span = 1
	lut_norm = 1,# span = 1
	upd2_part = 0xff,# span = 1
	lut_part = 2,# span = 1
	wr_temp_quick = 0xff,# span = 1
	ld_temp_quick = 0xff,# span = 1
	upd2_quick = 0xc7,# span = 1
	lut_quick = 0,# span = 1
	wr_temp_gr = 0xff,# span = 1
	ld_temp_gr = 0xff,# span = 1
	upd2_gr = 0xc7,# span = 1
	lut_gr = 0,# span = 1
    v_width= 0,
)

Epd2IN9 = Epdreg(
    name = 'Epd2IN9',
	seq = b'\x03\x02\x00\x01',# span = 4
	clr_ram_blk = 0xe6,# span = 1
	clr_ram_wt = 0xe5,# span = 1
	gate_nb = b'\x27\x01\x00',# span = 3
	gate_v = 0xff,# span = 1
	source_v = 0xff,# span = 3
	st_vcom = 0xff,# span = 1
    soft_start= 0xff,#span = 5
	upd2_norm = 0xf7,# span = 1
	lut_norm = 0xff,# span = 1
	upd2_part = 0x1c,# span = 1
	lut_part = 0xff,# span = 1
	wr_temp_quick = 0x5a,# span = 1
	ld_temp_quick = 0x91,# span = 1
	upd2_quick = 0xc7,# span = 1
	lut_quick = 0xff,# span = 1
	wr_temp_gr = 0xff,# span = 1
	ld_temp_gr = 0xff,# span = 1
	upd2_gr = 0xf4,# span = 1
	lut_gr = 0xff,# span = 1
    v_width= 1,
)

Epd1IN54 = Epdreg(
    name = 'Epd1In54',
	seq = b'\x03\x01\x00\x02',# span = 4
	clr_ram_blk = 0xe6,# span = 1
	clr_ram_wt = 0xe5,# span = 1
	gate_nb = b'\xc7\x00\x00',# span = 3
	gate_v = 0xff,# span = 1
	source_v = 0xff,# span = 3
	st_vcom = 0xff,# span = 1
    soft_start= 0xff,#span = 5
	upd2_norm = 0xf7,# span = 1
	lut_norm = 0xff,# span = 1
	upd2_part = 0xfc,# span = 1
	lut_part = 0xff,# span = 1
	wr_temp_quick = 0x64,# span = 1
	ld_temp_quick = 0x91,# span = 1
	upd2_quick = 0xc7,# span = 1
	lut_quick = 0xff,# span = 1
	wr_temp_gr = 0x5a,# span = 1
	ld_temp_gr = 0x91,# span = 1
	upd2_gr = 0xcf,# span = 1
	lut_gr = 0xff,# span = 1
    v_width=1,
)

"""
[insert name] = Epdreg(
    name = ,
	seq = ,# span = 4
	clr_ram_blk = ,# span = 1
	clr_ram_wt = ,# span = 1
	gate_nb = ,# span = 3
	gate_v = ,# span = 1
	source_v = ,# span = 3
	st_vcom = ,# span = 1
	soft_start= ,#span = 5
	wr_temp_norm = ,# span = 1
	ld_temp_norm = ,# span = 1
	upd2_norm = ,# span = 1
	lut_norm = ,# span = 1
	wr_temp_part = ,# span = 1
	ld_temp_part = ,# span = 1
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
	v_width = , # span = 1
)
"""
# Commands
DRV_OUT_CTRL = const(0x01)
GATE_DRV_VOLT_CTRL = const(0x03)
SRC_DRV_VOLT_CTRL = const(0x04)
INIT_CODE_SET = const(0x08)
WR_REG_INIT_CODE = const(0x09)
RD_REG_INIT_CODE = const(0x0A)
BOOST_SOFT_ST = const(0x0C)
DEEP_SLEEP = const(0x10)
DATA_ENTRY_MODE = const(0x11)
SW_RST = const(0x12)
HV_RDY_DET = const(0x14)
VCI_DET = const(0x15)
TEMP_SENS_CTRL = const(0x18)
TEMP_SENS_SEL = const(0x1A)
RD_TEMP = const(0x1B)
MASTER_ACT = const(0x20)
UPD_DISP_CTRL1 = const(0x21)
UPD_DISP_CTRL2 = const(0x22)
WR_RAM_BW = const(0x24)
WR_RAM_RED = const(0x26)
RD_RAM = const(0x27)
VCOM_SENSE = const(0x28)
VCOM_SENSE_DUR = const(0x29)
PRG_VCOM_OTP = const(0x2A)
WR_VCOM_REG = const(0x2C)
RD_VCOM_REG = const(0x2D)
OTP_REG_RD = const(0x2E)
STATUS_BIT_RD = const(0x2F)
WR_LUT_REG = const(0x32)
ST_DUMMY_LINE = const(0x3A)
ST_GATE_LINE_WIDTH = const(0x3B)
BORDER_WAVE_CTRL = const(0x3C)
WR_RAM_OPT = const(0x3D)
ST_RAM_X_START_END = const(0x44)
ST_RAM_Y_START_END = const(0x45)
ST_RAM_X_CNT = const(0x4E)
ST_RAM_Y_CNT = const(0x4F)
NOP = const(0xFF)