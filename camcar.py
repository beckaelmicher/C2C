from ir_car import * 
from basisklassen_cam import Camera
import cv2
import Beispiele.image_processing as ip
import matplotlib.pylab as plt

class CamCar(IRCar):
    
    camera = Camera(flip=True, height=480, width=640)

    def __init__(self) -> None:
        super().__init__()
        self.x_position = 0
        self.imgTemplate = 0
        self.frame = 0

   
    def stream(self):
        # Kamera-Objekt liefert aktuelles Bild als Numpy-Array
        # frame = self.camera.get_frame()
        # # Einige beipielhafte Manipulationen des Bildes
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.blur(frame, (5,5))
        # frame = ip.roi(frame, upper=0.6, under=0.2)

        # Lesen der Template-Bilder als Array in self.imgTemplate
        #self.imgTemplate = frame[150:250,50:590].copy()
        bilder_liste = []
        #bilder_liste = ['images/Gerade.png', 'images/Linkskurve.png', 'images/Rechtskurve.png']
        template_liste = []
        for i in range(len(bilder_liste)):
            template_liste.append(cv2.imread(bilder_liste[i]))

        while True:
            # Kamera-Objekt liefert aktuelles Bild als Numpy-Array
            self.frame = self.camera.get_frame()

            #img3 = self.quality_check(frame, template_liste)

            # Erstellen des Bytecode für das Bild/Videostream aus dem aktuellen Frame als NumPy-Array
            _, x = cv2.imencode(".jpeg", self.frame)
            x_bytes = x.tobytes()

            yield (
                b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + x_bytes + b"\r\n\r\n"
            )
    
    def quality_check(self, frame, temp_liste):
        # Einige beipielhafte Manipulationen des Bildes
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.blur(frame, (5,5))
        frame = ip.roi(frame, upper=0.6, under=0.2)
        # for-Schleife im Template-Bild-Array zur Prüfung des geringsten min_val mit merken des min_val_index
        temp_min_val = 1000000
        temp_min_loc = (50, 200)
        for bild in temp_liste:
            bild = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(frame, bild, cv2.TM_SQDIFF) 
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if min_val < temp_min_val:
                temp_min_val = min_val
                temp_min_loc = min_loc
            
        # Mittels min_val_index Bestimmung des min_loc
        top_left = temp_min_loc
        self.x_position = top_left[0]
        #-------------------------
        # Zeichnen der Boundary Box
        ht,wt = bild.shape
        bottom_right = (top_left[0] + wt, top_left[1] + ht)
        image=cv2.rectangle(frame.copy(), top_left, bottom_right, (255,0,0), 3)
        return image