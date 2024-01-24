from ir_car import *
import click
from datetime import datetime as dt
import time
import pandas as pd
import random
import json

# Anlegen der benötigten Instanzen
bc = BaseCar()  # Fahrparcours 1 und 2
sc = SonicCar() # Fahrparcours 3 und 4
irc = IRCar()   # Fahrparcours 5 (bis 7)

# Anlegen der Listen ausgelagert, damit die Messung per Methode aufrufbar ist
list_timestamp = []
list_time = []
list_speed = []
list_direction = []
list_steeringangle = []
list_distance = []
time_alt = dt.now()
time_alt = time_alt.timestamp()
csv_dateipfad = 'messergebnisse.csv'
mess_ergebnis = 0
abstand = 0

def recording_panda_lists(car):
    """Funktion zum Anhängen der Messdaten in den Listen

    Args:
        car (object): Übergabe des im jeweiligen Fahrparcours verwendeten Fahrzeugobjekts (bc / sc / irc)
    """
    time = dt.now()
    time = time.timestamp()
    time_diff = time-time_alt
    list_timestamp.append(dt.now().strftime("%H:%M:%S.%f")[:11])
    list_time.append(round(time_diff, 5))
    list_speed.append(car.speed)
    list_direction.append(car.direction)
    list_steeringangle.append(car.steering_angle)
    list_distance.append(abstand)

def list_2_csv():
    """Funktion zum Schreiben der Messergebnisse aus den Listen in die CSV-Datei mittels Pandas
    """
    messergebnisse = pd.DataFrame({
        "Timestamp": list_timestamp,
        "Time": list_time,
        "Speed": list_speed,
        "Direction": list_direction,
        "SteeringAngle": list_steeringangle,
        "Distance": list_distance
    })
    global mess_ergebnis
    if mess_ergebnis == 0:
        # Neu angelegte CSV-Datei mit Header
        messergebnisse.to_csv(csv_dateipfad, index=False)    
        mess_ergebnis = 1
    else:
        # In vorhandener CSV-Datei anhängen mit mode="a" (append) und ohne Header
        messergebnisse.to_csv(csv_dateipfad, index=False, mode="a", header=False)

def fahrparcours_1():
    try:
        bc.drive(30, 1)
        time.sleep(3)
        bc.drive(0, 0)
        time.sleep(1)
        bc.drive(30, -1)
        time.sleep(3)
        bc.drive(0, 0)
    except KeyboardInterrupt:
        pass

def stop():
    list_2_csv()
    bc.stop()   # Fahrzeug anhalten
    bc.steering_angle = 90  # Lenkung gerade ausrichten

def fahrparcours_3():
    no_obstacle = True
    sc.steering_angle = 90

    # Fahrfunktion asuführen, so lange kein Hindernis erkannt wird
    while no_obstacle:
        # Speichern des aktuellen Abstands zur Verwendung beim Stoppen und beim Loggen
        abstand = sc.abstand
        # Bei Prüfung des Abstands, Ausschluss möglicher negativer Fehlercodes (<0)
        if abstand > 20 or abstand < 0:
            print("Drive - Abstand =", abstand)
            sc.drive(40, 1)
        else:
            print("Halt - Abstand = ", abstand)
            no_obstacle = False
            print("Hindernis erkannt!")
            sc.stop()
        recording_panda_lists(sc)

    list_2_csv()

    sc.stop()   
 
# def simulate_ctrl_c():
#     keyboard.press_and_release('ctrl+c')
 
# # Beispiel: Tastenkombination nach 3 Sekunden simulieren
# time.sleep(3)
# simulate_ctrl_c()