# 🖱️ Virtual Mouse

A computer vision-based virtual mouse that allows users to control their computer using **hand gestures** through a webcam.

The project uses **OpenCV** and **MediaPipe** to detect and track hand movements in real time, while **PyAutoGUI** is used to control the mouse.

## ✨ Features

- Real-time hand detection using a webcam
- Hand landmark tracking using MediaPipe
- Cursor movement using hand gestures
- Mouse click control using gestures
- No physical mouse required
- Real-time computer vision processing

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- Pillow

## 📁 Project Structure

```text
virtual-mouse/
│
├── main.py
├── mouse_controller.py
├── utils.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/virtual-mouse.git
cd virtual-mouse
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Project

Start the virtual mouse with:

```bash
python main.py
```

Make sure your webcam is connected and accessible.

## 🔄 How It Works

1. The webcam captures live video.
2. OpenCV processes the video frames.
3. MediaPipe detects and tracks the hand landmarks.
4. Hand movements and gestures are interpreted as mouse actions.
5. PyAutoGUI converts these actions into actual mouse movements and clicks.

## 🚀 Future Improvements

- Add more mouse gestures
- Add scrolling using hand gestures
- Improve gesture recognition accuracy
- Add customizable gesture controls
- Add support for multiple hand gestures

## 👩‍💻 Author

**Nandini Bansal**

B.Tech CSE — Data Science