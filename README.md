🐭 Virtual Mouse using Hand Gestures
Control your computer's mouse with the wave of a hand! This project uses your webcam to track hand movements and translate them into cursor actions, offering a futuristic way to interact with your screen.

🌟 Key Features
Gesture-Based Control: Navigate your cursor by simply moving your index finger.

Clicking Action: Perform a click by bringing your index and middle fingers together.

Real-Time Performance: Experience smooth and responsive cursor control with minimal latency.

No Special Hardware: Works with any standard webcam.

🛠️ How It Works
This application is built using Python and leverages powerful computer vision libraries:

OpenCV: Captures the video feed from your webcam.

MediaPipe: Detects and tracks the landmarks of your hand in real-time from the video feed.

PyAutoGUI: Programmatically controls the mouse and keyboard to execute the translated gestures.

The script identifies the location of your fingertips. The tip of the index finger guides the cursor's movement. When the index and middle fingers are close together, the program registers a click.

🚀 Getting Started
To get this project running on your local machine, follow these simple steps.

Prerequisites
Python 3.7+

A connected webcam

Installation & Setup
Clone the repository:

Bash

git clone https://github.com/vighnesh-xi/Virtual-Mouse.git
cd Virtual-Mouse
Install the required dependencies:
It's recommended to use a virtual environment.

Bash

pip install opencv-python mediapipe pyautogui
Running the Application
Execute the main script from your terminal:

Bash

python VirtualMouse.py
A window showing your webcam feed will appear. Position your hand within the frame and start controlling the mouse!

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or open a pull request.
