import cv2
import numpy as np

def process_traffic_light(traffic_roi):
    hsv = cv2.cvtColor(traffic_roi, cv2.COLOR_BGR2HSV)
    
    lower_red_on = np.array([160, 50, 50], dtype=np.uint8)
    upper_red_on = np.array([180, 255, 255], dtype=np.uint8)
    lower_green_on = np.array([40, 150, 150], dtype=np.uint8)
    upper_green_on = np.array([80, 255, 255], dtype=np.uint8)

    red_mask_on = cv2.inRange(hsv, lower_red_on, upper_red_on)
    green_mask_on = cv2.inRange(hsv, lower_green_on, upper_green_on)

    if cv2.countNonZero(red_mask_on) > 500:
        return "RedON"
    elif cv2.countNonZero(green_mask_on) > 600:
        return "GreenON"
    return None
