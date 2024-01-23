from soniccar import * 

# Diese Klasse verwendet den IR-Sensor
class IRCar(SonicCar):
    def __init__(self) -> None:
        super().__init__()
        self.ir = Infrared()

    @property
    def ir_werte(self)-> list:
        """
        Getter- um die gemessenen IR-Werte in Form einer Liste auszulesen
        Return: Liste von gemessen IR-Werten der 5 Sensoren
        """
        return self.ir.read_analog()

