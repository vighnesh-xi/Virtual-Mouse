# 🐭 Virtual Mouse using Hand Gestures

<img src="https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif" width="200" align="right" />

Control your computer's mouse with the **wave of a hand!**  
This project uses your **webcam** to track hand movements and translate them into cursor actions — offering a **futuristic way to interact with your screen.**

---

## 🌟 Key Features
- 🎯 **Gesture-Based Control**: Navigate your cursor by simply moving your index finger.  
  <img src="https://media.giphy.com/media/3o7btT1T9qpQZFFVza/giphy.gif" width="150" />

- 🖱️ **Clicking Action**: Perform a click by bringing your index and middle fingers together.  
  <img src="https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif" width="150" />

- ⚡ **Real-Time Performance**: Smooth and responsive cursor control with minimal latency.  
- 📷 **No Special Hardware**: Works with any standard webcam.  
  <img src="https://media.giphy.com/media/xT1R9YX5A1WAG1rnDi/giphy.gif" width="150" />

---

## 🛠️ How It Works
This application is built using **Python** and leverages powerful computer vision libraries:  

- **OpenCV**: Captures the video feed from your webcam.  
- **MediaPipe**: Detects and tracks hand landmarks in real-time.  
- **PyAutoGUI**: Controls the mouse programmatically to execute the translated gestures.  

👉 The script identifies fingertip locations:  
- The **index finger tip** guides cursor movement.  
- **Index + Middle fingers close together** → triggers a mouse click.  

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python **3.7+**  
- A connected **webcam**  

### 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/vighnesh-xi/Virtual-Mouse.git
   cd Virtual-Mouse
