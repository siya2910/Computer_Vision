# 🎯 Face Recognition Attendance System

A real-time attendance marking system built with Python, OpenCV, and face_recognition. The system detects and recognizes faces via webcam, automatically logs attendance with date and time into a CSV file, and displays a live GUI dashboard built with Tkinter.

---

## 📸 Features

- Real-time face detection and recognition using webcam
- Automatic attendance logging with **Name**, **Date**, and **Time**
- Live Tkinter GUI with webcam feed and attendance table
- Beep sound when attendance is successfully marked
- Prevents duplicate entries for the same person on the same day
- Attendance count displayed live on screen

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.8 | Core language |
| OpenCV | Webcam capture and image processing |
| face_recognition | Face encoding and matching (built on dlib) |
| dlib | Deep learning face detection model |
| NumPy | Numerical operations |
| Tkinter | GUI interface |
| Pillow | Image rendering inside Tkinter |

---

## 📁 Project Structure

```
FaceAttendance/
├── ImagesAttendance/       ← Add known face photos here
│   ├── Rahul_Sharma.jpg
│   └── Priya_Singh.jpg
├── attendance.py           ← Main script
├── Attendance.csv          ← Auto-updated attendance log
├── requirements.txt        ← Python dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FaceAttendance.git
cd FaceAttendance
```

### 2. Create and activate conda environment

```bash
conda create -n face_attendance python=3.8
conda activate face_attendance
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note for Windows users:** If `dlib` fails to install, run:
> ```bash
> conda install -c conda-forge dlib
> ```
> Then install the rest with pip.

### 4. Add face photos

Place one clear, front-facing photo of each person inside the `ImagesAttendance/` folder. The filename (without extension) will be used as the person's name.

```
ImagesAttendance/
├── John_Doe.jpg
└── Jane_Smith.png
```

### 5. Create Attendance.csv

Create an empty file named `Attendance.csv` in the project root with this header:

```
Name,Date,Time
```

---

## ▶️ Running the Project

```bash
conda activate face_attendance
python attendance.py
```

The GUI window will open showing:
- Live webcam feed with face bounding boxes and names
- Attendance log table on the right
- Live count of people marked today
- Status messages for each recognition event

Press the **Quit** button to stop the application.

---

## 📋 How It Works

1. On startup, all images from `ImagesAttendance/` are loaded and encoded using dlib's pre-trained face recognition model
2. Each webcam frame is resized to 25% for faster processing
3. Detected faces are compared against the known encodings
4. On a match, the person's name, current date, and time are written to `Attendance.csv`
5. Each person is only marked once per session to avoid duplicates


## 👤 Author

Siya Mandal
- GitHub: [@siya2910](https://github.com/siya2910)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
