from basisklassen import *
import click
import time
import json

class BaseCar(object):
    """
    Basisklasse fuer Antrieb und Lenkung des Picar
    FrontWheel und BackWheels werden als Objekte instanziert
        
    """
    def __init__(self) -> None:
        # # Einlesen der individuellen Lenkrad-Einstellung
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                turning_offset = data["turning_offset"]
                # forward_A = data["forward_A"]
                # forward_B = data["forward_B"]
                # print("Daten in config.json:")
                # print(" - Turning Offset: ", turning_offset)
                # print(" - Forward A: ", forward_A)
                # print(" - Forward B: ", forward_B)
        except:
            print("Keine geeignete Datei config.json gefunden!")
        # turning_offset übergeben zur Justierung des Lenkeinschlags
        self.fw = FrontWheels(turning_offset=turning_offset) 
        self.bw = BackWheels()
        self.steering_angle = 90
        self.speed = 0 
        self._direction = 0

    
    @property
    def steering_angle(self)-> int :
        """Getter für die Lenkwinkel-Abfrage, gibt Winkel als int zurück"""
        return self._steering_angle
    
    @steering_angle.setter
    def steering_angle(self, angle: int)-> None:
        """Setter für Lenkwinkel
        Args:
        angle(int): Lenkwinkel, welcher eingestellt werden soll
        Eingabewert zwischen 45 und 135
        """
        self._steering_angle = angle
        self.fw.turn(angle)
    
    @property
    def direction(self)-> int:
        """Getter für Einstellung der Fahrtrichtung
            -1 : Rückwärts
            0  : STOP
            1  : Vorwärts
        """
        return self._direction

    @property
    def speed(self)-> int:
        """Getter für Geschwindigkeit
        Einstellung zwischen 0 und 100"""
        return self._speed

    @speed.setter
    def speed(self, speed: int)-> None:
        """Setter für Geschwindigkeit
        Args:
        speed(int): Setzen der Umdrehungsgeschwindigkeit der Räder
        """
        self._speed = speed
        self.bw.speed = speed
    
    def drive(self, speed:int, direction:int) -> None:
        """Methode zum Fahren
        
        Args: 
        Geschwindigkeit und Fahrtrichtung
        speed(int): Setzen der Umdrehungsgeschwindigkeit der Räder (0 und 100)
        direction(int): Einstellung der Fahrtrichtung
            -1 : Rückwärts
            0  : STOP
            1  : Vorwärts
        """
       
        self.speed = speed

        if direction == 1:
            print("Fahre vorwärts")
            self._direction = 1
            self.bw.forward()
        elif direction == -1:
            print("Fahre rückwärts")
            self._direction = -1
            self.bw.backward()
            
        elif direction == 0:
            print("Stop")
            self._direction = 0
            self.bw.stop()
        else:
            print("Ungültige Fahrtrichtungsangabe")
    
    def stop(self) -> None:
        """Methode zum Stoppen
        
        """
        self.bw.stop()
