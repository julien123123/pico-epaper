from machine import Pin
import core.draw_modes as dms
from utime import sleep_ms
from ustruct import pack

class EinkBase:
    black = const(0b00)
    white = 0
    darkgray = 0
    lightgray = 0
    RAM_BW = const(0b01)
    RAM_RED = const(0b10)
    RAM_RBW = const(0b11)
    x_set = 0  # format to send x width to the display

    def __init__(self, rotation=0, cs_pin=None, dc_pin=None, reset_pin=None, busy_pin=None, monochrome=True):
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
        self.monoc = monochrome  # black and white only flag
        self.pp = False  # pingpong flag
        self.x2 = False  # Some displays need the buffer to be sent twice in normal mode
        self.cur_seq = self._seqs[int(rotation/90)]
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

        # Flag to tell if the window size instruction was sent
        # To be removed
        self.wndw_set = False
        self.inited = False
        self.ram_inv = False

        self._init_disp()
        sleep_ms(500)

    def _sort_ram(self):
        if self.draw.mode is dms.BW1B:
            self._void_ram(red=True)
        else:
            self._void_ram()

    def _reset(self):
        self._rst(1)
        sleep_ms(30)
        self._rst(0)
        sleep_ms(3)
        self._rst(1)
        sleep_ms(30)

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
        self.wndw_set = True

    def _init_disp(self):
        # HW reset.
        self._reset()

        # SW reset.
        self._send_command(0x12)
        sleep_ms(20)

        # Clear BW and RED RAMs.
        self._clear_ram()

        # Set gate/voltages according to each display
        self._set_gate_nb()
        self._set_voltage()

        # Set Data Entry mode.
        self._send(0x11, self.cur_seq)

        # Set border.
        self._send(0x3c, 0x03)

        # Booster Soft-start Control.
        self._send(0x0c, pack("5B", 0xae, 0xc7, 0xc3, 0xc0, 0xc0))

        # Internal sensor on.
        self._send(0x18, 0x80)

        self._set_VCOM()

        self._sort_ram()
        self.inited = True

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

    # --------------------------------------------------------
    # Dummy Methods that get overridden by child classes
    # --------------------------------------------------------
    def _send_command(self, command):
        raise NotImplementedError

    def _send_data(self, data):
        raise NotImplementedError

    def _clear_ram():
        raise NotImplementedError

    def _set_gate_nb():
        raise NotImplementedError

    def _set_voltage(self):
        pass

    def _set_VCOM(self):
        pass

    def _virtual_width():
        raise NotImplementedError

    def _updt_ctrl_2(self):
        pass

    # --------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------
    # TODO making __call__ function work without actually resetting
    # Looks like 0xff for normal mode else if partial.
    def __call__(self, nbuf = 1, bw = None, partial = None, pingpong = None):
        """Set the hardware and software operation mode of the display"""
        setattr(self, 'monoc', bw) if bw is not None else None

        if self.monoc:
            if nbuf == 1:
                self.draw.mode = dms.BW1B if not self.x2 else dms.BW2X
            elif nbuf == 2:
                self.draw.mode= dms.BW2B
            else:
                raise ValueError('Only 1 or 2 buffers can be selected')
            setattr(self, '_partial', partial) if partial is not None else None
        else:
            # This always has 2 buffers
            self.draw.mode = dms.G2B
            self._partial = False

        setattr(self, 'pp', pingpong) if pingpong is not None and self._partial else setattr(self, 'pp', False) if not self._partial else None
        col = 0xff if self._partial else 0x00
        pp = 0x4f if self.pp and self._partial else 0xf if self._partial else 0x0
        self._send(0x37, pack("10B", 0x00, col, col, col, col, pp, col, col, col, col)) # The last 4 bytes don't matter
        # Looks like ths is not the right way to setup the display for partial update. This is more like manual override

        self._clear_ram()
        self._sort_ram()

    def reinit(self):
        """Public method for screen reinitialisation."""
        self._init_disp()


    def sleep(self, ram_on = False):
        self._send(0x10, 0x03) if ram_on == False else self._send(0x10, 0x01)
        self.inited = False
        self.wndw_set = False
        self.ram_inv = False