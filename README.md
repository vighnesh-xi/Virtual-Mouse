# 🐭 Virtual Mouse using Hand Gestures

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZGN6dWV2c2Z6YjUxdm5nNmt6ejh1NnZzMm44ajlzdGVjcHFycnQ5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/26tn33aiTi1jkl6H6/giphy.gif" width="200" align="right" />

Control your computer's mouse with the **wave of a hand!**  
This project uses your **webcam** to track hand movements and translate them into cursor actions — offering a **futuristic way to interact with your screen.**

---

## 🌟 Key Features
- 🎯 **Gesture-Based Control**: Navigate your cursor by simply moving your index finger.  
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZGdtZDJ6dm5yYXltbHppZmp4YTZudW90d3RqNmM3M2FkaThpZW5hcCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0ExncehJzexFpRHq/giphy.gif" width="120" />

- 🖱️ **Clicking Action**: Perform a click by bringing your index and middle fingers together.  
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHM3YThidXV2ZTZlNW02bm5rY21hYnh6NWFoa3JicjBjcjl6cGd3NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5VKbvrjxpVJCM/giphy.gif" width="120" />

- ⚡ **Real-Time Performance**: Smooth and responsive cursor control with minimal latency.  
- 📷 **No Special Hardware**: Works with any standard webcam.  
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGdrbGtjdmtjZzlqY2pnNnZ2eDdtam8zYjRoZ2F2cHNzdHRkYzZpOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oriO0OEd9QIDdllqo/giphy.gif" width="120" />

---

## 🛠️ How It Works  

This project is powered by **Python** and uses cutting-edge computer vision libraries:  

- 🟦 **OpenCV** → Captures the video feed from your webcam  
- ✋ **MediaPipe** → Detects and tracks hand landmarks in real-time  
- 🖥️ **PyAutoGUI** → Translates recognized gestures into mouse actions  

### 🧩 Gesture Logic  
👉 The script identifies fingertip locations to control the cursor:  
- 🖐️ **Index finger tip** → Guides cursor movement  
- ✌️ **Index + Middle fingers close together** → Triggers a mouse click  

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
