from basecar import *



class SonicCar(BaseCar):
    def __init__(self) -> None:
        super().__init__()
        self.us = Ultrasonic()
        self.measured_distance = self.abstand
    
    @property
    def abstand(self):
        return self.us.distance()
    



           
    
    