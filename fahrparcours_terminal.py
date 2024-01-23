from ir_car import *
import click
from datetime import datetime as dt
import time
import pandas as pd
import random
import json

# Click wird benötigt für die Modus-Auswahl im Terminal
@click.command() 
@click.option('--modus', '--m', type=int, default=None, help="Startet Test für Klasse direkt.")
def main(modus):
    """Function for choosing the parcours

    Args:
        modus (int): The mode that can be choosen by the user
    """
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
        # "mess_ergebnis" muss nochmal als global definiert werden, 
        # damit es nicht als lokale Variabe in folgender Abfrage angelegt wird
        nonlocal mess_ergebnis
        if mess_ergebnis == 0:
            # Neu angelegte CSV-Datei mit Header
            messergebnisse.to_csv(csv_dateipfad, index=False)    
            mess_ergebnis = 1
        else:
            # In vorhandener CSV-Datei anhängen mit mode="a" (append) und ohne Header
            messergebnisse.to_csv(csv_dateipfad, index=False, mode="a", header=False)

    # Try-Block, um Fahrprogramme mit STRG-C unterbrechen zu können
    try:
        # (Wiederholte) Anzeige des Auswahlmenüs, bis Programm abgebrochen wird
        while True:
            print('------ Auswahl der Fahrfunktionen ------')
            modi = {
                0: 'Ausrichtung der Servo der Lenkung auf Geradeaus',
                1: 'Fahrparcours 1 - Vorwärts und Rückwärts',
                2: 'Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel',
                3: 'Fahrparcours 3 - Vorwärtsfahrt bis Hindernis',
                4: 'Fahrparcours 4 - Erkundungstour',
                5: 'Fahrparcours 5 - Linienverfolgung'
            }

            # Anzeige des Auswahlmenüs
            if modus == None:
                print('--' * 20)
                print('Auswahl:')
                for m in modi.keys():
                    print('{i} - {name}'.format(i=m, name=modi[m]))
                print('--' * 20)

            # Auswahl des gewünschten Fahrparcours
            while modus == None:
                try:
                    modus_list = list(modi.keys())
                    modus = int(input('Wähle  (Andere Taste für Abbruch): ? '))
                    modus = modus_list[modus]
                    break
                except:
                    print('Getroffene Auswahl nicht möglich.')
                    quit()

            # Fahrprofil 0 zum Ausrichten und Testen der Lenkung aus Basisklassen-Test übernommen
            if modus == 0:
                print('Der Servomotor wird nach rechts und links bewegt und dann auf geradeus ausgerichtet.')
                bc.steering_angle = 45
                time.sleep(.5)
                bc.steering_angle = 135
                time.sleep(.5)
                bc.steering_angle = 90
                x=input('Servo der Lenkung auf 90 Grad/geradeaus ausgerichtet! (ENTER zum beenden)')
                modus = None
            
            # Fahrparcours 1 basierend auf BaseCar
            if modus == 1:
                x = input('ACHTUNG! Das Auto wird ein Stück vor und zurück fahren!\n Drücken Sie ENTER zum Start.')
                if x == '':
                    print('Fahrparcours 1')
                    bc.drive(30, 1)
                    time.sleep(3)
                    bc.drive(0, 0)
                    time.sleep(1)
                    bc.drive(30, -1)
                    time.sleep(3)
                    bc.drive(0, 0)
                    print("Ende des Parcours.")
                    modus = None
                else:
                    print('Abbruch.')
                    modus = None

            # Fahrparcours 2 basierend auf BaseCar
            if modus == 2:
                x = input(' ACHTUNG! Das Auto wird nach kurzer Geradeausfahrt verschiedene Kreise fahren!\n Drücken Sie ENTER zum Start.')
                if x == '':
                    print('Fahrparcours 2')
                    bc.steering_angle = 90
                    bc.drive(30, 1)
                    time.sleep(1)
                    bc.steering_angle = 135
                    time.sleep(8)
                    bc.drive(0, 0)
                    bc.drive(30, -1)
                    time.sleep(8)
                    bc.steering_angle = 90
                    time.sleep(1)
                    bc.drive(0, 0)
                    time.sleep(.5)
                    bc.drive(30, 1)
                    time.sleep(1)
                    bc.steering_angle = 45
                    time.sleep(8)
                    bc.drive(0, 0)
                    bc.drive(30, -1)
                    time.sleep(8)
                    bc.steering_angle = 90
                    time.sleep(1)
                    bc.drive(0, 0)
                    print("Ende des Parcours.")
                    modus = None
                else:
                    print('Abbruch.')
                    modus = None

            # Fahrparcours 3 basierend auf SonicCar
            if modus == 3:
                x = input('ACHTUNG! Das Auto fährt vorwärts bis zum ersten Hindernis!\n Drücken Sie ENTER zum Start.')
                if x == '':
                    print('Fahrparcours 3')
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
                    print("Ende des Parcours.")
                    modus = None
                else:
                    print('Abbruch.')
                    modus = None

            # Fahrparcours 4 basierend auf SonicCar
            if modus == 4: 
                hindernisse = int(input("Wieviele Hindernisse dürfen es sein?: "))
                x = input('ACHTUNG! Das Auto bewegt sich eigenständig durch den Raum!\n Drücken Sie ENTER zum Start.')
                
                if x == '':
                    print('Fahrparcours 4')
                    sc.steering_angle = 90

                    # Fahrzeug fährt bis Anzahl an Hindernissen erkannt
                    while hindernisse > 0:
                        # Speichern des aktuellen Abstands zur Verwendung beim Stoppen und beim Loggen
                        abstand = sc.abstand
                        # Bei Prüfung des Abstands, Ausschluss möglicher negativer Fehlercodes (<0)
                        if abstand > 20 or abstand < 0:
                            sc.drive(30, 1)
                        else:
                            # Ausweichroutine bei erkanntem Hindernis
                            print("Hindernis erkannt!")
                            print("Abstand: ", sc.abstand)                            
                            sc.stop()
                            # Zufällige Auswahl vollständiger Lenkeinschlag nach links oder rechts
                            sc.steering_angle = random.choice([45, 135])
                            sc.drive(30, -1)
                            time.sleep(2)
                            sc.stop()
                            sc.steering_angle = 90
                            hindernisse -= 1
                        recording_panda_lists(sc)

                    list_2_csv()

                    sc.stop()   
                    print("Ende des Parcours.")
                    modus = None
                else:
                    print('Abbruch.')
                    modus = None
            
            # Fahrparcours 5 basierend auf IRCar
            if modus == 5:
                x = input('ACHTUNG! Das Auto folgt einer Linie und hält vor Hindernissen!\n Drücken Sie ENTER zum Start.')
                
                if x == '':
                    # Einlesen eines individuellen Schwellwertes aus config-Datei
                    try:
                        with open("config.json", "r") as f:
                            data = json.load(f)
                            schwellwert = data["IR_schwellwert"]
                    except:
                        print("Keine geeignete Datei config.json gefunden!")

                    black_line = True
                    # Fahrfunktion ausführen so lange wie eine schwarze Linie erkannt wird
                    while black_line:
                        # Anlegen einer Liste mit den gemessenen Werten des IR-Sensors
                        ls = irc.ir_werte
                        print("--"*20)
                        print("IR-Werte: ", ls)

                        # Ermittlung des Minimalwerts und des zugehörigen List-Indexes (für den einzelen Sensor)
                        min_val = ls[0]
                        min_val_idx = 0
                        for i in range (len(ls)):
                            if ls[i] <= min_val:
                                min_val = ls[i]
                                min_val_idx = i
                                 
                        # Abfrage ob äußere Sensoren die Linie erkannt haben, um direkt stark zu lenken
                        if min_val_idx == 0:
                            irc.steering_angle = 45
                        elif min_val_idx == 4:
                            irc.steering_angle = 135
                        # wird die Linie durch einen der beiden inneren Sensoren erkannt, wird nur leicht gelenkt        
                        elif min_val_idx == 1:
                            irc.steering_angle = 68
                        elif min_val_idx == 3:
                            irc.steering_angle = 112
                        # wird die Linie durch den mittleren Sensor ekannt, wird geradeaus gelenkt
                        else:
                            irc.steering_angle = 90

                        # Speichern des aktuellen Abstands zur Verwendung beim Stoppen und beim Loggen
                        abstand = irc.abstand
                        # Bei Prüfung des Abstands, Ausschluss möglicher negativer Fehlercodes (<0)
                        if abstand < 15 and abstand > 0:            
                            print("Hindernis erkannt - halte an!")
                            irc.stop()
                            recording_panda_lists(irc)
                            # Bei erkanntem Hindernis anhalten und While-Schleife verlassen 
                            break
                        # Fahrprogramm zum Folgen der schwarzen Linie
                        else:
                            irc.drive(30, 1)
                            recording_panda_lists(irc)
                            # Berechnung der Standardabweichung der IR-Werte mittels Pandas
                            ir_std = pd.Series(ls).std()
                            print("IR-Standardabweichung: ", ir_std)
                            # Setzen des aktuellen Minimalwerts
                            ir_min = min(ls)
                            print("IR-Minimalwert: ", ir_min)
                            print("Index Sensor mit Minimalwert: ", min_val_idx)

                            # Abfrage ob äußere Sensoren zuletzt die schwarze Linie erkannt haben
                            # und anschließend kein Sensor mehr die Linie erkennt
                            if ((min_val_idx == 4) or (min_val_idx == 0)) and (ir_std < schwellwert) and (ir_min > schwellwert):
                                print("Kurve zu eng")
                                # Fahrmanöver zum wieder Auffinden der Linie einleiten
                                irc.drive(20, 1)
                                recording_panda_lists(irc)
                                time.sleep(0.5)
                                irc.stop()
                                recording_panda_lists(irc)
                                time.sleep(0.1)
                                if min_val_idx == 0 or min_val_idx == 1:
                                    irc.steering_angle = 135
                                    recording_panda_lists(irc)
                                elif min_val_idx == 3 or min_val_idx == 4:
                                    irc.steering_angle = 45
                                    recording_panda_lists(irc)
                                irc.drive(30, -1)
                                recording_panda_lists(irc)
                                time.sleep(0.5)
                                # Nach Fahrmanöver Fortsetzen des Fahrparcours
                                continue

                            # Abfrage auf Spezialfall "scharfe Rechtskurve" 
                            # bei dem die drei rechten Sensoren alle eine Linie erkennen
                            if (ls[2] < schwellwert) and (ls[3] < schwellwert) and (ls[4] < schwellwert):
                                irc.steering_angle = 45
                                irc.drive(30, -1)
                                recording_panda_lists(irc)
                                time.sleep(0.5)
                                irc.steering_angle = 135
                                irc.drive(30, 1)
                                recording_panda_lists(irc)
                                time.sleep(0.5)
                                # Nach Fahrmanöver Fortsetzen des Fahrparcours
                                continue

                            # Abfrage auf Spezialfall "scharfe Linkskurve" 
                            # bei dem die drei linken Sensoren alle eine Linie erkennen
                            if (ls[2] < schwellwert) and (ls[1] < schwellwert) and (ls[0] < schwellwert):
                                irc.steering_angle = 135
                                irc.drive(30, -1)
                                recording_panda_lists(irc)
                                time.sleep(0.5)
                                irc.steering_angle = 45
                                irc.drive(30, 1)
                                recording_panda_lists(irc)
                                time.sleep(0.5)
                                # Nach Fahrmanöver Fortsetzen des Fahrparcours
                                continue

                            # Abfrage ob Linie zu ende
                            if (ir_std < schwellwert/2) and (ir_min > schwellwert): 
                                # Hinweis: Schwellenwert nochmals optimieren, ggf. in Echtzeit messen
                                print("Halte an, Linie verlassen!")
                                black_line = False
                                irc.steering_angle = 90
                                irc.stop()
                                recording_panda_lists(irc)
                    irc.stop()
                    recording_panda_lists(irc)
                    list_2_csv()   
                    print("Ende des Parcours.")
                    modus = None
                else:
                    print('Abbruch.')
                    modus = None                

    # Möglichkeit zum Programmabbruch und Stoppen des Fahrzeugs durch STRG+C
    except KeyboardInterrupt:
        print("\nProgramm abgebrochen!")
        list_2_csv()
        bc.stop()   # Fahrzeug anhalten
        bc.steering_angle = 90  # Lenkung gerade ausrichten


if __name__ == '__main__':
    main()