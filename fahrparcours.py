from basecar import *
import click
import time

@click.command()
@click.option('--modus', '--m', type=int, default=None, help="Startet Test für Klasse direkt.")
def main(modus):
    """Function for choosing the parcours


    Args:
        modus (int): The mode that can be choosen by the user
    """
    print('-- Auswahl der Fahrfunktionen --------------------')
    modi = {
        0: 'Ausrichtung der Servo der Lenkung auf Geradeaus',
        1: 'Fahrparcours 1 - Vorwärts und Rückwärts',
        2: 'Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel',
        # 3: 'Test Ultraschallmodul / Klasse: Ultrasonic',
        # 4: 'Test Infrarotmodul / Klasse: Infrared',
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
        bc = BaseCar()
        bc.steering_angle = 45
        time.sleep(.5)
        bc.steering_angle = 135
        time.sleep(.5)
        bc.steering_angle = 90
        x=input('Servo der Lenkung auf 90 Grad/geradeaus ausgerichtet! (ENTER zum beenden)')

    if modus == 1:
        x = input('ACHTUNG! Das Auto wird ein Stück vor und zurück fahren!\n Drücken Sie ENTER zum Start.')
        if x == '':
            print('Fahrparcours 1')
            bc = BaseCar()
            bc.drive(30, 1)
            time.sleep(3)
            bc.drive(0, 0)
            time.sleep(1)
            bc.drive(30, -1)
            time.sleep(3)
            bc.drive(0, 0)
            print("Ende des Parcours.")
        else:
            print('Abbruch.')

    if modus == 2:
        
        x = input(' ACHTUNG! Das Auto wird nach kurzer Geradeausfahrt verschiedene Kreise fahren!\n Drücken Sie ENTER zum Start.')
        if x == '':
            print('Fahrparcours 2')
            bc = BaseCar()
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
        else:
            print('Abbruch.')
        


if __name__ == '__main__':
    main()