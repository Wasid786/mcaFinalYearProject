import cmath
from time import strftime
from tkinter import *
import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
from weekly_progress import Weekly_Progress
from student import Student
import os
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from help_desk import Help_Desk


class Face_recognition_System:
    def __init__(self, root):
        self.root   = root
        self.images = []  # keep references so images aren't garbage-collected

        self.root.title("Face Recognition System")
        self.root.state("zoomed")  # start maximised

        # Read screen dimensions AFTER the window is displayed
        self.root.update_idletasks()
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()

        # ── Load helper ─────────────────────────────────────────────────────
        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        # ── Header images (top strip, 15 % of screen height, split in 3) ───
        hdr_h = int(self.sh * 0.15)
        hdr_w = self.sw // 3

        self.photoimg01 = load_image(r"static\images\img01.jpg", hdr_w, hdr_h)
        Label(self.root, image=self.photoimg01).place(
            x=0, y=0, relwidth=1/3, height=hdr_h
        )

        self.photoimg02 = load_image(r"static\images\img02.jpg", hdr_w, hdr_h)
        Label(self.root, image=self.photoimg02).place(
            relx=1/3, y=0, relwidth=1/3, height=hdr_h
        )

        self.photoimg03 = load_image(r"static\images\img03.jpg", hdr_w, hdr_h)
        Label(self.root, image=self.photoimg03).place(
            relx=2/3, y=0, relwidth=1/3, height=hdr_h
        )

        # ── Background image (everything below the header) ──────────────────
        bg_h = self.sh - hdr_h
        self.photobg_image = load_image(r"static\images\main02.jpg", self.sw, bg_h)
        bg_img = Label(self.root, image=self.photobg_image)
        bg_img.place(x=0, y=hdr_h, relwidth=1, height=bg_h)

        # ── Title bar ───────────────────────────────────────────────────────
        title_font_size = max(14, int(self.sw * 0.018))
        title_lbl = Label(
            bg_img, text="Lab Attendance System",
            font=("times new roman", title_font_size, "bold"),
            bg="white", fg="red",
        )
        title_lbl.place(x=0, y=0, relwidth=1, height=50)

        # Clock (top-left of title bar)
        def tick():
            lbl_clock.config(text=strftime("%H:%M:%S %p"))
            lbl_clock.after(1000, tick)

        lbl_clock = Label(
            title_lbl, font=("times new roman", 14, "bold"),
            bg="white", fg="blue",
        )
        lbl_clock.place(x=0, y=0, width=110, height=50)
        tick()

        # ── Button grid ─────────────────────────────────────────────────────
        # Buttons are 12 % of screen width and 18 % of screen height each.
        # The 4 columns are evenly spaced, starting at 10 % from the left.
        btn_w = int(self.sw * 0.12)
        btn_h = int(self.sh * 0.18)

        # Horizontal positions: evenly spread across screen
        x_positions = [
            int(self.sw * 0.10),
            int(self.sw * 0.30),
            int(self.sw * 0.50),
            int(self.sw * 0.70),
        ]

        # Row 1 starts just below the title bar; row 2 is below row 1
        y_top    = int(self.sh * 0.08)   # relative to bg_img (after title bar)
        y_bottom = int(self.sh * 0.45)

        def create_button(img_path, text, x, y, command=lambda: None):
            img = load_image(img_path, btn_w, btn_h)
            self.images.append(img)  # prevent garbage collection

            btn_img = Button(
                bg_img, image=img, cursor="hand2", command=command,
                relief=FLAT, bd=0,
            )
            btn_img.place(x=x, y=y, width=btn_w, height=btn_h)

            btn_lbl = Button(
                bg_img, text=text, cursor="hand2", command=command,
                font=("times new roman", max(11, int(self.sw * 0.010)), "bold"),
                bg="darkblue", fg="white",
            )
            btn_lbl.place(x=x, y=y + btn_h, width=btn_w, height=40)

        # Row 1
        create_button(r"static\images\main_student.jpg", "Student Details", x_positions[0], y_top,    command=self.student_details)
        create_button(r"static\images\main_face.jpg", "Face Detection",  x_positions[1], y_top,    command=self.face_data)
        create_button(r"static\images\main_attendance.jpg", "Attendance",      x_positions[2], y_top,    command=self.attendance_data)
        create_button(r"static\images\main_help.jpg", "Help Desk",       x_positions[3], y_top, command=self.help_desk_window)

        # Row 2
        create_button(r"static\images\main_train.jpg", "Train Data",       x_positions[0], y_bottom, command=self.train_data)
        create_button(r"static\images\main_photo.jpg", "Photos",           x_positions[1], y_bottom, command=self.open_img)
        create_button(r"static\images\main_weekly.jpg", "Weekly Progress",  x_positions[2], y_bottom, command=self.weekly_progress)
        create_button(r"static\images\main_exit.jpg", "Exit",             x_positions[3], y_bottom, command=self.exit_func)

    # ────────────────────────────────────────────────────────────────────────
    # ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    def open_img(self):
        os.startfile("data")

    def student_details(self):
        self.new_window = Toplevel(self.root)
        Student(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        Train(self.new_window)

    def face_data(self):
        self.new_window = Toplevel(self.root)
        Face_Recognition(self.new_window)

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        Attendance(self.new_window)

    def weekly_progress(self):
        self.new_window = Toplevel(self.root)
        Weekly_Progress(self.new_window)

    def help_desk_window(self):
        self.new_window = Toplevel(self.root)
        Help_Desk(self.new_window)

    def exit_func(self):
        if messagebox.askyesno("Face Recognition", "Exit the application?"):
            self.root.destroy()


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    Face_recognition_System(root)
    root.mainloop()