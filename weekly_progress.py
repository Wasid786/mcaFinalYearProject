"""
weekly_progress.py  –  Grid-style weekly assignment tracker
===========================================================
Layout (matches the screenshot reference):
  - Rows   : one row per student (Name | Roll No | Student ID | Week 1 … Week 10 | Total Done)
  - Columns: Week 1 … Week 10  (click a cell to toggle Done / Pending)
  - Toolbar: Course / Semester / Year dropdowns + Search box + Export CSV button
  - Summary bar showing counts live

Database table created automatically on first run:
  weekly_assignment (student_id FK → student, week_number, course, semester, year, status)
"""

from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import csv
import os
from datetime import datetime

# ── constants ──────────────────────────────────────────────────────────────────
WEEKS        = 10
FONT_TITLE   = ("times new roman", 28, "bold")
FONT_BOLD    = ("times new roman", 12, "bold")
FONT_NORMAL  = ("times new roman", 11)
FONT_SMALL   = ("times new roman", 10)
COLOR_DONE   = "#c8e6c9"   # light green  – cell background when done
COLOR_HEADER = "#1a237e"   # dark blue    – title / header bar

SQL_CREATE = """
CREATE TABLE IF NOT EXISTS weekly_assignment (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    student_id   INT          NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    week_number  INT          NOT NULL,
    course       VARCHAR(50),
    semester     VARCHAR(50),
    year         VARCHAR(20),
    status       VARCHAR(20) DEFAULT 'Pending',
    marked_on    DATETIME,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uq_std_week (student_id, week_number, course, semester, year)
)
"""

SQL_DROP_MONTH = "ALTER TABLE weekly_assignment DROP COLUMN month"


class Weekly_Progress:
    def __init__(self, root):
        self.root = root
        self.sw   = root.winfo_screenwidth()
        self.sh   = root.winfo_screenheight()
        root.geometry(f"{self.sw}x{self.sh}+0+0")
        root.title("Weekly Assignment Progress")

        # filter dropdowns
        self.var_course = StringVar(value="All")
        self.var_sem    = StringVar(value="All")
        self.var_year   = StringVar(value="All")
        self.var_search = StringVar()

        # summary labels
        self.var_shown   = StringVar(value="0")
        self.var_done    = StringVar(value="0")
        self.var_pending = StringVar(value="0")
        self.var_pct     = StringVar(value="0%")

        # data storage
        self.assignment_data = {}   # {student_id: {week_number: "Done"}}  – saved to DB
        self.staged          = {}   # {student_id: set(week_numbers)}       – ticked but NOT saved yet
        self.student_rows    = []   # list of dicts

        self.ensure_table()
        self.build_ui()
        self.load_students()

    # =========================================================================
    #  DATABASE
    # =========================================================================

    def get_conn(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wasid@5284mysql",   # ← change if needed
            database="face_recognizer"
        )

    def ensure_table(self):
        conn = None
        try:
            conn = self.get_conn()
            cur  = conn.cursor()
            cur.execute(SQL_CREATE)
            # Drop the month column if it was added by an older version (error 1091 = column not found, safe to ignore)
            try:
                cur.execute(SQL_DROP_MONTH)
            except mysql.connector.Error as drop_err:
                if drop_err.errno != 1091:
                    raise
            conn.commit()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            if conn:
                conn.close()

    def load_students(self):
        """Pull student list + their saved Done statuses from DB, apply filters."""
        conn = None
        try:
            conn = self.get_conn()
            cur  = conn.cursor()

            cond, params = [], []
            if self.var_course.get() != "All":
                cond.append("course=%s");   params.append(self.var_course.get())
            if self.var_sem.get() != "All":
                cond.append("semester=%s"); params.append(self.var_sem.get())
            if self.var_year.get() != "All":
                cond.append("year=%s");     params.append(self.var_year.get())

            sql = "SELECT student_id, name, roll, course, semester, year FROM student"
            if cond:
                sql += " WHERE " + " AND ".join(cond)
            sql += " ORDER BY name"
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()

            # client-side search
            q = self.var_search.get().strip().lower()
            if q:
                rows = [r for r in rows if q in r[1].lower() or q in str(r[0]) or q in r[2].lower()] # type: ignore

            self.student_rows = [
                {"id": r[0], "name": r[1], "roll": r[2], # type: ignore
                 "course": r[3], "sem": r[4], "year": r[5]} # type: ignore
                for r in rows
            ]

            # load only "Done" statuses (the only ones saved)
            if self.student_rows:
                sids = tuple(s["id"] for s in self.student_rows)
                ph = ",".join(["%s"] * len(sids))
                cur.execute(
                    f"SELECT student_id, week_number FROM weekly_assignment "
                    f"WHERE student_id IN ({ph}) AND status='Done'",
                    sids # type: ignore
                )
                raw = cur.fetchall()
            else:
                raw = []

            self.assignment_data = {}
            for (sid, week) in raw:
                self.assignment_data.setdefault(sid, set()).add(week)

            # clear any unsaved staging when reloading
            self.staged = {}

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

        self.render_grid()

    def stage_week(self, student_id, week):
        """
        Clicking a blank cell stages it (yellow preview).
        Clicking a staged cell un-stages it (only allowed before Save).
        Clicking a saved Done cell does nothing at all.
        """
        # already saved to DB – locked, do nothing
        if week in self.assignment_data.get(student_id, set()):
            return

        # toggle staging (pre-save)
        staged_weeks = self.staged.setdefault(student_id, set())
        if week in staged_weeks:
            staged_weeks.discard(week)
        else:
            staged_weeks.add(week)

        self.render_grid()

    def save_staged(self):
        """Save all staged (yellow) cells to DB as Done. Cannot be undone."""
        # collect everything staged across all students
        to_save = [
            (s, w)
            for s in self.student_rows
            for w in self.staged.get(s["id"], set())
        ]
        if not to_save:
            messagebox.showinfo("Nothing to save",
                                "No new assignments are ticked.\nClick blank cells first, then press Save.",
                                parent=self.root)
            return

        count = len(to_save)
        confirm = messagebox.askyesno(
            "Confirm Save",
            f"You are about to mark {count} assignment(s) as Done.\n\nThis CANNOT be undone. Continue?",
            parent=self.root
        )
        if not confirm:
            return

        conn = None
        try:
            conn = self.get_conn()
            cur  = conn.cursor()
            now  = datetime.now()

            for s in self.student_rows:
                sid = s["id"]
                for w in self.staged.get(sid, set()):
                    cur.execute("""
                        INSERT INTO weekly_assignment
                            (student_id, student_name, week_number, course, semester, year, status, marked_on)
                        VALUES (%s, %s, %s, %s, %s, %s, 'Done', %s)
                        ON DUPLICATE KEY UPDATE student_name=%s, status='Done', marked_on=%s
                    """, (sid, s["name"], w, s["course"], s["sem"], s["year"], now,
                              s["name"], now)) # type: ignore
                    # move from staged → permanently done in memory
                    self.assignment_data.setdefault(sid, set()).add(w)

            conn.commit()
            self.staged = {}   # clear all staging
            messagebox.showinfo("Saved", f"{count} assignment(s) marked as Done and saved.", parent=self.root)
            self.render_grid()

        except Exception as e:
            messagebox.showerror("Save Error", str(e), parent=self.root)
        finally:
            if conn:
                conn.close()

    # =========================================================================
    #  UI
    # =========================================================================

    def build_ui(self):
        # title
        Label(self.root, text="Weekly Assignment Progress",
              font=FONT_TITLE, bg=COLOR_HEADER, fg="white"
              ).place(relx=0, rely=0, relwidth=1, height=52)

        # background image
        bg_y = 52
        bg_h = self.sh - bg_y
        try:
            img = Image.open(r"static\images\img04.jpg")
            img = img.resize((self.sw, bg_h), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            Label(self.root, image=self.bg_photo).place(x=0, y=bg_y, width=self.sw, height=bg_h)
        except Exception:
            Label(self.root, bg="#e8eaf6").place(x=0, y=bg_y, width=self.sw, height=bg_h)

        # main white card
        pad    = 10
        card_w = self.sw  - pad * 2
        card_h = bg_h - pad * 2
        self.card = Frame(self.root, bg="white", bd=1, relief=RIDGE)
        self.card.place(x=pad, y=bg_y + pad, width=card_w, height=card_h)

        self.build_toolbar(self.card, card_w)
        self.build_summary(self.card, card_w)

        grid_y = 122
        grid_h = card_h - grid_y - 6
        self.build_grid_area(self.card, card_w, grid_y, grid_h)

    # ── toolbar ──────────────────────────────────────────────────────────────
    def build_toolbar(self, parent, w):
        tf = Frame(parent, bg="white")
        tf.place(x=8, y=8, width=w - 16, height=50)

        items = [
            ("Course:",   self.var_course, ["All","FY","SY","TY"],                           0, 0),
            ("Semester:", self.var_sem,    ["All","Sem 1","Sem 2","Sem 3","Sem 4"],           0, 2),
            ("Year:",     self.var_year,   ["All","2022-23","2023-24","2024-25","2025-26"],   0, 4),
        ]
        for (lbl, var, vals, row, col) in items:
            Label(tf, text=lbl, font=FONT_BOLD, bg="white").grid(row=row, column=col, padx=(4,2), sticky=W)
            ttk.Combobox(tf, textvariable=var, values=vals,
                         state="readonly", width=9, font=FONT_NORMAL
                         ).grid(row=row, column=col+1, padx=(0,10), sticky=W)

        Label(tf, text="Search:", font=FONT_BOLD, bg="white").grid(row=0, column=6, padx=(4,2), sticky=W)
        ttk.Entry(tf, textvariable=self.var_search, width=18, font=FONT_NORMAL
                  ).grid(row=0, column=7, padx=(0,8), sticky=W)

        Button(tf, text="Apply",        command=self.load_students,  font=FONT_SMALL, bg=COLOR_HEADER, fg="white", relief=FLAT, padx=8).grid(row=0, column=8,  padx=3)
        Button(tf, text="Reset",        command=self.reset_filters,  font=FONT_SMALL, bg="#757575",    fg="white", relief=FLAT, padx=8).grid(row=0, column=9,  padx=3)
        Button(tf, text="💾 Save Marked", command=self.save_staged,  font=FONT_SMALL, bg="#e65100",    fg="white", relief=FLAT, padx=8).grid(row=0, column=10, padx=3)
        Button(tf, text="Export CSV",   command=self.export_csv,     font=FONT_SMALL, bg="#388e3c",    fg="white", relief=FLAT, padx=8).grid(row=0, column=11, padx=3)

    # ── summary strip ────────────────────────────────────────────────────────
    def build_summary(self, parent, w):
        sf = Frame(parent, bg=COLOR_HEADER)
        sf.place(x=8, y=62, width=w - 16, height=52)

        for (text, var) in [("Students", self.var_shown), ("Done", self.var_done),
                             ("Pending",  self.var_pending), ("Completion", self.var_pct)]:
            col = Frame(sf, bg=COLOR_HEADER)
            col.pack(side=LEFT, padx=20, pady=4)
            Label(col, text=text, font=("times new roman", 9), bg=COLOR_HEADER, fg="#90caf9").pack()
            Label(col, textvariable=var, font=("times new roman", 16, "bold"), bg=COLOR_HEADER, fg="white").pack()

    # ── scrollable canvas for the grid ───────────────────────────────────────
    def build_grid_area(self, parent, w, y, h):
        outer = Frame(parent, bg="white")
        outer.place(x=4, y=y, width=w - 8, height=h)

        vscr = ttk.Scrollbar(outer, orient=VERTICAL)
        hscr = ttk.Scrollbar(outer, orient=HORIZONTAL)
        vscr.pack(side=RIGHT, fill=Y)
        hscr.pack(side=BOTTOM, fill=X)

        self.canvas = Canvas(outer, bg="white",
                             yscrollcommand=vscr.set,
                             xscrollcommand=hscr.set)
        self.canvas.pack(fill=BOTH, expand=True)
        vscr.config(command=self.canvas.yview)
        hscr.config(command=self.canvas.xview)

        self.grid_frame = Frame(self.canvas, bg="white")
        self.cw = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        self.grid_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(
            self.cw, width=max(e.width, self.grid_frame.winfo_reqwidth())))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

    # =========================================================================
    #  GRID RENDERER
    # =========================================================================

    def render_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        col_widths = [170, 80, 90] + [64] * WEEKS + [82]

        # header
        headers = ["Student Name", "Roll No", "Student ID"] + \
                  [f"Week {i}" for i in range(1, WEEKS + 1)] + ["Total\nDone"]
        for col, (txt, cw) in enumerate(zip(headers, col_widths)):
            Label(self.grid_frame, text=txt,
                  font=("times new roman", 10, "bold"),
                  bg=COLOR_HEADER, fg="white", padx=3, pady=5, wraplength=cw
                  ).grid(row=0, column=col, sticky="nsew", padx=1, pady=(0, 2))

        if not self.student_rows:
            Label(self.grid_frame, text="No students found for these filters.",
                  font=FONT_NORMAL, bg="white", fg="#888"
                  ).grid(row=1, column=0, columnspan=len(headers), pady=30)
            self.update_summary([])
            return

        for r_idx, s in enumerate(self.student_rows, start=1):
            sid        = s["id"]
            done_weeks = self.assignment_data.get(sid, set())
            stgd_weeks = self.staged.get(sid, set())
            done_n     = len(done_weeks)
            bg_row     = "#f5f5f5" if r_idx % 2 == 0 else "white"

            Label(self.grid_frame, text=s["name"], font=FONT_BOLD, # type: ignore
                  bg=bg_row, anchor=W, padx=8
                  ).grid(row=r_idx, column=0, sticky="nsew", padx=1, pady=1)
            Label(self.grid_frame, text=s["roll"], font=FONT_SMALL, # type: ignore
                  bg=bg_row, fg="#555"
                  ).grid(row=r_idx, column=1, sticky="nsew", pady=1)
            Label(self.grid_frame, text=str(sid), font=FONT_SMALL,
                  bg=bg_row, fg="#555"
                  ).grid(row=r_idx, column=2, sticky="nsew", pady=1)

            for w in range(1, WEEKS + 1):
                if w in done_weeks:
                    # ── LOCKED: saved to DB, cannot be clicked ────────
                    Label(
                        self.grid_frame,
                        text="✓",
                        font=("times new roman", 11, "bold"),
                        bg="#c8e6c9", fg="#2e7d32",
                        relief=FLAT
                    ).grid(row=r_idx, column=2 + w, sticky="nsew",
                           ipadx=4, ipady=5, padx=1, pady=1)

                elif w in stgd_weeks:
                    # ── STAGED: ticked but not yet saved (yellow) ─────
                    Button(
                        self.grid_frame,
                        text="✓",
                        font=("times new roman", 11, "bold"),
                        bg="#fff9c4", fg="#f57f17",
                        relief=FLAT, bd=0, cursor="hand2",
                        command=lambda _sid=sid, _w=w: self.stage_week(_sid, _w)
                    ).grid(row=r_idx, column=2 + w, sticky="nsew",
                           ipadx=4, ipady=5, padx=1, pady=1)

                else:
                    # ── BLANK: pending, click to stage ────────────────
                    Button(
                        self.grid_frame,
                        text="",
                        font=("times new roman", 11, "bold"),
                        bg=bg_row, fg="#2e7d32",
                        relief=FLAT, bd=0, cursor="hand2",
                        command=lambda _sid=sid, _w=w: self.stage_week(_sid, _w)
                    ).grid(row=r_idx, column=2 + w, sticky="nsew",
                           ipadx=4, ipady=5, padx=1, pady=1)

            Label(self.grid_frame,
                  text=f"{done_n} / {WEEKS}",
                  font=("times new roman", 11, "bold"),
                  bg="#e3f2fd", fg=COLOR_HEADER
                  ).grid(row=r_idx, column=2 + WEEKS + 1, sticky="nsew", padx=1, pady=1)

        for col, cw in enumerate(col_widths):
            self.grid_frame.columnconfigure(col, minsize=cw)

        self.update_summary(self.student_rows)

    def update_summary(self, rows):
        total = len(rows) * WEEKS
        done  = sum(len(self.assignment_data.get(s["id"], set())) for s in rows)
        pending = total - done
        pct     = round(done / total * 100) if total else 0
        self.var_shown.set(str(len(rows)))
        self.var_done.set(str(done))
        self.var_pending.set(str(pending))
        self.var_pct.set(f"{pct}%")



    # =========================================================================
    #  FILTER / EXPORT
    # =========================================================================

    def reset_filters(self):
        self.var_course.set("All")
        self.var_sem.set("All")
        self.var_year.set("All")
        self.var_search.set("")
        self.load_students()

    def export_csv(self):
        if not self.student_rows:
            messagebox.showwarning("Nothing to export", "No students to export.", parent=self.root)
            return
        path = os.path.join(os.path.expanduser("~"), "Downloads", "weekly_assignments.csv")
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Student Name","Roll No","Student ID","Course","Semester","Year"] +
                           [f"Week {i}" for i in range(1, WEEKS + 1)] + ["Total Done"])
                for s in self.student_rows:
                    sid   = s["id"]
                    done_weeks = self.assignment_data.get(sid, set())
                    cells = ["Done" if i in done_weeks else "Pending" for i in range(1, WEEKS + 1)]
                    done_n = len(done_weeks)
                    w.writerow([s["name"], s["roll"], sid, s["course"], s["sem"], s["year"]] + cells + [done_n])
            messagebox.showinfo("Exported", f"File saved:\n{path}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Export Error", str(e), parent=self.root)


if __name__ == "__main__":
    root = Tk()
    app  = Weekly_Progress(root)
    root.mainloop()