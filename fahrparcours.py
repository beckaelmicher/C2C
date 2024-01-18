from basecar import *
from soniccar import *
import click
from datetime import datetime as dt
import time
import pandas as pd

@click.command()
@click.option('--modus', '--m', type=int, default=None, help="Startet Test für Klasse direkt.")
def main(modus):
    """Function for choosing the parcours


    Args:
        modus (int): The mode that can be choosen by the user
    """
    bc = BaseCar()
    sc = SonicCar()

    # Messergebnis und Listen ausgelagert, damit per Methode aufrufbar wird.
    #global mess_ergebnis
    list_time = []
    list_time_delta = []
    list_speed = []
    list_direction = []
    list_steeringangle = []
    list_distance = []
    time_alt = dt.now()
    time_alt = time_alt.timestamp()
    csv_dateipfad = 'messergebnisse.csv'
    mess_ergebnis = 0

    def recording_panda_lists():
        time = dt.now()
        time = time.timestamp()
        time_diff = time-time_alt
        list_time.append(dt.now().strftime("%H:%M:%S.%f")[:11])
        list_time_delta.append(round(time_diff, 5))
        list_speed.append(sc.speed)
        list_direction.append(sc.direction)
        list_steeringangle.append(sc.steering_angle)
        list_distance.append(sc.abstand)

    def list_2_csv(mess_ergebnis):
        messergebnisse = pd.DataFrame({
            "Timestamp": list_time,
            "timedelta": list_time_delta,
            "Speed": list_speed,
            "Direction": list_direction,
            "SteeringAngle": list_steeringangle,
            "Distance": list_distance
        })

        if mess_ergebnis == 0:
            messergebnisse.to_csv(csv_dateipfad, index=False)    
            mess_ergebnis = 1
        else:
            messergebnisse.to_csv(csv_dateipfad, index=False, mode="a", header=False)


    try:
        while True:
            print('-- Auswahl der Fahrfunktionen --------------------')
            modi = {
                0: 'Ausrichtung der Servo der Lenkung auf Geradeaus',
                1: 'Fahrparcours 1 - Vorwärts und Rückwärts',
                2: 'Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel',
                3: 'Fahrparcours 3 - Vorwärtsfahrt bis Hindernis',
                4: 'Fahrparcous 4 - Erkundungstour',
                # 5: 'Test Hinter- und Vorderräder unter Verwendung der Konfigurationen in config.json',
            }
            
            if modus == None:
                print('--' * 20)
                print('Auswahl:')
                for m in modi.keys():
                    print('{i} - {name}'.format(i=m, name=modi[m]))
                print('--' * 20)

            while modus == None:
                try:
                    modus_list = list(modi.keys())
                    modus = int(input('Wähle  (Andere Taste für Abbruch): ? '))
                    modus = modus_list[modus]
                    break
                except:
                    print('Getroffene Auswahl nicht möglich.')
                    quit()

            if modus == 0:
                print('Der Servomotor wird nach rechts und links bewegt und dann auf geradeus ausgerichtet.')
                bc.steering_angle = 45
                time.sleep(.5)
                bc.steering_angle = 135
                time.sleep(.5)
                bc.steering_angle = 90
                x=input('Servo der Lenkung auf 90 Grad/geradeaus ausgerichtet! (ENTER zum beenden)')
                modus = None
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
            if modus == 3:
                x = input('ACHTUNG! Das Auto fährt vorwärts bis zum ersten Hindernis!\n Drücken Sie ENTER zum Start.')
                if x == '':
                    print('Fahrparcours 3')
                    no_obstacle = True
                    sc.steering_angle = 90

                    while no_obstacle:
                        
                        # print(sc.abstand)
                        if sc.abstand > 10 or  sc.abstand < 0:
                            sc.drive(30, 1)
                        else:
                            no_obstacle = False
                            print("Hindernis")
                            print(sc.abstand)
                            sc.stop()
                        recording_panda_lists()

                    list_2_csv(mess_ergebnis)

                    sc.stop()   
                    print("Ende des Parcours.")
                    modus = None
                else:
                    print('Abbruch.')
                    modus = None

            if modus == 4: 
                x = input('ACHTUNG! Das Auto bewegt sich eigenständig durch den Raum!\n Drücken Sie ENTER zum Start.')
                if x == '':
                    print('Fahrparcours 4')

                        # tbd!
                    print("Ende des Parcours.")
                    modus = None
                else:
                    print('Abbruch.')
                    modus = None
    except KeyboardInterrupt:
        print("\nProgramm abgebrochen!")
        bc.stop()   # Fahrzeug anhalten
        bc.steering_angle = 90  # Lenkung gerade ausrichten


if __name__ == '__main__':
    main()