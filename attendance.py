from email import message
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from winsound import MessageBeep
from PIL import Image, ImageTk
import mysql.connector
import cv2
from time import strftime
from datetime import datetime
import csv
from tkinter import filedialog

from numpy import delete


mydata= []

class Attendance:
    def __init__(self, root):
        self.root = root
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Attendance Page")        

        # //////////////////// variables for data sending at database /////////
        self.var_attendance_id = StringVar()
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_dep  = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_attendance_status= StringVar() 

        header_height = int(self.screen_height * 0.15)
        header_width = int(self.screen_width / 3)
    

        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        self.photoimg01 = load_image(r"static\images\img01.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg01).place(x=0, y=0, width=header_width, height=header_height)

        self.photoimg02 = load_image(r"static\images\img02.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg02).place(x=header_width, y=0, width=header_width, height=header_height)

        self.photoimg03 = load_image(r"static\images\img03.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg03).place(x=header_width*2, y=0, width=header_width, height=header_height)

        bg_height = self.screen_height - header_height
        self.photobg_image = load_image(r"static\images\img04.jpg", self.screen_width, bg_height)
        bg_img = Label(self.root, image=self.photobg_image)
        bg_img.place(x=0, y=header_height, width=self.screen_width, height=bg_height)

        Label(bg_img, text="Attendance Management System",
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

        img_left = Image.open(r"static\images\img05.jpg")
        img_left = img_left.resize((img_w, img_h), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        f_lbl = Label(Left_frame, image=self.photoimg_left)
        f_lbl.place(x=5, y=0, width=img_w, height=img_h)


        # Current Course Frame
        current_frame = LabelFrame(
            Left_frame, bd=2, relief=RIDGE, text="Current Course",
            font=("times new roman", 15, "bold"),
            bg="white", fg="red"
        )
        course_frame_h = int(left_height * 0.25)
        current_frame.place(x=5, y=img_h + 5, width=img_w, height=course_frame_h)

        dep_label = Label(current_frame, text="Department", font=("times new roman", 12, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        dep_combo = ttk.Combobox(current_frame,textvariable=self.var_dep, font=("times new roman", 12, "bold"), state="readonly", width=17)
        dep_combo["values"] = ("Select Department", "BCA", "MCA", "Cyber Security")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)



        date_label = Label(current_frame, text="Year", font=("times new roman", 12, "bold"), bg="white")
        date_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        year_combo = ttk.Combobox(current_frame,textvariable=self.var_date, font=("times new roman", 12, "bold"), state="readonly", width=17)
        year_combo["values"] = ("Select Year", "2022-23", "2023-24", "2024-25")
        year_combo.current(2)
        year_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Class Student Info Frame
        left_inside_frame = LabelFrame(
            Left_frame, bd=2, relief=RIDGE, text="Class Student Info",
            font=("times new roman", 15, "bold"),
            bg="white", fg="red"
        )
        class_frame_y = img_h + course_frame_h + 10
        class_frame_h = left_height - class_frame_y - 10
        left_inside_frame.place(x=5, y=class_frame_y, width=left_width - 10, height=class_frame_h)

# Class Student Info Frame fields - linked to StringVars
        field_data = [
    ("AttendanceId",   self.var_attendance_id,   0, 0),
    ("Roll:", self.var_roll, 0, 2),
    ("Name:",    self.var_name,      1, 0),
    ("Dept:",      self.var_dep,     1, 2),
    ("Time",       self.var_time,   2, 0),
    ("Date:",          self.var_date,      2, 2),
    ("Attendance Status:",        self.var_attendance_status,    3, 0),

]

        for (text, var, row, col) in field_data:
            Label(
              left_inside_frame,
              text=text,
              font=("times new roman", 12, "bold"),
              bg="white"
             ).grid(row=row, column=col, padx=10, pady=10, sticky=W)

    # 👇 condition for combobox
            if text == "Attendance Status:":
                combo = ttk.Combobox(
            left_inside_frame,
            textvariable=var,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=18
        )
                combo["values"] = ("Status","Present", "Absent")
                combo.current(0)
                combo.grid(row=row, column=col+1, padx=10, pady=10, sticky=W)

            
            elif text == "Dept:":
                combo = ttk.Combobox(
            left_inside_frame,
            textvariable=var,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=18
        )
                combo["values"] = ("Select course","MCA", "BCA")
                combo.current(0)
                combo.grid(row=row, column=col+1, padx=10, pady=10, sticky=W)

            else:
             ttk.Entry(
            left_inside_frame,
            textvariable=var,
            width=20,
            font=("times new roman", 13, "bold")
        ).grid(row=row, column=col+1, padx=10, pady=10, sticky=W)


        # ---- Button Frame 1 (Save/Update/Delete/Reset) ----
        # Use grid row 7 instead of place so it aligns properly inside left_inside_frame
        btn_frame = Frame(left_inside_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.grid(row=7, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        Button(btn_frame, text="Import CSV", command=self.importCSV ,font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=0, sticky="nsew")
        Button(btn_frame, text="Export CSV",command=self.exportCSV, font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=1, sticky="nsew")
        Button(btn_frame, text="Update", font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=2, sticky="nsew")
        Button(btn_frame, text="Reset" ,command=self.reset_data, font=("times new roman", 13, "bold"), bg="blue", fg="white").grid(row=0, column=3, sticky="nsew")











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
        img_right = Image.open(r"static\images\img06.jpg")
        img_right = img_right.resize((right_width - 10, 130), Image.Resampling.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)
        Label(Right_frame, image=self.photoimg_right).place(x=5, y=0, width=right_width - 10, height=130)


        # Table Frame
        table_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=180, width=right_width - 10, height=right_height - 220)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.attendanceReportTable = ttk.Treeview(
            table_frame,
            columns=("id","roll","name","department","time","date","attendance"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.config(command=self.attendanceReportTable.xview)
        scroll_y.config(command=self.attendanceReportTable.yview)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        


        self.attendanceReportTable.heading("id",text="Attendance ID")
        self.attendanceReportTable.heading("roll",text="Roll")
        self.attendanceReportTable.heading("name",text="Name")
        self.attendanceReportTable.heading("department",text="Department")
        self.attendanceReportTable.heading("time",text="Time")
        self.attendanceReportTable.heading("date",text="Date")
        self.attendanceReportTable.heading("attendance",text="Attendance")
        # //////// for removing extra empty row ////////
        self.attendanceReportTable["show"]= "headings"


        self.attendanceReportTable.column("id",width=100)

        self.attendanceReportTable.pack(fill=BOTH,expand=1)

        self.attendanceReportTable.bind("<ButtonRelease>",self.get_cursor)

    # //////////face data////////////
    def fetchData(self, rows):
        self.attendanceReportTable.delete(*self.attendanceReportTable.get_children())
        for i in rows:
            self.attendanceReportTable.insert("",END, values=i)
    
    # //////// import csv ///////

    def importCSV(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"), ("All File","*.*")),parent=self.root)
        with open(fln) as myfile:
            csvread = csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)


    # ////////// export csv ///////////
    def exportCSV(self):
        try:
            if len(mydata) < 1:
                messagebox.showerror("No Data","No Data Found!",parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(
    initialdir=os.getcwd(),
    title="Save CSV",
    defaultextension=".csv",
    filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),
    parent=self.root
)

            if fln:
                with open(fln, mode="w", newline="") as myfile:
                    exp_write = csv.writer(myfile, delimiter=",")
                    exp_write.writerows(mydata)

                    messagebox.showinfo(
        "Data Export",
        "Your Data Exported to " + os.path.basename(fln) + " successfully"
    )    

        except Exception as e:
            messagebox.showerror("Error",f"Due to :{str(e)}", parent=self.root)
    



    def get_cursor(self,event):
        cursor_row  = self.attendanceReportTable.focus()
        content = self.attendanceReportTable.item(cursor_row)
        rows = content['values']
        if rows:  
            self.var_attendance_id.set(rows[0])
            self.var_roll.set(rows[1])
            self.var_name.set(rows[2])
            self.var_dep.set(rows[3])
            self.var_time.set(rows[4])
            self.var_date.set(rows[5])
            self.var_attendance_status.set(rows[6])

    
    def reset_data(self):
        self.var_attendance_id.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_dep.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attendance_status.set("")













    






if __name__ == "__main__":
    root = Tk()
    app = Attendance(root)
    root.mainloop()