#from basecar import *
from soniccar import * 

class IRCar(SonicCar):
    def __init__(self) -> None:
        super().__init__()
        self.ir = Infrared()

    @property
    def ir_werte(self):
        return self.ir.read_analog()