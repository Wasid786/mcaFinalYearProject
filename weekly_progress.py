"""
weekly_progress.py  –  Grid-style weekly assignment tracker
===========================================================
Layout:
  - Rows   : one row per student (Name | Roll No | Student ID | Week 1…Week 10 | Total Done)
  - Columns: Week 1…Week 10 (click a cell to toggle Done / Pending)
  - Toolbar: Course / Semester / Year dropdowns + Search box + action buttons
  - Summary bar showing live counts
  - Fully responsive: all sizes are % of screen width/height
"""

from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import csv
import os
from datetime import datetime

# ── constants ─────────────────────────────────────────────────────────────────
WEEKS        = 10
COLOR_DONE   = "#c8e6c9"
COLOR_HEADER = "#1a237e"

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
        self.root.title("Weekly Assignment Progress")
        self.root.state("zoomed")

        self.root.update_idletasks()
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        self.root.geometry(f"{self.sw}x{self.sh}+0+0")

        # ── filter variables ──────────────────────────────────────────────────
        self.var_course = StringVar(value="All")
        self.var_dep = StringVar(value="All")
        self.var_sem    = StringVar(value="All")
        self.var_year   = StringVar(value="All")
        self.var_search = StringVar()

        # ── summary variables ─────────────────────────────────────────────────
        self.var_shown   = StringVar(value="0")
        self.var_done    = StringVar(value="0")
        self.var_pending = StringVar(value="0")
        self.var_pct     = StringVar(value="0%")

        # ── data ──────────────────────────────────────────────────────────────
        self.assignment_data = {}   # {student_id: set(done_weeks)}
        self.staged          = {}   # {student_id: set(staged_weeks)}
        self.student_rows    = []

        self.ensure_table()
        self.build_ui()
        self.load_students()

    # =========================================================================
    #  DATABASE
    # =========================================================================

    def get_conn(self):
        return mysql.connector.connect(
            host="localhost", user="root",
            password="Wasid@5284mysql",
            database="face_recognizer",
        )

    def ensure_table(self):
        conn = None
        try:
            conn = self.get_conn()
            cur  = conn.cursor()
            cur.execute(SQL_CREATE)
            try:
                cur.execute(SQL_DROP_MONTH)
            except mysql.connector.Error as err:
                if err.errno != 1091:
                    raise
            conn.commit()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            if conn:
                conn.close()

    def load_students(self):
        conn = None
        try:
            conn = self.get_conn()
            cur  = conn.cursor()

            cond, params = [], []
            if self.var_dep.get() != "All":
                cond.append("dep=%s");   params.append(self.var_dep.get())
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

            q = self.var_search.get().strip().lower()
            if q:
                rows = [r for r in rows
                        if q in r[1].lower() or q in str(r[0]) or q in r[2].lower()]  # type: ignore

            self.student_rows = [
                {"id": r[0], "name": r[1], "roll": r[2],  # type: ignore
                 "course": r[3], "sem": r[4], "year": r[5]} # type: ignore
                for r in rows
            ]

            if self.student_rows:
                sids = tuple(s["id"] for s in self.student_rows)
                ph   = ",".join(["%s"] * len(sids))
                cur.execute(
                    f"SELECT student_id, week_number FROM weekly_assignment "
                    f"WHERE student_id IN ({ph}) AND status='Done'",
                    sids,  # type: ignore
                )
                raw = cur.fetchall()
            else:
                raw = []

            self.assignment_data = {}
            for (sid, week) in raw:
                self.assignment_data.setdefault(sid, set()).add(week)

            self.staged = {}

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if conn:
                conn.close()

        self.render_grid()

    def stage_week(self, student_id, week):
        if week in self.assignment_data.get(student_id, set()):
            return  # already saved – locked
        staged_weeks = self.staged.setdefault(student_id, set())
        if week in staged_weeks:
            staged_weeks.discard(week)
        else:
            staged_weeks.add(week)
        self.render_grid()

    def save_staged(self):
        to_save = [
            (s, w)
            for s in self.student_rows
            for w in self.staged.get(s["id"], set())
        ]
        if not to_save:
            messagebox.showinfo(
                "Nothing to save",
                "No new assignments are ticked.\nClick blank cells first, then press Save.",
                parent=self.root,
            )
            return

        if not messagebox.askyesno(
            "Confirm Save",
            f"You are about to mark {len(to_save)} assignment(s) as Done.\n\n"
            "This CANNOT be undone. Continue?",
            parent=self.root,
        ):
            return

        conn = None
        try:
            conn = self.get_conn()
            cur  = conn.cursor()
            now  = datetime.now()

            for s in self.student_rows:
                sid = s["id"]
                for w in self.staged.get(sid, set()):
                    cur.execute(
                        """
                        INSERT INTO weekly_assignment
                            (student_id, student_name, week_number,
                             course, semester, year, status, marked_on)
                        VALUES (%s, %s, %s, %s, %s, %s, 'Done', %s)
                        ON DUPLICATE KEY UPDATE
                            student_name=%s, status='Done', marked_on=%s
                        """,
                        (sid, s["name"], w, s["course"], s["sem"], s["year"], now,
                         s["name"], now),  # type: ignore
                    )
                    self.assignment_data.setdefault(sid, set()).add(w)

            conn.commit()
            self.staged = {}
            messagebox.showinfo(
                "Saved",
                f"{len(to_save)} assignment(s) marked as Done and saved.",
                parent=self.root,
            )
            self.render_grid()

        except Exception as e:
            messagebox.showerror("Save Error", str(e), parent=self.root)
        finally:
            if conn:
                conn.close()

    # =========================================================================
    #  UI BUILD
    # =========================================================================

    def build_ui(self):
        sw, sh = self.sw, self.sh

        # ── Title bar ────────────────────────────────────────────────────────
        title_size = max(18, int(sw * 0.020))
        Label(
            self.root, text="Weekly Assignment Progress",
            font=("times new roman", title_size, "bold"),
            bg=COLOR_HEADER, fg="white",
        ).place(relx=0, rely=0, relwidth=1, height=52)

        # ── Background image ─────────────────────────────────────────────────
        bg_y = 52
        bg_h = sh - bg_y
        try:
            img = Image.open(r"static\images\img04.jpg")
            img = img.resize((sw, bg_h), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            Label(self.root, image=self.bg_photo).place(
                x=0, y=bg_y, relwidth=1, height=bg_h
            )
        except Exception:
            Label(self.root, bg="#e8eaf6").place(
                x=0, y=bg_y, relwidth=1, height=bg_h
            )

        # ── Main card (fills everything below title, with small padding) ─────
        pad = max(6, int(sw * 0.005))
        self.card = Frame(self.root, bg="white", bd=1, relief=RIDGE)
        self.card.place(
            x=pad, y=bg_y + pad,
            relwidth=1, width=-pad * 2,
            height=bg_h - pad * 2,
        )

        self._build_toolbar()
        self._build_summary()

        # grid area starts below toolbar (50 px) + summary (52 px) + small gap
        grid_y = 50 + 52 + 8
        # card height = bg_h - 2*pad; grid fills the rest
        card_h = bg_h - pad * 2
        grid_h = card_h - grid_y - 6
        self._build_grid_area(grid_y, grid_h)

    # ── Toolbar ──────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        sw = self.sw
        font_bold   = ("times new roman", max(10, int(sw * 0.009)), "bold")
        font_normal = ("times new roman", max(9,  int(sw * 0.008)))
        font_small  = ("times new roman", max(9,  int(sw * 0.008)))

        tf = Frame(self.card, bg="white")
        tf.place(x=8, y=6, relwidth=1, width=-16, height=46)

        # Dropdowns
        items = [
            ("Department:",   self.var_course, ["All", "MCA", "BCA", "Cyber"],                         0, 0),
            ("Semester:", self.var_sem,    ["All", "Sem 1", "Sem 2", "Sem 3", "Sem 4"],        0, 2),
            ("Year:",     self.var_year,   ["All", "2022-23", "2023-24", "2024-25", "2025-26"], 0, 4),
        ]
        for (lbl, var, vals, row, col) in items:
            Label(tf, text=lbl, font=font_bold, bg="white").grid(
                row=row, column=col, padx=(4, 2), sticky=W
            )
            ttk.Combobox(
                tf, textvariable=var, values=vals,
                state="readonly", width=9, font=font_normal,
            ).grid(row=row, column=col + 1, padx=(0, 8), sticky=W)

        # Search
        Label(tf, text="Search:", font=font_bold, bg="white").grid(
            row=0, column=6, padx=(4, 2), sticky=W
        )
        ttk.Entry(
            tf, textvariable=self.var_search, width=16, font=font_normal,
        ).grid(row=0, column=7, padx=(0, 6), sticky=W)

        # Action buttons
        for col, (text, cmd, color) in enumerate([
            ("Apply",         self.load_students,  COLOR_HEADER),
            ("Reset",         self.reset_filters,  "#757575"),
            ("Save Marked", self.save_staged,   "#e65100"),
            ("Export CSV",    self.export_csv,     "#388e3c"),
        ], start=8):
            Button(
                tf, text=text, command=cmd,
                font=font_small, bg=color, fg="white",
                relief=FLAT, padx=6, cursor="hand2",
            ).grid(row=0, column=col, padx=3, sticky=W)

    # ── Summary strip ─────────────────────────────────────────────────────────
    def _build_summary(self):
        sw = self.sw
        sf = Frame(self.card, bg=COLOR_HEADER)
        sf.place(x=8, y=54, relwidth=1, width=-16, height=50)

        num_font = ("times new roman", max(13, int(sw * 0.012)), "bold")
        lbl_font = ("times new roman", max(8, int(sw * 0.007)))

        for (text, var) in [
            ("Students",   self.var_shown),
            ("Done",       self.var_done),
            ("Pending",    self.var_pending),
            ("Completion", self.var_pct),
        ]:
            col = Frame(sf, bg=COLOR_HEADER)
            col.pack(side=LEFT, padx=max(10, int(sw * 0.012)), pady=3)
            Label(col, text=text, font=lbl_font, bg=COLOR_HEADER, fg="#90caf9").pack()
            Label(col, textvariable=var, font=num_font, bg=COLOR_HEADER, fg="white").pack()

    # ── Scrollable grid area ──────────────────────────────────────────────────
    def _build_grid_area(self, y, h):
        outer = Frame(self.card, bg="white")
        outer.place(x=4, y=y, relwidth=1, width=-8, height=h)

        vscr = ttk.Scrollbar(outer, orient=VERTICAL)
        hscr = ttk.Scrollbar(outer, orient=HORIZONTAL)
        vscr.pack(side=RIGHT,  fill=Y)
        hscr.pack(side=BOTTOM, fill=X)

        self.canvas = Canvas(
            outer, bg="white",
            yscrollcommand=vscr.set,
            xscrollcommand=hscr.set,
        )
        self.canvas.pack(fill=BOTH, expand=True)
        vscr.config(command=self.canvas.yview)
        hscr.config(command=self.canvas.xview)

        self.grid_frame = Frame(self.canvas, bg="white")
        self.cw = self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self.cw, width=max(e.width, self.grid_frame.winfo_reqwidth())
            ),
        )
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

    # =========================================================================
    #  GRID RENDERER
    # =========================================================================

    def render_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        sw = self.sw

        # Scale column widths proportionally to screen width
        # Base widths at 1920 px: name=170, roll=80, id=90, week=64, total=82
        scale    = sw / 1920
        name_w   = max(120, int(170 * scale))
        roll_w   = max(55,  int(80  * scale))
        id_w     = max(65,  int(90  * scale))
        week_w   = max(48,  int(64  * scale))
        total_w  = max(60,  int(82  * scale))

        col_widths = [name_w, roll_w, id_w] + [week_w] * WEEKS + [total_w]

        header_font = ("times new roman", max(9, int(sw * 0.007)), "bold")
        cell_font   = ("times new roman", max(9, int(sw * 0.008)), "bold")
        small_font  = ("times new roman", max(8, int(sw * 0.007)))

        headers = (
            ["Student Name", "Roll No", "Student ID"]
            + [f"Week {i}" for i in range(1, WEEKS + 1)]
            + ["Total\nDone"]
        )

        for col, (txt, cw) in enumerate(zip(headers, col_widths)):
            Label(
                self.grid_frame, text=txt,
                font=header_font,
                bg=COLOR_HEADER, fg="white",
                padx=3, pady=5, wraplength=cw,
            ).grid(row=0, column=col, sticky="nsew", padx=1, pady=(0, 2))

        if not self.student_rows:
            Label(
                self.grid_frame,
                text="No students found for these filters.",
                font=("times new roman", max(11, int(sw * 0.009))),
                bg="white", fg="#888",
            ).grid(row=1, column=0, columnspan=len(headers), pady=30)
            self.update_summary([])
            return

        for r_idx, s in enumerate(self.student_rows, start=1):
            sid        = s["id"]
            done_weeks = self.assignment_data.get(sid, set())
            stgd_weeks = self.staged.get(sid, set())
            done_n     = len(done_weeks)
            bg_row     = "#f5f5f5" if r_idx % 2 == 0 else "white"

            Label(self.grid_frame, text=s["name"],  # type: ignore
                  font=cell_font, bg=bg_row, anchor=W, padx=6,
                  ).grid(row=r_idx, column=0, sticky="nsew", padx=1, pady=1)
            Label(self.grid_frame, text=s["roll"],  # type: ignore
                  font=small_font, bg=bg_row, fg="#555",
                  ).grid(row=r_idx, column=1, sticky="nsew", pady=1)
            Label(self.grid_frame, text=str(sid),
                  font=small_font, bg=bg_row, fg="#555",
                  ).grid(row=r_idx, column=2, sticky="nsew", pady=1)

            for w in range(1, WEEKS + 1):
                if w in done_weeks:
                    # Saved – locked, green tick
                    Label(
                        self.grid_frame, text="✓",
                        font=cell_font, bg="#c8e6c9", fg="#2e7d32", relief=FLAT,
                    ).grid(row=r_idx, column=2 + w,
                           sticky="nsew", ipadx=3, ipady=4, padx=1, pady=1)

                elif w in stgd_weeks:
                    # Staged – yellow, clickable to un-stage
                    Button(
                        self.grid_frame, text="✓",
                        font=cell_font, bg="#fff9c4", fg="#f57f17",
                        relief=FLAT, bd=0, cursor="hand2",
                        command=lambda _sid=sid, _w=w: self.stage_week(_sid, _w),
                    ).grid(row=r_idx, column=2 + w,
                           sticky="nsew", ipadx=3, ipady=4, padx=1, pady=1)

                else:
                    # Pending – blank, click to stage
                    Button(
                        self.grid_frame, text="",
                        font=cell_font, bg=bg_row, fg="#2e7d32",
                        relief=FLAT, bd=0, cursor="hand2",
                        command=lambda _sid=sid, _w=w: self.stage_week(_sid, _w),
                    ).grid(row=r_idx, column=2 + w,
                           sticky="nsew", ipadx=3, ipady=4, padx=1, pady=1)

            Label(
                self.grid_frame, text=f"{done_n} / {WEEKS}",
                font=cell_font, bg="#e3f2fd", fg=COLOR_HEADER,
            ).grid(row=r_idx, column=2 + WEEKS + 1,
                   sticky="nsew", padx=1, pady=1)

        for col, cw in enumerate(col_widths):
            self.grid_frame.columnconfigure(col, minsize=cw)

        self.update_summary(self.student_rows)

    def update_summary(self, rows):
        total   = len(rows) * WEEKS
        done    = sum(len(self.assignment_data.get(s["id"], set())) for s in rows)
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
        self.var_dep.set("All")
        self.var_sem.set("All")
        self.var_year.set("All")
        self.var_search.set("")
        self.load_students()

    def export_csv(self):
        if not self.student_rows:
            messagebox.showwarning(
                "Nothing to export", "No students to export.", parent=self.root
            )
            return

        path = os.path.join(
            os.path.expanduser("~"), "Downloads", "weekly_assignments.csv"
        )
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Student Name", "Roll No", "Student ID",
                     "Course", "Semester", "Year"]
                    + [f"Week {i}" for i in range(1, WEEKS + 1)]
                    + ["Total Done"]
                )
                for s in self.student_rows:
                    sid        = s["id"]
                    done_weeks = self.assignment_data.get(sid, set())
                    cells      = ["Done" if i in done_weeks else "Pending"
                                  for i in range(1, WEEKS + 1)]
                    writer.writerow(
                        [s["name"], s["roll"], sid,
                         s["course"], s["sem"], s["year"]]
                        + cells + [len(done_weeks)]
                    )
            messagebox.showinfo("Exported", f"File saved:\n{path}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Export Error", str(e), parent=self.root)


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    Weekly_Progress(root)
    root.mainloop()