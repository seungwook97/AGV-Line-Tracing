import cv2
import threading
import time
from pymycobot.myagv import MyAgv
from line_tracing import process_line_tracing
from traffic_light_detection import process_traffic_light

agv = MyAgv("/dev/ttyAMA2", 115200)

is_red_on = False
is_line_tracing_active = True  
line_result = None

def control_agv():
    global is_red_on, line_result, is_line_tracing_active
    while True:
        if is_red_on:
            print("AGV state: red, stop!")
            agv.stop()
        elif is_line_tracing_active and line_result:
            print(f"AGV state: line mode! - {line_result}")
            if line_result == "LEFT":
                agv.counterclockwise_rotation(1)
                time.sleep(0.1)
            elif line_result == "RIGHT":
                agv.clockwise_rotation(1)
                time.sleep(0.1)
            elif line_result == "FORWARD":
                agv.go_ahead(1)
                time.sleep(0.1)

def camera_thread():
    global is_red_on, line_result, is_line_tracing_active
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
        height, width, _ = frame.shape
        
        line_tracing_roi = frame[height // 2:, :]
        traffic_light_roi = frame[:height // 2, :]

        cv2.rectangle(frame, (0, height // 2), (width, height), (255, 0, 0), 2) 
        cv2.rectangle(frame, (0, 0), (width, height // 2), (0, 255, 0), 2)  

        traffic_light = process_traffic_light(traffic_light_roi)
        if traffic_light == "RedON":
            print("Red_Light!")
            is_red_on = True
            is_line_tracing_active = False

        elif traffic_light == "GreenON":
            print("Green_Light!")
            is_red_on = False
            is_line_tracing_active = True

        if not is_red_on and is_line_tracing_active:
            line_result = process_line_tracing(line_tracing_roi)

        cv2.imshow('AGV Camera', frame)
        if cv2.waitKey(1) == ord('q'):
            threading.Timer(0.3, agv.stop).start()  
            is_line_tracing_active = False
            agv.restore()  
            break

    cap.release()
    cv2.destroyAllWindows()

agv_thread = threading.Thread(target=control_agv)
camera_thread = threading.Thread(target=camera_thread)

agv_thread.start()
camera_thread.start()

camera_thread.join()
agv_thread.join()
