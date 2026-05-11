import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime
import csv

mydata      = []
marked_today = set()


class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Page")
        self.root.state("zoomed")

        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{sw}x{sh}+0+0")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # ── StringVars ───────────────────────────────────────────────────────
        self.var_attendance_id     = StringVar()
        self.var_roll              = StringVar()
        self.var_name              = StringVar()
        self.var_dep               = StringVar()
        self.var_time              = StringVar()
        self.var_date              = StringVar()
        self.var_attendance_status = StringVar()

        # ── Load helper ──────────────────────────────────────────────────────
        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        # ── Header (3 images, 15 % of screen height) ─────────────────────────
        hdr_h = int(sh * 0.15)
        hdr_w = sw // 3

        self.photoimg01 = load_image(r"static\images\img01.jpg", hdr_w, hdr_h)
        Label(self.root, image=self.photoimg01).place(x=0,        y=0, relwidth=1/3, height=hdr_h)

        self.photoimg02 = load_image(r"static\images\img02.jpg", hdr_w, hdr_h)
        Label(self.root, image=self.photoimg02).place(relx=1/3,   y=0, relwidth=1/3, height=hdr_h)

        self.photoimg03 = load_image(r"static\images\img03.jpg", hdr_w, hdr_h)
        Label(self.root, image=self.photoimg03).place(relx=2/3,   y=0, relwidth=1/3, height=hdr_h)

        # ── Background below header ──────────────────────────────────────────
        bg_h = sh - hdr_h
        self.photobg = load_image(r"static\images\attendance_left.jpg", sw, bg_h)
        bg_img = Label(self.root, image=self.photobg)
        bg_img.place(x=0, y=hdr_h, relwidth=1, height=bg_h)

        # ── Page title bar ───────────────────────────────────────────────────
        title_size = max(14, int(sw * 0.018))
        Label(
            bg_img, text="Attendance Management System",
            font=("times new roman", title_size, "bold"),
            bg="white", fg="blue",
        ).place(x=0, y=0, relwidth=1, height=50)

        # ── Main frame (fills the rest) ──────────────────────────────────────
        # 2 % margin on all sides, below the 50 px title
        mx = int(sw * 0.01)
        my = int(sh * 0.01)
        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(
            x=mx, y=50 + my,
            relwidth=1, width=-2 * mx,
            height=bg_h - 50 - 2 * my,
        )

        # ── Frame dimensions computed from actual main_frame fill ────────────
        # We use relwidth on sub-frames so they scale with main_frame
        gap = 10

        # ── LEFT FRAME (50 % of main frame) ──────────────────────────────────
        Left_frame = LabelFrame(
            main_frame, bd=2, relief=RIDGE,
            text="Left Frame", font=("times new roman", 18, "bold"),
            bg="white", fg="red",
        )
        Left_frame.place(x=gap, y=gap, relwidth=0.50, relheight=0.97,
                         width=-gap * 2)

        # ── Decorative image inside left frame (18 % of left frame height) ───
        # We use a sub-frame trick: bind <Configure> to re-draw when size is known
        self._left_img_lbl = Label(Left_frame, bg="white")
        self._left_img_lbl.place(relx=0, rely=0, relwidth=1, relheight=0.18)

        def _load_left_img(event=None):
            w = Left_frame.winfo_width()
            h = Left_frame.winfo_height()
            if w < 10 or h < 10:
                return
            img_w = w - 10
            img_h = max(10, int(h * 0.18))
            img = Image.open(r"static\images\attendance_left.jpg")
            img = img.resize((img_w, img_h), Image.Resampling.LANCZOS)
            self._left_photo = ImageTk.PhotoImage(img) # type: ignore
            self._left_img_lbl.config(image=self._left_photo, # type: ignore
                                      width=img_w, height=img_h)

        Left_frame.bind("<Configure>", _load_left_img)

        # ── Current Course sub-frame (inside left, below image) ───────────────
        course_frame = LabelFrame(
            Left_frame, bd=2, relief=RIDGE,
            text="Current Course", font=("times new roman", 13, "bold"),
            bg="white", fg="red",
        )
        course_frame.place(relx=0, rely=0.19, relwidth=1, relheight=0.22)

        Label(course_frame, text="Department",
              font=("times new roman", 11, "bold"), bg="white"
              ).grid(row=0, column=0, padx=10, pady=8, sticky=W)
        dep_combo = ttk.Combobox(
            course_frame, textvariable=self.var_dep,
            font=("times new roman", 11, "bold"), state="readonly", width=16,
        )
        dep_combo["values"] = ("Select Department", "BCA", "MCA", "Cyber Security")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=8, sticky=W)

        Label(course_frame, text="Year",
              font=("times new roman", 11, "bold"), bg="white"
              ).grid(row=1, column=0, padx=10, pady=8, sticky=W)
        year_combo = ttk.Combobox(
            course_frame, textvariable=self.var_date,
            font=("times new roman", 11, "bold"), state="readonly", width=16,
        )
        year_combo["values"] = ("Select Year", "2022-23", "2023-24", "2024-25")
        year_combo.current(2)
        year_combo.grid(row=1, column=1, padx=10, pady=8, sticky=W)

        # ── Class Student Info sub-frame ──────────────────────────────────────
        info_frame = LabelFrame(
            Left_frame, bd=2, relief=RIDGE,
            text="Class Student Info", font=("times new roman", 13, "bold"),
            bg="white", fg="red",
        )
        info_frame.place(relx=0, rely=0.42, relwidth=1, relheight=0.56)

        fields = [
            ("AttendanceId",       self.var_attendance_id,     0, 0),
            ("Roll:",              self.var_roll,              0, 2),
            ("Name:",              self.var_name,              1, 0),
            ("Dept:",              self.var_dep,               1, 2),
            ("Time",               self.var_time,              2, 0),
            ("Date:",              self.var_date,              2, 2),
            ("Attendance Status:", self.var_attendance_status, 3, 0),
        ]

        for (text, var, row, col) in fields:
            Label(
                info_frame, text=text,
                font=("times new roman", 11, "bold"), bg="white",
            ).grid(row=row, column=col, padx=8, pady=8, sticky=W)

            if text == "Attendance Status:":
                combo = ttk.Combobox(
                    info_frame, textvariable=var,
                    font=("times new roman", 11, "bold"),
                    state="readonly", width=16,
                )
                combo["values"] = ("Status", "Present", "Absent")
                combo.current(0)
                combo.grid(row=row, column=col + 1, padx=8, pady=8, sticky=W)
            elif text == "Dept:":
                combo = ttk.Combobox(
                    info_frame, textvariable=var,
                    font=("times new roman", 11, "bold"),
                    state="readonly", width=16,
                )
                combo["values"] = ("Select course", "MCA", "BCA")
                combo.current(0)
                combo.grid(row=row, column=col + 1, padx=8, pady=8, sticky=W)
            else:
                ttk.Entry(
                    info_frame, textvariable=var, width=18,
                    font=("times new roman", 12, "bold"),
                ).grid(row=row, column=col + 1, padx=8, pady=8, sticky=W)

        # Buttons row inside info_frame
        btn_frame = Frame(info_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.grid(row=7, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        btn_font = ("times new roman", 11, "bold")
        Button(btn_frame, text="Import CSV",  command=self.importCSV,  font=btn_font, bg="blue", fg="white").grid(row=0, column=0, sticky="nsew")
        Button(btn_frame, text="Export CSV",  command=self.exportCSV,  font=btn_font, bg="blue", fg="white").grid(row=0, column=1, sticky="nsew")
        Button(btn_frame, text="Update",      command=self.update_data, font=btn_font, bg="blue", fg="white").grid(row=0, column=2, sticky="nsew")
        Button(btn_frame, text="Reset",       command=self.reset_data, font=btn_font, bg="blue", fg="white").grid(row=0, column=3, sticky="nsew")

        # ── RIGHT FRAME (remaining width) ─────────────────────────────────────
        Right_frame = LabelFrame(
            main_frame, bd=2, relief=RIDGE,
            text="Right Frame", font=("times new roman", 18, "bold"),
            bg="white", fg="red",
        )
        # starts just after the left frame (50 % + gap)
        Right_frame.place(relx=0.50, rely=0, x=gap * 2, y=gap,
                          relwidth=0.50, relheight=0.97,
                          width=-gap * 3)

        # ── Decorative image inside right frame ───────────────────────────────
        self._right_img_lbl = Label(Right_frame, bg="white")
        self._right_img_lbl.place(relx=0, rely=0, relwidth=1, height=130)

        def _load_right_img(event=None):
            w = Right_frame.winfo_width()
            if w < 10:
                return
            img = Image.open(r"static\images\attendance_right.jpg")
            img = img.resize((w - 10, 130), Image.Resampling.LANCZOS)
            self._right_photo = ImageTk.PhotoImage(img) # type: ignore
            self._right_img_lbl.config(image=self._right_photo) # type: ignore

        Right_frame.bind("<Configure>", _load_right_img)

        # ── Search bar ────────────────────────────────────────────────────────
        self.var_search = StringVar()
        search_frame = Frame(Right_frame, bg="white")
        search_frame.place(relx=0, rely=0, y=130, relwidth=1, height=50)

        Label(search_frame, text="Search By:",
              font=("times new roman", 11, "bold"), bg="white"
              ).pack(side=LEFT, padx=6)

        self.combo_search = ttk.Combobox(
            search_frame, textvariable=self.var_search,
            font=("times new roman", 11, "bold"), state="readonly", width=12,
        )
        self.combo_search["values"] = ("Select", "Roll", "Name", "Date", "Department")
        self.combo_search.current(0)
        self.combo_search.pack(side=LEFT, padx=6)

        self.var_search_entry = StringVar()
        ttk.Entry(
            search_frame, textvariable=self.var_search_entry,
            font=("times new roman", 11, "bold"), width=16,
        ).pack(side=LEFT, padx=6)

        Button(
            search_frame, text="Search", command=self.search_data,
            font=("times new roman", 11, "bold"), bg="blue", fg="white",
            cursor="hand2",
        ).pack(side=LEFT, padx=4)

        Button(
            search_frame, text="Show All", command=lambda: self.fetchData(mydata),
            font=("times new roman", 11, "bold"), bg="darkgreen", fg="white",
            cursor="hand2",
        ).pack(side=LEFT, padx=4)

        # ── Table ─────────────────────────────────────────────────────────────
        table_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(relx=0, rely=0, y=182, relwidth=1, relheight=1,
                          height=-182)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.attendanceReportTable = ttk.Treeview(
            table_frame,
            columns=("id", "roll", "name", "department", "time", "date", "attendance"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )
        scroll_x.config(command=self.attendanceReportTable.xview)
        scroll_y.config(command=self.attendanceReportTable.yview)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT,  fill=Y)

        for col, heading in [
            ("id",          "Attendance ID"),
            ("roll",        "Roll"),
            ("name",        "Name"),
            ("department",  "Department"),
            ("time",        "Time"),
            ("date",        "Date"),
            ("attendance",  "Attendance"),
        ]:
            self.attendanceReportTable.heading(col, text=heading)
            self.attendanceReportTable.column(col, width=100, anchor=CENTER)

        self.attendanceReportTable["show"] = "headings"
        self.attendanceReportTable.pack(fill=BOTH, expand=True)
        self.attendanceReportTable.bind("<ButtonRelease>", self.get_cursor)

    # ────────────────────────────────────────────────────────────────────────
    # CLOSE
    # ────────────────────────────────────────────────────────────────────────
    def on_close(self):
        self.root.destroy()

    # ────────────────────────────────────────────────────────────────────────
    # MARK ATTENDANCE (called from face_recognition module)
    # ────────────────────────────────────────────────────────────────────────
    def mark_attendance(self, roll, name, department):
        global mydata, marked_today

        today = datetime.now().strftime("%Y-%m-%d")
        key   = f"{roll}_{today}"

        if key in marked_today:
            return False
        marked_today.add(key)

        now           = datetime.now()
        attendance_id = len(mydata) + 1
        time_str      = now.strftime("%H:%M:%S")
        record        = [attendance_id, roll, name, department, time_str, today, "Present"]

        mydata.append(record)
        self.fetchData(mydata)
        return True

    # ────────────────────────────────────────────────────────────────────────
    # FETCH / POPULATE TABLE
    # ────────────────────────────────────────────────────────────────────────
    def fetchData(self, rows):
        self.attendanceReportTable.delete(*self.attendanceReportTable.get_children())
        for row in rows:
            self.attendanceReportTable.insert("", END, values=row)

    # ────────────────────────────────────────────────────────────────────────
    # SEARCH
    # ────────────────────────────────────────────────────────────────────────
    def search_data(self):
        col_map = {
            "Roll": 1, "Name": 2, "Department": 3, "Date": 5,
        }
        field = self.var_search.get()
        term  = self.var_search_entry.get().strip().lower()

        if field == "Select" or not term:
            messagebox.showerror("Error", "Select a search field and enter a term.",
                                 parent=self.root)
            return

        idx = col_map.get(field)
        if idx is None:
            return

        results = [row for row in mydata if term in str(row[idx]).lower()]
        self.fetchData(results)

    # ────────────────────────────────────────────────────────────────────────
    # IMPORT CSV
    # ────────────────────────────────────────────────────────────────────────
    def importCSV(self):
        global mydata
        mydata.clear()

        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Open CSV",
            filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),
            parent=self.root,
        )
        if not fln:
            return

        with open(fln, newline="") as myfile:
            reader = csv.reader(myfile)
            for i, row in enumerate(reader):
                if i == 0 and row and row[0].strip().lower() in (
                    "attendanceid", "attendance id", "id"
                ):
                    continue  # skip header
                if row:
                    mydata.append(row)

        self.fetchData(mydata)

    # ────────────────────────────────────────────────────────────────────────
    # EXPORT CSV
    # ────────────────────────────────────────────────────────────────────────
    def exportCSV(self):
        try:
            if not mydata:
                messagebox.showerror("No Data", "No Data Found!", parent=self.root)
                return

            fln = filedialog.asksaveasfilename(
                initialdir=os.getcwd(), title="Save CSV",
                defaultextension=".csv",
                filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),
                parent=self.root,
            )
            if not fln:
                return

            with open(fln, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "AttendanceId", "Roll", "Name", "Dept",
                    "Time", "Date", "Attendance Status",
                ])
                writer.writerows(mydata)

            messagebox.showinfo(
                "Data Export",
                f"Data exported to {os.path.basename(fln)} successfully.",
            )
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # ────────────────────────────────────────────────────────────────────────
    # GET ROW INTO FORM FIELDS
    # ────────────────────────────────────────────────────────────────────────
    def get_cursor(self, event):
        cursor_row = self.attendanceReportTable.focus()
        content    = self.attendanceReportTable.item(cursor_row)
        rows       = content["values"]
        if rows:
            self.var_attendance_id.set(rows[0])
            self.var_roll.set(rows[1])
            self.var_name.set(rows[2])
            self.var_dep.set(rows[3])
            self.var_time.set(rows[4])
            self.var_date.set(rows[5])
            self.var_attendance_status.set(rows[6])

    # ────────────────────────────────────────────────────────────────────────
    # RESET FORM
    # ────────────────────────────────────────────────────────────────────────
    def reset_data(self):
        for var in (
            self.var_attendance_id, self.var_roll, self.var_name,
            self.var_dep, self.var_time, self.var_date,
            self.var_attendance_status,
        ):
            var.set("")

    # ────────────────────────────────────────────────────────────────────────
    # UPDATE
    # ────────────────────────────────────────────────────────────────────────
    def update_data(self):
        global mydata

        aid    = self.var_attendance_id.get()
        status = self.var_attendance_status.get()

        if not aid:
            messagebox.showerror("No Selection",
                                 "Please select a record from the table first.",
                                 parent=self.root)
            return

        if not status or status == "Status":
            messagebox.showerror("Missing Status",
                                 "Please select Present or Absent.",
                                 parent=self.root)
            return

        for i, row in enumerate(mydata):
            if str(row[0]) == str(aid):
                mydata[i] = [
                    aid,
                    self.var_roll.get(),
                    self.var_name.get(),
                    self.var_dep.get(),
                    self.var_time.get(),
                    self.var_date.get(),
                    status,
                ]
                self.fetchData(mydata)
                messagebox.showinfo("Success",
                                    "Attendance record updated successfully.",
                                    parent=self.root)
                self.reset_data()
                return

        messagebox.showerror("Not Found",
                             "Could not find the record to update.",
                             parent=self.root)


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    Attendance(root)
    root.mainloop()