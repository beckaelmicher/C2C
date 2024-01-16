
**3. Klasse: BaseCar** - Mittwoch

Datei: basecar.py mit Class BaseCar erbt von FrontWheels, BackWheels

• steering_angle: Setzen und Zugriff auf den Lenkwinkel (Property mit Setter)
• speed: Setzen und Zugriff auf die Geschwindigkeit (Property mit Setter)
• direction: Zugriff auf die Fahrrichtung (1: vorwärts, 0: Stillstand, ‑1 Rückwärts) (Property ohne Setter)
• drive(speed:int, direction:int): Methode zum Setzen von Geschwindigkeit und Fahrrichtung
• stop: Methode zum Anhalten des Autos. Sie setzt die Geschwindigkeit auf Null und den Lenkwinkel auf Geradeaus.

Prüfen Sie, ob die Properties steering_angle, speed und direction immer die korrekten Werte liefern. Dies muss unabhängig von der Verwendungsgeschichte einer korrekten Instanz gewährleistet sein. Die Klasse BaseCar soll mittels der folgenden Aufgaben getestet werden.

In Main einbauen welcher Parcour und dementsprechend Methoden aufrufen.

Während dieser Fahrten sollen die Fahrdaten so aufgezeichnet werden, dass diese nach der Fahrt von der Instanz abgefragt werden und beispielsweise gespeichert oder anderweitig verarbeitet werden können. Die Fahrdaten umfassen die Geschwindigkeit, die Fahrtrichtung, den Lenkwinkel und die Daten des Ultraschallsensors. Die Daten sollen die verschiedenen Steueranweisungen und die ihnen zugrunde liegenden Sensordaten einer Fahrt reflektieren.

**4. Klasse: SonicCar** - Donnerstag

Datei: soniccar.py mit Class SonicCar erbt von BaseCar und Ultrasonic

• Fahrparcours 3 ‑ Vorwärtsfahrt bis Hindernis: Fahren bis ein Hindernis im Weg ist und dann stoppen. 
• Fahrparcours 4 ‑ Erkundungstour: Das Auto soll bei freier Fahrt die Fahrrichtung, und optional auch die Geschwindigkeit, variieren. Im Falle eines Hindernisses soll das Auto die Fahrrichtung ändern und die Fahrt dann fortsetzen. Zur Änderung der Fahrrichtung ist dabei ein maximaler Lenkwinkel einzuschlagen und rückwärts zu fahren. Als Ergebnis soll das Auto den hindernsfreien Raum “erkunden”. Die genaue Gestaltung obliegt Ihnen.

**5. Visualiserung der Fahrdaten mit Dash** - Freitag

...

**6. Klasse: SensorCar** - Montag/Dienstag

Datei: sensorcar.py mit Class SensorCar erbt von SonicCar ?? und Infrared

• Fahrparcours 5 ‑ Linienverfolgung : Folgen einer etwas 1,5 bis 2 cm breiten Linie auf dem Boden. Das Auto soll stoppen, sobald das Auto das Ende der Linie erreicht hat. Als Test soll eine Linie genutzt werden, die sowohl eine Rechts‑ als auch eine Linkskurve macht. Die Kurvenradien sollen deutlich größer sein als der maximale Radius, den das Auto ohne ausgleichende Fahrmanöver fahren kann. 
• Fahrparcours 6 ‑ Erweiterte Linienverfolgung: Folgen eine Linie, die sowohl eine Rechts‑ als auch eine Linkskurve macht mit Kurvenradien kleiner als der maximale Lenkwinkel.

**7. Fahrparcours 7: Erweiterte Linienverfolgung mit Hindernisserkennung (Optional):** - Dienstag / Mittwoch

...

**8. Nutzer Interface** - Mittwoch / Donnerstag

...
