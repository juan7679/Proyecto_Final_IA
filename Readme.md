# ✋ Hand Gesture Drawing — Real-Time Computer Vision App

> Draw on a virtual canvas using only your hand and a webcam. No mouse, no touch screen — just gestures.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📌 Project Overview

**Hand Gesture Drawing** is a real-time computer vision application that lets users draw on a virtual canvas using hand gestures captured through a standard webcam. The system uses **MediaPipe's Hand Landmarker** to track 21 hand keypoints per frame and translates gestures into drawing actions — no hardware beyond a camera required.

This was developed as a final academic project for an Artificial Intelligence course, focusing on human-computer interaction, real-time image processing, and gesture recognition.

---

## ✨ Features

- 🖊️ **Pinch to draw** — bring index finger and thumb together to trace lines on the canvas
- 🖐️ **Open hand to pause** — stop drawing without lifting anything, just open your hand
- ✊ **Fist to erase** — close your fist to wipe the entire canvas clean
- 🎨 **Color selector bar** — raise your index finger to the top bar to switch between 6 colors in real time
- 🪞 **Mirror mode** — natural mirrored view so movement feels intuitive
- 🔁 **Live canvas overlay** — drawing is composited on top of the live camera feed

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Core language |
| OpenCV | Camera capture, frame rendering, canvas compositing |
| MediaPipe Tasks API | Hand landmark detection (21 keypoints) |
| NumPy | Canvas matrix operations |

---

## 👤 My Contribution

This was a team project. My specific contributions were:

- **`selectorColor.py`** — Built the color selection module. Detects when the index finger enters the top color bar and switches the active drawing color in real time. Highlights the selected color with a white border.
- **`gestos.py`** — Built the gesture recognition module. Uses MediaPipe landmark coordinates to compare fingertip positions against knuckle positions, detecting open hand (pause) and closed fist (erase) gestures.
- **Pinch improvement** — Refactored the pinch detection from a fixed pixel threshold to a relative threshold based on real-time hand size, making it consistent regardless of distance from the camera.

---

## 📁 Project Structure

```
hand-gesture-drawing/
├── main.py               # Main application loop
├── selector_colores.py   # Color selection via finger position
├── gestos.py             # Gesture detection (fist, open hand)
├── hand_landmarker.task  # MediaPipe model (download separately)
├── requirements.txt      # Project dependencies
└── README.md
```

---

## ⚙️ Installation

> ⚠️ Use a virtual environment to avoid dependency conflicts.

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/hand-gesture-drawing.git
cd hand-gesture-drawing
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install mediapipe opencv-python numpy
```

**4. Download the MediaPipe model**

Download `hand_landmarker.task` and place it in the project root:
👉 https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task

**5. Run the application**
```bash
python main.py
```

---

## 🖱️ Usage

| Gesture | Action |
|---|---|
| Pinch (index + thumb) | Draw on canvas |
| Open hand | Pause drawing |
| Closed fist | Erase entire canvas |
| Index finger on top bar | Change drawing color |
| Press `c` | Clear canvas |
| Press `q` | Quit |

---

## 🎥 Demo

> 📸 *Screenshots and demo GIF coming soon.*

**Suggested setup for best results:**
- Good lighting on your hand
- Keep your hand 40–70 cm from the camera
- Plain background improves detection accuracy

---

## 🚀 Future Improvements

- [ ] Save canvas as PNG with a gesture or keypress
- [ ] Undo last stroke gesture
- [ ] Adjustable brush thickness
- [ ] Two-hand support (one hand draws, one hand controls)
- [ ] Web-based version using WebRTC + TensorFlow.js

---

## 📄 License

This project was developed for academic purposes at [Universidad de Guanajuato].