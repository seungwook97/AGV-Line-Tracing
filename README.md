# Line Tracing and Traffic Light Detection for AGV

This project demonstrates the integration of two functionalities: **Line Tracing** and **Traffic Light Detection**. The AGV (Automated Guided Vehicle) follows a predefined path based on line detection, and when a traffic light is detected, it reacts accordingly to the red or green signal.

## Features
- **Line Tracing**: The AGV detects the black line on a white surface using computer vision, and adjusts its movement to stay on track.
- **Traffic Light Detection**: The AGV stops when a red light is detected and resumes line tracing when a green light is detected.
- **AGV Control**: The AGV can move forward, rotate left, or rotate right based on the line tracing and traffic light signals.

## Hardware
- **AGV**: myAGV, Raspberry Pi 4 (4GB RAM)
- **Camera**: Used for line detection and traffic light recognition.
- **Libraries**: OpenCV, PyMyCobot (for AGV control)

## Requirements
- Python 3.10
- OpenCV
- pymycobot
- NumPy
- Threading

## Setup
1. Install the required libraries:

    ```bash
    pip install pymycobot==3.5.0
    ```

2. Make sure the AGV is connected and the correct COM port is specified in the code (e.g., `/dev/ttyAMA2`).

## Code Overview
### Line Tracing
The AGV follows the black line using image processing techniques:
1. The camera feed is converted to grayscale and thresholded to detect the black line.
2. The AGV adjusts its movement (left, right, or forward) based on the detected line's position.

### Traffic Light Detection
The AGV detects red and green traffic lights using HSV color space:
- **Red Light**: The AGV stops when a red light is detected.
- **Green Light**: The AGV resumes line tracing once the green light is detected.

### Multi-threading
Two threads are used:
1. **Camera Thread**: Captures video from the camera, processes the image for line tracing and traffic light detection.
2. **Control Thread**: Controls the AGV’s movement based on the detection results.

## How It Works
- The AGV first follows the black line on the ground.
- If a red light is detected in the camera feed, the AGV stops and waits.
- Once the green light is detected, the AGV resumes its line tracing.

## Running the Code
Run the code using the following command:
```bash
python main.py
