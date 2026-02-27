import secrets
from tkinter import *
from tkinter import ttk
from turtle import bgcolor
from PIL import Image, ImageTk
from matplotlib import widgets
from matplotlib.hatch import HorizontalHatch
from numpy import imag, save
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

        # //// class student info/////
        class_Student_frame = LabelFrame(
          Left_frame, bd=2, relief=RIDGE, text="Class Student Info",
          font=("times new roman", 15, "bold"),
          bg="white", fg="red"
        )
        class_Student_frame.place(x=5, y=250, width=720, height=300) 

        studentId_label = Label(
          class_Student_frame,
          text="Student ID: ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        studentId_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)    
   
        # student id 
        studentId_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        studentId_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)    



        studentName_label = Label(
          class_Student_frame,
          text="Student Name: ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        studentName_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)    
        # student id 
        studentName_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=10, sticky=W)    


        class_div_label = Label(
          class_Student_frame,
          text="Class Div: ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        class_div_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)     
        # student id 
        class_div_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        class_div_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)   



        roll_no_label = Label(
          class_Student_frame,
          text="Roll No: ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        roll_no_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)     
        # student id 
        roll_no_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=10, sticky=W) 



        gender_label = Label(
          class_Student_frame,
          text="Gender ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        gender_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)     
        # student id 
        gender_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        gender_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W) 



        dob_label = Label(
          class_Student_frame,
          text="DOB ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        dob_label.grid(row=2, column=2, padx=10, pady=10, sticky=W)     
        # student id 
        dob_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        dob_entry.grid(row=2, column=3, padx=10, pady=10, sticky=W) 




        email_label = Label(
          class_Student_frame,
          text="Email:  ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        email_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)     
        # student id 
        email_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W) 



        phone_label = Label(
          class_Student_frame,
          text="Phone: ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        phone_label.grid(row=3, column=2, padx=10, pady=10, sticky=W)     
        # student id 
        phone_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=10, sticky=W) 





        address_label = Label(
          class_Student_frame,
          text="address: ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        address_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)     
        # student id 
        address_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        address_entry.grid(row=4, column=1, padx=10, pady=10, sticky=W) 



        teacher_label = Label(
          class_Student_frame,
          text="Teacher: ",
          font=("times new roman", 12, "bold"),
          bg="white"
        )
        teacher_label.grid(row=4, column=2, padx=10, pady=10, sticky=W)     
        # student id 
        teacher_entry = ttk.Entry(class_Student_frame, width=20, font=("times new roman",13, "bold"))
        teacher_entry.grid(row=4, column=3, padx=10, pady=10, sticky=W) 


        # ///  radio button //
        radioBtn1 = ttk.Radiobutton(class_Student_frame, text="Take photo Sample", value="Yes", )
        radioBtn1.grid(row=5, column=0, )


                # ///  radio button //
        radioBtn2 = ttk.Radiobutton(class_Student_frame, text="No photo Sample", value="Yes", )
        radioBtn2.grid(row=6, column=0, )


        # ////button frame ///?
        btn_frame = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0,y=200, width=715, height=35)


        save_btn= Button(btn_frame, text="Save", width=17,  font=("times new roman",13, "bold"), bg="blue", fg="white")
        save_btn.grid(row=0, column=0, )

        update_btn= Button(btn_frame, text="Update", width=17,  font=("times new roman",13, "bold"), bg="blue", fg="white")
        update_btn.grid(row=0, column=1, )

        delete_btn= Button(btn_frame, text="Delete", width=17,  font=("times new roman",13, "bold"), bg="blue", fg="white")
        delete_btn.grid(row=0, column=2, )
        
        reset_btn= Button(btn_frame, text="Reset", width=17,  font=("times new roman",13, "bold"), bg="blue", fg="white")
        reset_btn.grid(row=0, column=3, )





        # ////button frame2 ///?
        btn_frame2 = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame2.place(x=0,y=230, width=715, height=35)

        take_photo_btn = Button(btn_frame2, text="Take Photo Sample", width=35,  font=("times new roman",13, "bold"), bg="blue", fg="white")
        take_photo_btn.grid(row=0, column=0, )

        update_photo_btn = Button(btn_frame2, text="Update Photo Sample", width=35,  font=("times new roman",13, "bold"), bg="blue", fg="white")
        update_photo_btn.grid(row=0, column=1 )


        # /////  right label frame   ////////////////
        Right_frame= LabelFrame(main_frame, bd=2, relief=RIDGE, text="Right Frame",font=("times new roman", 35, "bold"),
              bg="white", fg="red")
        Right_frame.place(x=780, y=10, width=720, height=580)
        
                # IMAGE
        img_right = Image.open(r"D:\Projects\mcaProject\static\images\img06.jpg")
        img_right = img_right.resize((720, 130), Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        f_lbl = Label(Right_frame, image=self.photoimg_right)
        f_lbl.place(x=5, y=135, width=720, height=70)


        # /////////// search feature //////////
        search_frame= LabelFrame(Right_frame, bd=2, relief=RIDGE, text="Class Student Info",font=("times new roman", 15, "bold"),
              bg="white", fg="red")
        search_frame.place(x=5, y=135, width=710, height=70)
        search_label = Label(search_frame, text="Search By: ", font=("times new roman", 13, "bold"), bg="red",fg="black" )
        search_label.grid(row=0, column=0, padx=12, pady=5, sticky=W)


        search_combo = ttk.Combobox(
           search_frame,
           font=("times new roman", 12, "bold"),
          state="readonly",
          width=13
        )
        search_combo["values"] = ("Select", "Roll_No", "Phone_No")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        search_entry = ttk.Entry(search_frame, width=15, font=("times new roman",13, "bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)




        search_btn= Button(search_frame, text="Search", width=14,  font=("times new roman",13, "bold"), bg="blue", fg="white")
        search_btn.grid(row=0, column=3, padx=10, pady=5)
        
        showAll_btn= Button(search_frame, text="Show All", width=14,  font=("times new roman",13, "bold"), bg="blue", fg="white")
        showAll_btn.grid(row=0, column=4, padx=10, pady=5)

        # ///////// table ///////
        table_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=210, width=710, height=350)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
        table_frame,
        columns=("dep","course","year","sem","id","name","div","roll","gender","dob","email","phone","address","teacher","photo"),
        xscrollcommand=scroll_x.set,
        yscrollcommand=scroll_y.set
        )

#  CONNECT scrollbars
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

#  PROPER PACKING
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.student_table.pack(fill=BOTH, expand=1)

#  HEADINGS
        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="Student ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("div", text="Division")
        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("photo", text="Photo")

        self.student_table["show"] = "headings"

#  COLUMN WIDTH (make wide to force horizontal scroll)
        for col in ("dep","course","year","sem","id","name","div","roll","gender","dob","email","phone","address","teacher","photo"):
         self.student_table.column(col, width=120)


        




        


if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()