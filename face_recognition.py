from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np
from time import strftime
from datetime import datetime

class Face_Recognition:
    def _init_(self, root):
        self.root = root
        self.root.geometry("1500x790+0+0")  
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="FACE RECOGNITION ", font=("times new roman", 35, "bold"), bg="white", fg="green")
        title_lbl.place(x=0, y=0, width=1505, height=45)

        # First image
        img_top = Image.open(r"C:\face_recognition\pic\airkd.png")
        img_top = img_top.resize((650, 700), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=650, height=700)

        # Second image
        img_bottom = Image.open(r"C:\face_recognition\pic\Facial-Recognition.jpg")
        img_bottom = img_bottom.resize((950, 700), Image.Resampling.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=650, y=55, width=950, height=700)

        # Button
        bt_1 = Button(f_lbl, text="FACE RECOGNITION", command=self.face_recog, cursor="hand2", font=("times new roman", 18, "bold"), bg="darkgreen", fg="white")
        bt_1.place(x=250, y=600, width=420, height=50)





    
      

        





    # Face recognition
from tkinter import *
import cv2
import mysql.connector
import os

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry("800x500")

        # Button to start face recognition
        btn = Button(self.root, text="Start Face Recognition", command=self.face_recog, font=("Arial", 18), bg="green", fg="white")
        btn.pack(pady=20)

    def face_recog(self):
        print("Face recognition started!")  # Debug statement

        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Dipan#1234",
                        database="face_recognizer",
                        auth_plugin="mysql_native_password"
                    )
                    my_cursor = conn.cursor()

                    # Retrieve user details
                    my_cursor.execute("SELECT Name FROM student WHERE Student_id = %s", (id,))
                    n = my_cursor.fetchone()
                    n = n[0] if n else "Unknown"

                    my_cursor.execute("SELECT Roll FROM student WHERE Student_id = %s", (id,))
                    r = my_cursor.fetchone()
                    r = r[0] if r else "Unknown"

                    my_cursor.execute("SELECT Dep FROM student WHERE Student_id = %s", (id,))
                    d = my_cursor.fetchone()
                    d = d[0] if d else "Unknown"

                except Exception as e:
                    print(f"Database error: {e}")
                    n, r, d = "Error", "Error", "Error"

                finally:
                    if conn.is_connected():
                        my_cursor.close()
                        conn.close()

                if confidence > 77:
                    
                    cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

                coord = [x, y, w, h]
            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        if faceCascade.empty():
            print("Error loading Haar cascade file!")
            return

        clf = cv2.face.LBPHFaceRecognizer_create()
        try:
            clf.read("classifier.xml")
        except Exception as e:
            print(f"Error loading classifier: {e}")
            return

        video_cap = cv2.VideoCapture(0)
        if not video_cap.isOpened():
            print("Error: Could not access the webcam!")
            return

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Failed to grab frame!")
                break

            img = recognize(img, clf, faceCascade)
            cv2.imshow("Welcome to Face Recognition", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                break

        video_cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
