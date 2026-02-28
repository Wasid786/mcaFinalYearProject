from multiprocessing import parent_process
import secrets
from tkinter import *
from tkinter import ttk
from tokenize import String
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from numpy import delete

class Student:
    def __init__(self, root):
        self.root = root
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Student Info Page")


        # //////////////////// variables for data sending at database /////////
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester  = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div= StringVar() 
        self.var_roll= StringVar()
        self.var_gender= StringVar()
        self.var_dob  = StringVar()
        self.var_email = StringVar()
        self.var_phone  = StringVar()
        self.var_address   = StringVar()
        self.var_teacher    = StringVar()


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
        dep_combo = ttk.Combobox(current_course_frame,textvariable=self.var_dep, font=("times new roman", 12, "bold"), state="readonly", width=17)
        dep_combo["values"] = ("Select Department", "BCA", "MCA", "Cyber Security")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        course_label = Label(current_course_frame, text="Course", font=("times new roman", 12, "bold"), bg="white")
        course_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        course_combo = ttk.Combobox(current_course_frame,textvariable=self.var_course, font=("times new roman", 12, "bold"), state="readonly", width=17)
        course_combo["values"] = ("Select Course", "FY", "SY", "TY")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        date_label = Label(current_course_frame, text="Year", font=("times new roman", 12, "bold"), bg="white")
        date_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        year_combo = ttk.Combobox(current_course_frame,textvariable=self.var_year, font=("times new roman", 12, "bold"), state="readonly", width=17)
        year_combo["values"] = ("Select Year", "2022-23", "2023-24", "2024-25")
        year_combo.current(2)
        year_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        sem_label = Label(current_course_frame, text="Semester", font=("times new roman", 12, "bold"), bg="white")
        sem_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        sem_combo = ttk.Combobox(current_course_frame,textvariable=self.var_semester, font=("times new roman", 12, "bold"), state="readonly", width=17)
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

# Class Student Info Frame fields - linked to StringVars
        field_data = [
    ("Student ID:",   self.var_std_id,   0, 0),
    ("Student Name:", self.var_std_name, 0, 2),
    ("Class Div:",    self.var_div,      1, 0),
    ("Roll No:",      self.var_roll,     1, 2),
    ("Gender:",       self.var_gender,   2, 0),
    ("DOB:",          self.var_dob,      2, 2),
    ("Email:",        self.var_email,    3, 0),
    ("Phone:",        self.var_phone,    3, 2),
    ("Address:",      self.var_address,  4, 0),
    ("Teacher:",      self.var_teacher,  4, 2),
]

        for (text, var, row, col) in field_data:
            Label(
              class_Student_frame,
              text=text,
              font=("times new roman", 12, "bold"),
              bg="white"
             ).grid(row=row, column=col, padx=10, pady=10, sticky=W)

    # 👇 condition for combobox
            if text == "Gender:":
                combo = ttk.Combobox(
            class_Student_frame,
            textvariable=var,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=18
        )
                combo["values"] = ("Male", "Female", "Other")
                combo.current(0)
                combo.grid(row=row, column=col+1, padx=10, pady=10, sticky=W)


            elif text == "Class Div:":
                combo = ttk.Combobox(
            class_Student_frame,
            textvariable=var,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=18
        )
                combo["values"] = ("A", "B", "C")
                combo.current(0)
                combo.grid(row=row, column=col+1, padx=10, pady=10, sticky=W)

            else:
             ttk.Entry(
            class_Student_frame,
            textvariable=var,
            width=20,
            font=("times new roman", 13, "bold")
        ).grid(row=row, column=col+1, padx=10, pady=10, sticky=W)

    
        # ////// radio button ////
        self.var_radio1 = StringVar()
        radioBtn1 = ttk.Radiobutton(class_Student_frame,variable=self.var_radio1, text="Take photo Sample", value="Yes")
        radioBtn1.grid(row=5, column=0)
        

        radioBtn2 = ttk.Radiobutton(class_Student_frame,variable=self.var_radio1, text="No photo Sample", value="No")
        radioBtn2.grid(row=6, column=0)

        # ---- Button Frame 1 (Save/Update/Delete/Reset) ----
        # Use grid row 7 instead of place so it aligns properly inside class_Student_frame
        btn_frame = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.grid(row=7, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        Button(btn_frame, text="Save",command=self.add_data,   font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=0, sticky="nsew")
        Button(btn_frame, text="Update",command=self.update_data, font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=1, sticky="nsew")
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
        self.fetch_data()
        self.student_table.bind("<ButtonRelease>", self.get_cursor)


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


    # ////////////////////   func for data adding /////////////////

    def add_data(self):
        try:
            if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":   
             messagebox.showerror("Error", "All Fields are required!", parent=self.root)
            else:
                conn = mysql.connector.connect( 
                host="localhost",
                user="root",
                password="Wasid@5284mysql",
                database="face_recognizer"
            )
                my_cursor = conn.cursor()
                my_cursor.execute(
                "insert into student values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    int(self.var_std_id.get()),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get()
                )
            )
    
                conn.commit()
                conn.close()
    
                messagebox.showinfo("Success", "Student details has been added Successfully", parent=self.root)
    
        except Exception as es:
         messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)


    # ///////////////// fetch data //////////

    def fetch_data(self):
        try:
                conn = mysql.connector.connect( 
                host="localhost",
                user="root",
                password="Wasid@5284mysql",
                database="face_recognizer"
            )
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                data = my_cursor.fetchall()

                if len(data) !=0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in data:
                        self.student_table.insert("",END,values=tuple(i))

                
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

        finally:
            if conn:
                conn.close()

    
    # ////////////// get cursor ////////
    def get_cursor(self, event):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data =content["values"]

        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_semester.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_div.set(data[6]) 
        self.var_roll.set(data[7])
        self.var_gender.set(data[8])
        self.var_dob.set(data[9])
        self.var_email.set(data[10])
        self.var_phone.set(data[11])
        self.var_address.set(data[12])
        self.var_teacher.set(data[13])
        self.var_radio1.set(data[14])

        # //// update func //////
    def update_data(self):
        try:
            if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":   
             messagebox.showerror("Error", "All Fields are required!", parent=self.root)
            else:
                Update= messagebox.askyesno("Update", "Do you Want to update this student details: ", parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect( 
                host="localhost",
                user="root",
                password="Wasid@5284mysql",
                database="face_recognizer"
            )
                    my_cursor = conn.cursor()
                    my_cursor.execute(
                "update student set dep=%s,course=%s,year=%s,semester=%s,name=%s,division=%s,roll=%s,gender=%s,dob=%s,email=%s,phone=%s,address=%s,teacher=%s,photo_sample = %s where student_id=%s",
                (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get(),
                    int(self.var_std_id.get())

                ) )
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success","Student data update successfully!",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
                    
        except Exception as es:
         messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)
        finally:
            if conn:
                conn.close()







           


        # for var in [self.var_std_id, self.var_std_name, self.var_div,
        #         self.var_roll, self.var_gender, self.var_dob,
        #         self.var_email, self.var_phone, self.var_address, self.var_teacher]:
        #  var.set("")



if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()