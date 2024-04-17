import cv2
import numpy as np
import math 

def resize(image, factor=0.5):
    if image is not None:
        width = int(image.shape[1]*factor)
        height = int(image.shape[0]*factor)
        dim = (width, height)
        return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    else:
        return image

def roi(image, upper: float=0.4, under: float=0.2, left: float=0.025, right: float=0.025, scale=1): 

    height = image.shape[0]
    width = image.shape[1]
    
    polygon = np.float32([
                        (int(width*left), int(height*upper)),
                        (width*(1-right), height*upper),
                        (width, height*(1-under)),
                        (int(0), int(height*(1-under))),  
                        ]) 

    output = np.float32([(0, 0), # oben links
                        (width, 0), #oben rehcts
                        (width, height), #unten rechts
                        (0, height)]) #unten links
    
    M = cv2.getPerspectiveTransform(polygon, output)
    warped = cv2.warpPerspective(image, M, (int(width*scale), int(height*scale)), flags=cv2.INTER_LINEAR)
    return warped#[::-1, ::-1, :]



def filter_color(image: np.array, lower=np.array([90,40,200]), upper=np.array([130,255,255])):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def detect_line_segments(image: np.array):
    """Uses HoughLinesP to detect connected lines in an image

    Args:
        image (np.array): image with lines in it

    Returns:
        np.array: lines of the image
    """
    
    rho = 1  # precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # degree in radian, i.e. 1 degree
    min_threshold = 10 
    line_segments = cv2.HoughLinesP(image, rho, angle, min_threshold, np.array([]), minLineLength=8,
                                    maxLineGap=10)
    return line_segments


def make_points(image: np.array, line: np.array):

    height, width, _ = image.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]
    

def average_slope_intercept(image: np.array, line_segments: np.array, boundary = 0.5):

    lane_lines = []
    if line_segments is None:
        return lane_lines

    _, width, _ = image.shape
    left_fit = []
    right_fit = []

    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(image, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(image, right_fit_average))

    return lane_lines

def add_lines_to_image(image: np.array, lines: list, line_color: tuple=(0, 255, 0), line_width: int=3):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(image, 1, line_image, .3, 1)
    return line_image

def compute_steering_angle(image: np.array, lane_lines: np.array, camera_mid_offset_percent=0.0):

    if len(lane_lines) == 0:
        return 90

    height, width, _ = image.shape

    if len(lane_lines) == 1:
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        mid = int(width / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid

    y_offset = int(height / 2)

    angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
    steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed by picar front wheel

    return max(35, steering_angle, min(135, steering_angle))

def get_lane_points(col_filtered_image, side_crop=0.3, top_crop=0.2, n_windows=20):
    left_points_y = []
    right_points_y = []
    left_points_x = []
    right_points_x = []

    height = col_filtered_image.shape[0]
    width = col_filtered_image.shape[1]
    height_cropped = int(height*(1-top_crop))

    left_side = col_filtered_image[0:height_cropped, 0:int(width*(1-side_crop))]
    right_side = col_filtered_image[0:height_cropped, int(width*side_crop):width]

    for i in range(n_windows):
        left_points_x.append(int((n_windows-(i+1))/n_windows*height))
        right_points_x.append(int((n_windows-(i+1))/n_windows*height))
        left_points_y.append(np.argmax(np.sum(left_side[int((n_windows-(i+1))/n_windows*height_cropped):int((n_windows-i)/n_windows*height_cropped), :], axis=0)))
        right_points_y.append(np.argmax(np.sum(right_side[int((n_windows-(i+1))/n_windows*height_cropped):int((n_windows-i)/n_windows*height_cropped), :], axis=0)))
    return  np.array(left_points_x), np.array(left_points_y), np.array(right_points_x), np.array(right_points_y) + int(width*side_crop)

def draw_points(image, x, y, color=(0, 0, 255)):
    image_copy = image.copy()
    for point in zip(y, x):
        image_copy = cv2.circle(image_copy, tuple(point), 3, color)
    return image_copy

def fit_line(x, y, degree=1):
    line = np.polyfit(x, y, degree)
    angle = math.degrees(math.atan(line[0]))
    return angle, line

def distance(x1, x2, max_dist=320):
    return np.linalg.norm(x1-x2)/np.sqrt(len(x1)*max_dist**2)

def drop_outlier_points(x):
    x = np.array(x)
    m = np.mean(x)
    sd = np.std(x)
    return np.where(abs(x-m) < 3* sd, x, m).astype(int)
    
