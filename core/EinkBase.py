from machine import Pin
import core.draw_modes as dms
from utime import sleep_ms
from ustruct import pack

class EinkBase:
    black = const(0b00)
    white = 0
    darkgray = 0
    lightgray = 0
    norm = const(0)
    quick = const(1)
    part = const(2)
    gray4 = const(3)
    x_set = 0  # format to send x width to the display
    modes = (norm, quick, part, gray4)

    def __init__(self, rotation=0, cs_pin=None, dc_pin=None, reset_pin=None, busy_pin=None, hold = False):
        if rotation in (0,180):
            self.width = self.ic_side
            self.height = self.sqr_side
            self._sqr = False
        elif rotation in (90,270):
            self.width = self.sqr_side
            self.height = self.ic_side
            self._sqr = True #srq = square rotations
        else:
            raise ValueError(
                f"Incorrect rotation selected ({rotation}). Valid values: 0, 90, 180 and 270.")

        self._rotation = rotation
        self.monoc = True  # black and white only flag
        self.pp = False  # pingpong flag
        self.x2 = False  # Some displays need the buffer to be sent twice in normal mode
        self.hold = hold # Hold memory when sleeping flag
        self.cur_seq = self.breg[0:4][int(rotation/90)]
        self.cur_md = EinkBase.modes[0] # start in normal mode
        self.draw = dms.DirectMode(self, 0, not self._sqr)

        self._rst = reset_pin
        self._rst.init(Pin.OUT, value=0)
        self._dc = dc_pin
        self._dc.init(Pin.OUT, value=0)
        self._cs = cs_pin
        self._cs.init(Pin.OUT, value=1)
        self._busy = busy_pin
        self._busy.init(Pin.IN)

        self._partial = False

        self._init_disp()
        sleep_ms(500)

    def _sort_ram(self):
        if self.draw.mode is dms.BW1B:
            self._void_ram(red=True)
        else:
            self._void_ram()

    def _reset(self):
        self._rst(1)
        sleep_ms(20)
        self._rst(0)
        sleep_ms(3)
        self._rst(1)
        sleep_ms(20)

    def _send(self, command, data):
        self._send_command(command)
        self._send_data(data)

    def _read_busy(self):
        while self._busy.value() == 1:
            sleep_ms(10)
        sleep_ms(200)

    def _load_LUT(self, lut=0):
        self._send(0x32, self._luts[lut])

    def _set_cursor(self, x, y):
        self._send(0x4e, pack("h", x))
        self._send(0x4f, pack("h", y))

    def _set_window(self, start_x, end_x, start_y, end_y):
        self._send(0x44, pack(self.x_set, start_x, end_x))
        self._send(0x45, pack("2h", start_y, end_y))

    def _clear_ram(self, bw=True, red=True):
        if red:
            self._send(0x46, self.breg[4])
            self._read_busy()
        if bw:
            self._send(0x47, self.breg[4])
            self._read_busy()

    def _updt_ctrl_2(self):
        # Set Display Update Control 2 / loading LUTs
        if self.cur_md == self.norm:
            self._send(0x22, self.breg[19])
            self._load_LUT(self.breg[20]) if self.breg[20] is not 0xff else None
        elif self.cur_md == self.gray4:
            self._send(0x22, self.breg[29])
            self._load_LUT(self.breg[30]) if self.breg[30] is not 0xff else None
        elif self.cur_md == self.quick:
            self._send(0x22, self.breg[25])
            self._load_LUT(self.breg[26]) if self.breg[26] is not 0xff else None
        else:
            self._send(0x22, self.breg[21])
            self._load_LUT(self.breg[22]) if self.breg[22] is not 0xff else None
        self._read_busy()

    def _init_disp(self):
        # HW reset.
        self._reset()

        # SW reset.
        self._send_command(0x12)
        sleep_ms(20)

        # Clear BW and RED RAMs.
        self._clear_ram() if not self.hold else None
        # Set gate number.
        self._send(0x01, self.breg[6:9]) # if last b is 1, then the display is mirrored
        # Set gate voltage.
        self._send(0x03, self.breg[9]) if self.breg[9] is not 0xff else None
        # Set source voltage.
        self._send(0x04, self.breg[10:13]) if self.breg[10] is not 0xff else None
        # Set Data Entry mode.
        self._send(0x11, self.cur_seq)
        # Set border.
        self._send(0x3c, 0x03)
        # Booster Soft-start Control.
        self._send(0x0c, self.breg[14:19]) if self.breg[14] is not 0xff else None
        # Internal sensor on.
        self._send(0x18, 0x80)

        # Set Vcom
        self._send(0x2c, self.breg[13]) if self.breg[13] is not 0xff else None

        if self.cur_md & 1:
            # if mode is quick update or shades of gray, load these.
            self._send(0x1A, self.breg[23]) if not self.cur_md & 0b10 and self.breg[23] is not 0xff else self.breg[27] if self.breg[27] is not 0xff else None# Write temp register
            self._send(0x22, self.breg[24]) if self.breg[24] is not 0xff else None  # Load temp value
            self._send_command(0x20)
            self._read_busy()

        self._sort_ram()

    def _abs_xy(self, rel_x, rel_y):
        """:returns absolute display coordinates"""
        x, y = (rel_y, rel_x) if (self.cur_seq >> 2) & 1 else (rel_x, rel_y)
        seq = self.cur_seq & 0b11
        abs_x, abs_y = 0,0
        if not seq:
            abs_x = self.ic_side - 1 - x
            abs_y = self.sqr_side - 1 - y
        elif seq == 1:
            abs_x = x
            abs_y = self.sqr_side - 1  - y
        elif seq == 2:
            abs_x = self.ic_side - 1 - x
            abs_y = y
        else: #seq == 3
            abs_x = x
            abs_y = y
        return abs_x, abs_y

    def _virtual_width(self, num = None):
        """ Returning width whether the epd whant it in bytes or absolute numbers"""
        if self.breg[31]:
            return num // 8 if num is not None else self.width //8
        else:
            return num if num is not None else self.width

    # --------------------------------------------------------
    # Dummy Methods that get overridden by child classes
    # --------------------------------------------------------
    def _send_command(self, command):
        raise NotImplementedError

    def _send_data(self, data):
        raise NotImplementedError

    # --------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------
    def __call__(self, nbuf = 1, mode = None, pingpong = None, hold = None):
        """Set the hardware and software operation mode of the display"""
        rst_flag = 0 if mode is not None and mode == self.cur_md else 1
        setattr(self, 'cur_md', mode) if mode is not None else None
        setattr(self, 'hold', hold) if hold is not None else None

        if self.cur_md != self.gray4:
            if nbuf == 1:
                self.draw.mode = dms.BW1B if not self.x2 else dms.BW2X
            elif nbuf == 2:
                self.draw.mode= dms.BW2B
            else:
                raise ValueError('Only 1 or 2 buffers can be selected')
            self._partial= True if self.cur_md is self.part else False
        else:
            # This always has 2 buffers
            self.draw.mode = dms.G2B
            self._partial = False

        if rst_flag:
            self.reinit()
            if self._partial:
                pp = 0x4f if self.pp else 0xf
                self._send(0x37, pack('10B', 0x00, 0xff, 0xff, 0xff, 0xff, pp, 0xff, 0xff, 0xff, 0xff))
        self._clear_ram() if not self.hold else None
        self._sort_ram()

    def reinit(self):
        self._init_disp()

    def sleep(self):
        self._send(0x10, 0x03) if self.hold == False else self._send(0x10, 0x01)