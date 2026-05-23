import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import winsound
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading

# ── Load and encode known faces ──
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding complete.')

# ── Mark attendance ──
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dateString = now.strftime('%Y-%m-%d')
            timeString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dateString},{timeString}')
            winsound.Beep(1000, 200)
            return True
    return False

# ── GUI Setup ──
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("900x600")
root.configure(bg="#1e1e2e")

# Left: webcam feed
cam_label = tk.Label(root, bg="#1e1e2e")
cam_label.place(x=10, y=10, width=580, height=440)

# Title
title = tk.Label(root, text="Attendance System",
                 font=("Helvetica", 16, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4")
title.place(x=600, y=20)

# Status label
status_var = tk.StringVar(value="Starting camera...")
status_label = tk.Label(root, textvariable=status_var,
                        font=("Helvetica", 11),
                        bg="#1e1e2e", fg="#a6e3a1")
status_label.place(x=600, y=60)

# Count label
count_var = tk.StringVar(value="Marked today: 0")
count_label = tk.Label(root, textvariable=count_var,
                       font=("Helvetica", 11),
                       bg="#1e1e2e", fg="#89b4fa")
count_label.place(x=600, y=90)

# Attendance log table
cols = ("Name", "Date", "Time")
tree = ttk.Treeview(root, columns=cols, show="headings", height=12)
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#313244",
                foreground="#cdd6f4",
                fieldbackground="#313244",
                rowheight=25)
style.configure("Treeview.Heading",
                background="#45475a",
                foreground="#cdd6f4",
                font=("Helvetica", 10, "bold"))

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=90, anchor="center")

tree.place(x=598, y=125, width=290, height=330)

# Load existing CSV rows into table
def loadExistingAttendance():
    with open('Attendance.csv', 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 3:
                tree.insert('', 'end', values=parts)

loadExistingAttendance()

# Quit button
def quitApp():
    cap.release()
    root.destroy()

quit_btn = tk.Button(root, text="Quit", command=quitApp,
                     font=("Helvetica", 11, "bold"),
                     bg="#f38ba8", fg="white",
                     activebackground="#e06c75",
                     relief="flat", padx=20, pady=6)
quit_btn.place(x=700, y=470)

# ── Webcam loop inside GUI ──
cap = cv2.VideoCapture(0)
attendanceCount = [0]

def updateFrame():
    success, img = cap.read()
    if not success:
        root.after(10, updateFrame)
        return

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(img, name, (x1+6,y2-6),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)

            marked = markAttendance(name)
            if marked:
                attendanceCount[0] += 1
                count_var.set(f"Marked today: {attendanceCount[0]}")
                status_var.set(f"✓ {name} marked!")
                now = datetime.now()
                tree.insert('', 'end', values=(
                    name,
                    now.strftime('%Y-%m-%d'),
                    now.strftime('%H:%M:%S')
                ))
            else:
                status_var.set(f"Already marked: {name}")

    # Show frame in GUI
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize((580, 440))
    imgtk = ImageTk.PhotoImage(image=img_pil)
    cam_label.imgtk = imgtk
    cam_label.configure(image=imgtk)

    root.after(10, updateFrame)

# ── Install Pillow if needed ──
# pip install Pillow

updateFrame()
root.mainloop()