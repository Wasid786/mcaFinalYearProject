import secrets
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class Student:
    def __init__(self, root):
        self.root = root

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Student Info Page")

        header_height = int(self.screen_height * 0.15)
        header_width = int(self.screen_width / 3)

        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        self.photoimg01 = load_image(r"D:\Projects\mcaProject\static\images\img01.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg01).place(x=0, y=0, width=header_width, height=header_height)

        self.photoimg02 = load_image(r"D:\Projects\mcaProject\static\images\img02.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg02).place(x=header_width, y=0, width=header_width, height=header_height)

        self.photoimg03 = load_image(r"D:\Projects\mcaProject\static\images\img03.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg03).place(x=header_width*2, y=0, width=header_width, height=header_height)

        bg_height = self.screen_height - header_height
        self.photobg_image = load_image(r"D:\Projects\mcaProject\static\images\img04.jpg", self.screen_width, bg_height)
        bg_img = Label(self.root, image=self.photobg_image)
        bg_img.place(x=0, y=header_height, width=self.screen_width, height=bg_height)

        Label(bg_img, text="Student Management System",
              font=("times new roman", int(self.screen_width * 0.02), "bold"),
              bg="white", fg="blue").place(x=0, y=0, width=self.screen_width, height=50)

        margin_x = int(self.screen_width * 0.01)
        margin_y = int(self.screen_height * 0.02)

        main_width = self.screen_width - (2 * margin_x)
        main_height = bg_height - (2 * margin_y) - 50

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(
            x=margin_x,
            y=50 + margin_y,
            width=main_width,
            height=main_height
        )

        # ===== LEFT FRAME: exactly 50% of main_width =====
        gap = 10
        left_width = int(main_width * 0.5) - gap
        left_height = int(main_height * 0.95)

        Left_frame = LabelFrame(
            main_frame, bd=2, relief=RIDGE, text="Left Frame",
            font=("times new roman", 20, "bold"),
            bg="white", fg="red"
        )
        Left_frame.place(x=gap, y=gap, width=left_width, height=left_height)

        # Image inside left frame
        img_w = left_width - 10
        img_h = int(left_height * 0.18)

        img_left = Image.open(r"D:\Projects\mcaProject\static\images\img05.jpg")
        img_left = img_left.resize((img_w, img_h), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        f_lbl = Label(Left_frame, image=self.photoimg_left)
        f_lbl.place(x=5, y=0, width=img_w, height=img_h)

        # Current Course Frame
        current_course_frame = LabelFrame(
            Left_frame, bd=2, relief=RIDGE, text="Current Course",
            font=("times new roman", 15, "bold"),
            bg="white", fg="red"
        )
        course_frame_h = int(left_height * 0.25)
        current_course_frame.place(x=5, y=img_h + 5, width=img_w, height=course_frame_h)

        dep_label = Label(current_course_frame, text="Department", font=("times new roman", 12, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        dep_combo = ttk.Combobox(current_course_frame, font=("times new roman", 12, "bold"), state="readonly", width=17)
        dep_combo["values"] = ("Select Department", "BCA", "MCA", "Cyber Security")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        course_label = Label(current_course_frame, text="Course", font=("times new roman", 12, "bold"), bg="white")
        course_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        course_combo = ttk.Combobox(current_course_frame, font=("times new roman", 12, "bold"), state="readonly", width=17)
        course_combo["values"] = ("Select Course", "FY", "SY", "TY")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        date_label = Label(current_course_frame, text="Year", font=("times new roman", 12, "bold"), bg="white")
        date_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        year_combo = ttk.Combobox(current_course_frame, font=("times new roman", 12, "bold"), state="readonly", width=17)
        year_combo["values"] = ("Select Year", "2022-23", "2023-24", "2024-25")
        year_combo.current(2)
        year_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        sem_label = Label(current_course_frame, text="Semester", font=("times new roman", 12, "bold"), bg="white")
        sem_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        sem_combo = ttk.Combobox(current_course_frame, font=("times new roman", 12, "bold"), state="readonly", width=17)
        sem_combo["values"] = ("Select Semester", "Sem 1", "Sem 2", "Sem 3", "Sem 4")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # Class Student Info Frame
        class_Student_frame = LabelFrame(
            Left_frame, bd=2, relief=RIDGE, text="Class Student Info",
            font=("times new roman", 15, "bold"),
            bg="white", fg="red"
        )
        class_frame_y = img_h + course_frame_h + 10
        class_frame_h = left_height - class_frame_y - 10
        class_Student_frame.place(x=5, y=class_frame_y, width=left_width - 10, height=class_frame_h)

        fields = [
            ("Student ID:", 0, 0), ("Student Name:", 0, 2),
            ("Class Div:", 1, 0),  ("Roll No:", 1, 2),
            ("Gender:", 2, 0),     ("DOB:", 2, 2),
            ("Email:", 3, 0),      ("Phone:", 3, 2),
            ("Address:", 4, 0),    ("Teacher:", 4, 2),
        ]
        entries = {}
        for (text, row, col) in fields:
            Label(class_Student_frame, text=text, font=("times new roman", 12, "bold"), bg="white").grid(
                row=row, column=col, padx=10, pady=10, sticky=W)
            e = ttk.Entry(class_Student_frame, width=20, font=("times new roman", 13, "bold"))
            e.grid(row=row, column=col + 1, padx=10, pady=10, sticky=W)
            entries[text] = e

        radioBtn1 = ttk.Radiobutton(class_Student_frame, text="Take photo Sample", value="Yes")
        radioBtn1.grid(row=5, column=0)
        radioBtn2 = ttk.Radiobutton(class_Student_frame, text="No photo Sample", value="No")
        radioBtn2.grid(row=6, column=0)

        # ---- Button Frame 1 (Save/Update/Delete/Reset) ----
        # Use grid row 7 instead of place so it aligns properly inside class_Student_frame
        btn_frame = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.grid(row=7, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        Button(btn_frame, text="Save",   font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=0, sticky="nsew")
        Button(btn_frame, text="Update", font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=1, sticky="nsew")
        Button(btn_frame, text="Delete", font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=2, sticky="nsew")
        Button(btn_frame, text="Reset",  font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=3, sticky="nsew")

        # ---- Button Frame 2 (Photo buttons) ----
        btn_frame2 = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame2.grid(row=8, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        for i in range(2):
            btn_frame2.columnconfigure(i, weight=1)

        Button(btn_frame2, text="Take Photo Sample",   font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=0, sticky="nsew")
        Button(btn_frame2, text="Update Photo Sample", font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=1, sticky="nsew")

        # ===== RIGHT FRAME: starts at 50% and takes remaining half =====
        right_x = left_width + (gap * 2)
        right_width = main_width - right_x - gap
        right_height = left_height

        Right_frame = LabelFrame(
            main_frame, bd=2, relief=RIDGE, text="Right Frame",
            font=("times new roman", 20, "bold"),
            bg="white", fg="red"
        )
        Right_frame.place(x=right_x, y=gap, width=right_width, height=right_height)

        # Image inside right frame
        img_right = Image.open(r"D:\Projects\mcaProject\static\images\img06.jpg")
        img_right = img_right.resize((right_width - 10, 130), Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)
        Label(Right_frame, image=self.photoimg_right).place(x=5, y=0, width=right_width - 10, height=130)

        # Search Frame (placed below image)
        search_frame = LabelFrame(
            Right_frame, bd=2, relief=RIDGE, text="Search Student",
            font=("times new roman", 15, "bold"),
            bg="white", fg="red"
        )
        search_frame.place(x=5, y=135, width=right_width - 10, height=70)

        Label(search_frame, text="Search By:", font=("times new roman", 13, "bold"), bg="red", fg="black").grid(row=0, column=0, padx=12, pady=5, sticky=W)

        search_combo = ttk.Combobox(search_frame, font=("times new roman", 12, "bold"), state="readonly", width=13)
        search_combo["values"] = ("Select", "Roll_No", "Phone_No")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        search_entry = ttk.Entry(search_frame, width=15, font=("times new roman", 13, "bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        Button(search_frame, text="Search",   width=14, font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=3, padx=10, pady=5)
        Button(search_frame, text="Show All", width=14, font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=4, padx=10, pady=5)

        # Table Frame
        table_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=210, width=right_width - 10, height=right_height - 220)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("dep", "course", "year", "sem", "id", "name", "div", "roll",
                     "gender", "dob", "email", "phone", "address", "teacher", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.student_table.pack(fill=BOTH, expand=1)

        headings = {
            "dep": "Department", "course": "Course", "year": "Year", "sem": "Semester",
            "id": "Student ID", "name": "Name", "div": "Division", "roll": "Roll No",
            "gender": "Gender", "dob": "DOB", "email": "Email", "phone": "Phone",
            "address": "Address", "teacher": "Teacher", "photo": "Photo"
        }
        for col_id, heading in headings.items():
            self.student_table.heading(col_id, text=heading)
            self.student_table.column(col_id, width=120)

        self.student_table["show"] = "headings"


if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()