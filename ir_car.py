#from basecar import *
from soniccar import * 

class IRCar(SonicCar):
    def __init__(self) -> None:
        super().__init__()
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                schwellwert = data["IR_schwellwert"]
        except:
            print("Keine geeignete Datei config.json gefunden!")
        self.ir_auslesen = Infrared().read_analog()
        
        
    