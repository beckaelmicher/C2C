from basisklassen import *

class BaseCar():

    def __init__(self) -> None:
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                turning_offset = data["turning_offset"]

        except:
            
            self.fw = FrontWheels(turning_offset)
            self.bw = BackWheels
    
    @property
    def steering_angle(self):

        return self._ster_angle
    
    @steering_angle.setter
    def steering_angle(self, angle):

        self._ster_angle = angle
        self._ster_angle = self.fw.turn(angle)

    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed):

        self._speed = speed
        self.bw.speed = speed
    
    @property
    def direction(self):

        return self._direction
    
    def drive(self, speed: int = 0, direction: int = 0):

        self._speed = speed
        self._direction = direction
        if self._direction == - 1:
            self.bw.backward()
            self.speed = speed
        elif self._direction == 0:
            self.stop()
        elif self.direction == +1:
            self.bw.forward()
            self.speed = speed
        else:
            self.stop()
            print("Falsche Richtung angegeben")

    def stop(self):

        self.bw.stop()


    



    
if __name__ == '__main__':
    main()

