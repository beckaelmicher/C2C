from basecar import *

# Diese Klasse verwendet den Ultraschallsensor
class SonicCar(BaseCar):
    def __init__(self) -> None:      
        super().__init__()
        # Verwenden individueller Konfigurationseinstellungen für den Ultraschallsensor aus der config.json
        try:
            with open("config.json", "r") as f: 
                data = json.load(f)
                timeout = data["timeout"]
        except:
            print("Keine geeignete Datei config.json gefunden!")  
        self.us = Ultrasonic(timeout=timeout)
        self.measured_distance = self.abstand
    
    @property
    def abstand(self)-> int:
        """
        Misst den Abstand mittels Ultraschallsensor zu einem Hinderniss
        
        Return: int Abstand zum Hinderniss in cm, negativ Wert zeigt Sensorfehler an
        """
        return self.us.distance()
    
    def stop(self)-> None:
        """
        Methode zum Stoppen
        Überschrieben aus BaseCar und erweitert um Stoppen des Ultraschallsensors
        """
        # Stoppen der Fahrbewegung
        self.bw.stop()
        # Anhalten der Ultra-Schallmessung
        self.us.stop()

           
    
    