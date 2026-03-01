from email import message
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os 
import mysql.connector
import numpy as np
import cv2


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Face recognition Page")

        # Title (full width, fixed height)
        title_lbl = Label(self.root, text="Face Recognition",
                          font=("times new roman", 30, "bold"),
                          bg="white", fg="green")
        title_lbl.place(relx=0, rely=0, relwidth=1, height=50)

        header_height = int(self.screen_height * 0.9)
        header_width = int(self.screen_width / 2)
    

        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        self.photoimg01 = load_image(r"static\images\img01.jpg", header_width, header_height)
        f_lb_1 = Label(self.root, image=self.photoimg01)
        f_lb_1.place(x=0, y=46, width=header_width, height=header_height)

        self.photoimg02 = load_image(r"static\images\img02.jpg", header_width, header_height)
        f_lb_2 = Label(self.root, image=self.photoimg02)
        f_lb_2.place(x=header_width, y=46, width=header_width, height=header_height)
        
        # // button 
        b1_1 = Button(f_lb_2, text="Face Recognition",  cursor="hand2",command=self.face_recog, font=("times new roman", 18,"bold"), bg="darkgreen", fg="white")
        b1_1.place(x=header_width - 500, y=header_height - 90, width=200, height=60)

    
    def get_connection(self):
        return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Wasid@5284mysql",
        database="face_recognizer"
    )
    
    # //////////// face recognition/////////
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbours,color, text,clf):
            gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features= classifier.detectMultiScale(gray_image,scaleFactor, minNeighbours)
            coord =[]
            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y), (x+w,y+h),(0,255,0),3)
                id,predict =clf.predict(gray_image[y:y+h, x:x+w])
                confidence =int((100 * (1- predict/300)))


                conn = self.get_connection()
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT name FROM student WHERE student_id=%s", (id,))
                n = my_cursor.fetchone()
                n = n[0] if n else "Unknown" # type: ignore

                my_cursor.execute("SELECT roll FROM student WHERE student_id=%s", (id,))
                r = my_cursor.fetchone()
                r = r[0] if r else "Unknown" # type: ignore


                my_cursor.execute("SELECT dep FROM student WHERE student_id=%s", (id,))
                d = my_cursor.fetchone()
                d = d[0] if d else "Unknown" # type: ignore

                if confidence > 76:
                    cv2.putText(img, f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
                    cv2.putText(img, f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
                    cv2.putText(img, f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)

                else:
                    cv2.rectangle(img,(x,y), (x+w,y+h), (0,0,255), 3)
                    cv2.putText(img, f"UnKnown Face",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)

                coord= [x,y,w,h]
            return coord
        
        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255,25, 255),"Face", clf)
            return img        #coord use ?
        
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create() # type: ignore
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret,img = video_cap.read()
            img = recognize(img, clf,faceCascade)
            cv2.imshow("Welcome to face Recognition", img)

            if cv2.waitKey(1) == 13:
                break
        video_cap.release()
        cv2.destroyAllWindows()

        








if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition(root)
    root.mainloop()