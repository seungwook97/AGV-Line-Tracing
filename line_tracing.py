import cv2
import numpy as np

def process_line_tracing(line_roi):
    gray = cv2.cvtColor(line_roi, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            center = line_roi.shape[1] // 2
            if cx < center - 25:
                return "LEFT"
            elif cx > center + 25:
                return "RIGHT"
            else:
                return "FORWARD"
    return None
