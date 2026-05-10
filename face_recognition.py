from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
import cv2
from datetime import datetime


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Page")
        self.root.state("zoomed")  # start maximised

        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        self.root.geometry(f"{sw}x{sh}+0+0")

        # Set that keeps track of who was already marked this session
        self.marked_ids = set()

        # ── Load helper ─────────────────────────────────────────────────────
        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        # ── Title bar (full width, 50 px) ────────────────────────────────────
        title_font = max(20, int(sw * 0.020))
        title_lbl = Label(
            self.root, text="Face Recognition",
            font=("times new roman", title_font, "bold"),
            bg="white", fg="green",
        )
        title_lbl.place(x=0, y=0, relwidth=1, height=50)

        # ── Two background panels (each half the screen width) ───────────────
        panel_h = sh - 50          # full height minus title bar
        panel_w = sw // 2

        self.photoimg01 = load_image(r"static\images\img01.jpg", panel_w, panel_h)
        f_lb_1 = Label(self.root, image=self.photoimg01)
        f_lb_1.place(x=0, y=50, relwidth=0.5, height=panel_h)

        self.photoimg02 = load_image(r"static\images\img02.jpg", panel_w, panel_h)
        f_lb_2 = Label(self.root, image=self.photoimg02)
        f_lb_2.place(relx=0.5, y=50, relwidth=0.5, height=panel_h)

        # ── Face Recognition button (bottom-centre of right panel) ───────────
        btn_w    = max(180, int(sw * 0.15))
        btn_h    = max(50,  int(sh * 0.07))
        btn_font = max(13,  int(sw * 0.012))

        Button(
            f_lb_2, text="Face Recognition",
            command=self.face_recog, cursor="hand2",
            font=("times new roman", btn_font, "bold"),
            bg="darkgreen", fg="white",
        ).place(
            relx=0.5, rely=0.95,
            anchor=CENTER,
            width=btn_w, height=btn_h,
        )

    # ────────────────────────────────────────────────────────────────────────
    # DB CONNECTION
    # ────────────────────────────────────────────────────────────────────────
    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD",
            database="face_recognizer",
        )

    # ────────────────────────────────────────────────────────────────────────
    # MARK ATTENDANCE
    # ────────────────────────────────────────────────────────────────────────
    def mark_attendance(self, i, r, n, d):
        """Write one attendance record to CSV; ignore duplicates this session."""
        if i in self.marked_ids:
            return
        self.marked_ids.add(i)

        with open("attendanceFile.csv", "a", newline="\n") as f:
            now     = datetime.now()
            d1      = now.strftime("%d/%m/%y")
            t_str   = now.strftime("%H:%M:%S")
            f.write(f"\n{i},{r},{n},{d},{t_str},{d1},Present")

    # ────────────────────────────────────────────────────────────────────────
    # FACE RECOGNITION LOOP
    # ────────────────────────────────────────────────────────────────────────
    def face_recog(self):

        def draw_boundary(img, classifier, scale_factor, min_neighbours, clf):
            gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces  = classifier.detectMultiScale(gray, scale_factor, min_neighbours)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

                student_id, predict = clf.predict(gray[y:y + h, x:x + w])
                confidence = int(100 * (1 - predict / 300))

                conn      = self.get_connection()
                cursor    = conn.cursor()

                def fetch_one(col):
                    cursor.execute(
                        f"SELECT {col} FROM student WHERE student_id=%s",
                        (student_id,)
                    )
                    row = cursor.fetchone()
                    return row[0] if row else "Unknown" # type: ignore

                name   = fetch_one("name")
                roll   = fetch_one("roll")
                dep    = fetch_one("dep")
                sid    = fetch_one("student_id")
                conn.close()

                if confidence > 78:
                    cv2.putText(img, f"ID:{sid}",         (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Roll:{roll}",       (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Name:{name}",       (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Department:{dep}",  (x, y - 5),  cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    self.mark_attendance(sid, roll, name, dep)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

            return img

        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf          = cv2.face.LBPHFaceRecognizer_create()  # type: ignore
        clf.read("classifier.xml")

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = draw_boundary(frame, face_cascade, 1.1, 10, clf)
            cv2.imshow("Welcome to Face Recognition", frame)
            if cv2.waitKey(1) == 13:   # Enter key
                break

        cap.release()
        cv2.destroyAllWindows()


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    Face_Recognition(root)
    root.mainloop()