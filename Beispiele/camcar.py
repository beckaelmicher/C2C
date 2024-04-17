from basecar import BaseCar
from basisklassen_cam import Camera
import time
import image_processing as ip
import numpy as np
import cv2
from datetime import datetime
import uuid
import os

class CamCar(BaseCar):
    def __init__(self, config="config.json"):
        super().__init__(config)
        self.speed = 30
        self.cam = Camera()
        self.frame = self.cam.get_frame()
        self.roi = self.frame
        self.filtered = self.frame
        self.point = self.frame
        self.driving = False
        self.saving = False
        self.images = {"Original": self.frame, "ROI": self.roi, 
                       "Filtered": self.filtered, "Points": self.point}
        self.streaming_image = "Original"
        self.hsv_lower = np.array([0, 50, 50])
        self.hsv_upper = np.array([50, 255, 255])
        self.roi_upper = 1
        self.roi_lower = 1
        self.new_angle = 90
        self.last_angle = 90
        self.last_line1 = (0, [0, 0])
        self.last_line2 = (0, [0, 0])
        self.steering_method = "cv2"
        self.path = "./images/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def cv2_angle(self, frame):
        self.roi = ip.roi(self.frame, upper=self.roi_upper, under=self.roi_lower)
        self.filtered = ip.filter_color(self.roi, self.hsv_lower, self.hsv_upper)
        ly, lx, ry, rx = ip.get_lane_points(self.filtered)

        print(lx)

        ly = ip.drop_outlier_points(ly)
        lx = ip.drop_outlier_points(lx)
        ry = ip.drop_outlier_points(ry)
        rx = ip.drop_outlier_points(rx)

        print("LX: ", lx)
        print("RX: ", rx)
        try:
            line1 = ip.fit_line(lx[::-1], ly)
            line2 = ip.fit_line(rx[::-1], ry)
        except:
            line1 = self.last_line1
            line2 = self.last_line2

        distance = ip.distance(lx, rx, self.filtered.shape[1])

        if distance < 0.4:
            print("Vermutlich nur eine Linie erkannt")
            #! Welche Linie soll genommen werden?
            # ? Die mit größerer y Summe?
        self.point = ip.draw_points(self.roi, ly, lx)
        self.point = ip.draw_points(self.point, ry, rx)
        delta_angle = (line1[0]+line2[0])/2
        self.steering_angle = int(max(45, min(90 + delta_angle, 135)))

    def save_image(self, image_id, run_id, frame):
        current_time = datetime.now().strftime("%Y%m%d_%H-%M-%S")
        filename = f"IMG_{run_id}_{current_time}_{image_id}_{self.steering_angle}.jpg"
        cv2.imwrite(self.path + filename, frame)

    def stream(self):
        image_id = 0
        run_id = str(uuid.uuid4())[:8]
        while True:
            self.frame = self.cam.get_frame()
            self.frame = ip.resize(self.frame)

            self.roi = ip.roi(self.frame, upper=self.roi_upper, under=self.roi_lower)
            self.filtered = ip.filter_color(self.roi, self.hsv_lower, self.hsv_upper)
            ly, lx, ry, rx = ip.get_lane_points(self.filtered)

            ly = ip.drop_outlier_points(ly)
            lx = ip.drop_outlier_points(lx)
            ry = ip.drop_outlier_points(ry)
            rx = ip.drop_outlier_points(rx)

            try:
                line1 = ip.fit_line(lx[::-1], ly)
                line2 = ip.fit_line(rx[::-1], ry)
            except:
                line1 = self.last_line1
                line2 = self.last_line2

            distance = ip.distance(lx, rx, self.filtered.shape[1])

            if distance < 0.4:
                print("Vermutlich nur eine Linie erkannt")
                #! Welche Linie soll genommen werden?
                # ? Die mit größerer y Summe?
            #print("Steigung Links: ", line1)
            #print("Steigung Rechts: ", line2)
            self.point = ip.draw_points(self.roi, ly, lx)
            self.point = ip.draw_points(self.point, ry, rx)
            delta_angle = (line1[0]+line2[0])/2
            self.steering_angle = int(max(45, min(90 + delta_angle, 135)))
            if self.saving:
                self.save_image(image_id, run_id, self.frame)
                image_id += 1
            
            if self.streaming_image == "Original":
                _, displayed_image = cv2.imencode(".jpeg", self.frame)
            if self.streaming_image == "ROI":
                _, displayed_image = cv2.imencode(".jpeg", self.roi) 
            if self.streaming_image == "Filtered":
                _, displayed_image = cv2.imencode(".jpeg", self.filtered) 
            if self.streaming_image == "Points":
                _, displayed_image = cv2.imencode(".jpeg", self.point) 

            x_bytes = displayed_image.tobytes()
            x_string = (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + x_bytes + b'\r\n\r\n')
            yield x_string
