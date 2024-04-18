from ir_car import * 
from basisklassen_cam import Camera
import cv2
#from fahrparcours_dash import *

class CamCar(IRCar):
    
    camera = Camera(flip=True, height=480, width=640)

    def __init__(self) -> None:
        super().__init__()
   
    def stream(self):
        # Kamera-Objekt liefert aktuelles Bild als Numpy-Array
        frame = self.camera.get_frame()
        # Einige beipielhafte Manipulationen des Bildes
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.blur(frame, (5,5))
        frame = cv2.Canny(frame, 0, 100)
        frame = cv2.normalize(frame, frame, alpha=5, norm_type=cv2.NORM_MINMAX)
        # canny = cv2.Canny(gray, 100, 200)
        frame = frame[150:350,0:640].copy()
        imgTemplate = frame[100:170,50:590].copy()

        while True:
            # Kamera-Objekt liefert aktuelles Bild als Numpy-Array
            frame = self.camera.get_frame()
            # Einige beipielhafte Manipulationen des Bildes
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.blur(frame, (5,5))
            frame = cv2.Canny(frame, 0, 100)
            frame = cv2.normalize(frame, frame, alpha=5, norm_type=cv2.NORM_MINMAX)
            # canny = cv2.Canny(gray, 100, 200)
            frame = frame[200:480,0:640].copy()
            res = cv2.matchTemplate(frame, imgTemplate,cv2.TM_SQDIFF) 
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            top_left = min_loc
            x_position = top_left[0]
            #-------------------------
            # Zeichnen der Boundary Box
            ht,wt = imgTemplate.shape
            bottom_right = (top_left[0] + wt, top_left[1] + ht)
            img3=cv2.rectangle(frame.copy(), top_left, bottom_right, (255,0,0), 3)

            # Erstellen des Bytecode für das Bild/Videostream aus dem aktuellen Frame als NumPy-Array
            _, x = cv2.imencode(".jpeg", img3)
            x_bytes = x.tobytes()


            self.steering_angle = 0.9 * x_position + 45
            # if x_position < 25: 
            #     self.steering_angle = 45
            # elif x_position > 75:
            #     self.steering_angle = 135
            # elif x_position < 37: 
            #     self.steering_angle = 68
            # elif x_position > 62:
            #     self.steering_angle = 112
            # else:
            #     self.steering_angle = 90
            

            yield (
                b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n" + x_bytes + b"\r\n\r\n"
            )
