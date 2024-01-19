from basecar import *



class SonicCar(BaseCar):
    def __init__(self) -> None:      
        super().__init__()
        try:
            with open("config.json", "r") as f: # Verwenden individueller Konfigurationseinstellungen für den Ultraschallsensor aus der config.json
                data = json.load(f)
                timeout = data["timeout"]
        except:
            print("Keine geeignete Datei config.json gefunden!")  
        self.us = Ultrasonic(timeout=timeout)
        self.measured_distance = self.abstand
    
    @property
    def abstand(self):
        return self.us.distance()
    
    def stop(self):
        """Methode zum Stoppen
        Überschrieben aus BaseCar und erweitert um Stoppen des Ultraschallsensors
        """
        self.bw.stop()
        self.us.stop()



           
    
    