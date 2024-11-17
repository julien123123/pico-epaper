from core.Eink import Eink

class EPD4IN2(Eink): #SSD1683

    def __init__(self, spi=None, *args, **kwargs):
        self.long = 400
        self.short = 300
        super().__init__(spi, *args, **kwargs)

if __name__ == "__main__":
    pass