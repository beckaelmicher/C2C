from basisklassen import *

def main():
    
    bc = BaseCar()
    bc.steering_angle = 45
    print(bc.steering_angle)
    
    
    
     
class BaseCar(FrontWheels, BackWheels):
    
    def __init__(self) -> None:
        """Setup channels and basic stuff
        Args:
            turning_offset (int): Offset used to calculate the angle. Defaults to 0.
        """
        self._steering_angle = 90
        self._speed = 0
        self._direction = 0 #(1 vorwärts?, -1 rückwärts)
        
        
    
    @property
    def steering_angle(self):
        """Zugriff  des Lenkwinkels
        
        """
        return self._steering_angle
    
    @steering_angle.setter
    def steering_angle(self, angle:int):
        print("Ich bin der Sterring-Setter")
        self._steering_angle = angle
    
    @property
    def direction(self):
        return self._direction    
    
    
    @property    
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed:int):
        print("Ich bin der Speed-Setter")
        self._speed = speed
        
    def drive(self, speed, direction):
        pass
    
        
        
    def stop(self):
        self.speed = 0
        self.steering_angle = 90
    
    
    
        
    
    
    
    
if __name__ == '__main__':
    main()
        