import secrets
from tkinter import *
from tkinter import ttk
from turtle import bgcolor
from PIL import Image, ImageTk
from numpy import imag
from pyparsing import col

class Student:
    def __init__(self, root):
        self.root = root

        # Get screen size dynamically
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Student Info Page")

        # Header image size (divide screen into 3 parts)
        header_height = int(self.screen_height * 0.15)
        header_width = int(self.screen_width / 3)

        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        # Top 3 images
        self.photoimg01 = load_image(r"D:\Projects\mcaProject\static\images\img01.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg01).place(x=0, y=0, width=header_width, height=header_height)

        self.photoimg02 = load_image(r"D:\Projects\mcaProject\static\images\img02.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg02).place(x=header_width, y=0, width=header_width, height=header_height)

        self.photoimg03 = load_image(r"D:\Projects\mcaProject\static\images\img03.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg03).place(x=header_width*2, y=0, width=header_width, height=header_height)

        # Background image
        bg_height = self.screen_height - header_height
        self.photobg_image = load_image(r"D:\Projects\mcaProject\static\images\img04.jpg", self.screen_width, bg_height)
        bg_img = Label(self.root, image=self.photobg_image)
        bg_img.place(x=0, y=header_height, width=self.screen_width, height=bg_height)

        # Title
        Label(bg_img, text="Student Management System",
              font=("times new roman", int(self.screen_width*0.02), "bold"),
              bg="white", fg="blue").place(x=0, y=0, width=self.screen_width, height=50)


        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=20, y=50, width=1480, height=600 )

        # /////  left label frame   ////////////////

        
        # LEFT FRAME
        Left_frame = LabelFrame(
           main_frame, bd=2, relief=RIDGE, text="Left Frame",
           font=("times new roman", 20, "bold"),
           bg="white", fg="red"
            )
        Left_frame.place(x=10, y=10, width=760, height=580)
        
        # IMAGE
        img_left = Image.open(r"D:\Projects\mcaProject\static\images\img05.jpg")
        img_left = img_left.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl = Label(Left_frame, image=self.photoimg_left)
        f_lbl.place(x=5, y=0, width=720, height=130)

        # current course frame
        current_course_frame = LabelFrame(
          Left_frame, bd=2, relief=RIDGE, text="Current Course",
          font=("times new roman", 15, "bold"),
          bg="white", fg="red"
        )
        current_course_frame.place(x=5, y=135, width=720, height=150)

        # ///  Department ////
        dep_label = Label(
          current_course_frame,
          text="Department",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        dep_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        dep_combo = ttk.Combobox(
           current_course_frame,
           font=("times new roman", 12, "bold"),
          state="readonly",
          width=17
        )
        dep_combo["values"] = ("Select Department", "BCA", "MCA", "Cyber Security")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)


                # ///  Course  ////
        course_label = Label(
          current_course_frame,
          text="Course",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        course_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        course_combo = ttk.Combobox(
            current_course_frame,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=17
        )
        course_combo["values"] = ("Select Course", "FY", "SY", "TY")
        course_combo.current(0)  # default placeholder
        course_combo.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        
                        # ///  year  ////
        date_label = Label(
          current_course_frame,
          text="Year",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        date_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        year_combo = ttk.Combobox(
            current_course_frame,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=17
        )
        year_combo["values"] = ("Select Year", "2022-23", "2023-24", "2024-25")
        year_combo.current(2)  
        year_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

                # ///  Semester  ////
        sem_label = Label(
          current_course_frame,
          text="Semester",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        sem_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)        
        sem_combo = ttk.Combobox(
            current_course_frame,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=17
        )
        sem_combo["values"] = ("Select Semester", "Sem 1", "Sem 2", "Sem 3", "Sem 4")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=10, pady=10, sticky=W)
        
        














        # /////  right label frame   ////////////////
        Right_frame= LabelFrame(main_frame, bd=2, relief=RIDGE, text="Right Frame",font=("times new roman", 35, "bold"),
              bg="white", fg="red").place(x=780, y=10, width=690, height=580)

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()