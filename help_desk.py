import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import mysql.connector
from datetime import datetime


# ─── DB config (same as the rest of the project) ────────────────────────────
DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="Wasid@5284mysql",
    database="register",
)


class Help_Desk:
    """Simple Help-Desk window with three tabs:
       1. FAQ            – common questions & answers (accordion style)
       2. Submit Ticket  – user fills a form, stored in DB
       3. Contact        – team contact info
    """

    def __init__(self, root: tk.Toplevel | tk.Tk):
        self.root = root
        self.root.title("Help Desk")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        self.root.configure(bg="#f0f4f8")

        self._build_header()
        self._build_notebook()
        self._ensure_table()

    # ── Header ───────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.root, bg="#003366", height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="  Help Desk",
            font=("Arial", 22, "bold"),
            bg="#003366",
            fg="white",
            anchor="w",
        ).pack(side="left", padx=20, fill="y")

        tk.Label(
            hdr,
            text="Face Recognition Attendance System",
            font=("Arial", 11),
            bg="#003366",
            fg="#a8c8f0",
            anchor="e",
        ).pack(side="right", padx=20, fill="y")

    # ── Notebook / tabs ──────────────────────────────────────────────────────
    def _build_notebook(self):
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[16, 6])

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=16, pady=16)

        self._build_faq_tab(nb)
        self._build_ticket_tab(nb)
        self._build_contact_tab(nb)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 – FAQ
    # ══════════════════════════════════════════════════════════════════════════
    def _build_faq_tab(self, nb: ttk.Notebook):
        frame = tk.Frame(nb, bg="#f0f4f8")
        nb.add(frame, text="  FAQ  ")

        tk.Label(
            frame,
            text="Frequently Asked Questions",
            font=("Arial", 14, "bold"),
            bg="#f0f4f8",
            fg="#003366",
        ).pack(anchor="w", padx=20, pady=(16, 8))

        canvas = tk.Canvas(frame, bg="#f0f4f8", highlightthickness=0)
        sb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#f0f4f8")
        canvas_win = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_resize(e):
            canvas.itemconfig(canvas_win, width=e.width)

        canvas.bind("<Configure>", _on_resize)
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        faqs = [
            ("How do I register a new student?",
             "Go to Student Details → click 'Add Student'. Fill in the form and click Save. "
             "The system will create a record in the database automatically."),
            ("How do I capture face data?",
             "Open Face Detection. Select the student from the dropdown and click 'Generate Data Set'. "
             "The webcam will capture 100 sample images. Make sure the student faces the camera clearly."),
            ("How do I train the model?",
             "After capturing face data for all students, go to Train Data and click 'Train'. "
             "Training may take a few minutes depending on the number of students."),
            ("How is attendance marked?",
             "Open Attendance → click 'Take Attendance'. The system uses the webcam and the trained "
             "model to recognise faces and log attendance automatically with a timestamp."),
            ("What if a face is not recognised?",
             "Ensure the lighting is good and the student is looking at the camera. "
             "If the problem persists, retake face data and re-train the model for that student."),
            ("How do I view weekly attendance?",
             "Click Weekly Progress on the main screen. Select the student and the date range, "
             "then click Generate Report."),
            ("How do I reset a forgotten password?",
             "On the Login screen, enter your email and click 'Forgot Password'. "
             "Answer your security question and verify via the OTP sent to your email."),
            ("Which Python packages are required?",
             "opencv-python, Pillow, mysql-connector-python, bcrypt, face_recognition (dlib), "
             "numpy. Install them with: pip install opencv-python Pillow mysql-connector-python "
             "bcrypt face_recognition numpy"),
        ]

        self._faq_states: list[bool] = []

        for i, (q, a) in enumerate(faqs):
            self._faq_states.append(False)
            self._add_faq_item(inner, i, q, a)

    def _add_faq_item(self, parent, idx, question, answer):
        card = tk.Frame(parent, bg="white", bd=0, relief="flat",
                        highlightbackground="#d0dcea", highlightthickness=1)
        card.pack(fill="x", padx=20, pady=6, ipady=2)

        # Question row (acts as toggle)
        q_frame = tk.Frame(card, bg="white")
        q_frame.pack(fill="x")

        arrow_var = tk.StringVar(value="▶")
        arrow_lbl = tk.Label(q_frame, textvariable=arrow_var,
                             bg="white", fg="#003366",
                             font=("Arial", 10), width=2)
        arrow_lbl.pack(side="left", padx=(10, 0), pady=10)

        q_lbl = tk.Label(q_frame, text=question,
                         bg="white", fg="#003366",
                         font=("Arial", 11, "bold"),
                         anchor="w", cursor="hand2", wraplength=700, justify="left")
        q_lbl.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        # Answer (hidden by default)
        a_frame = tk.Frame(card, bg="#f7f9fc")
        a_lbl = tk.Label(a_frame, text=answer,
                         bg="#f7f9fc", fg="#333",
                         font=("Arial", 10),
                         anchor="w", wraplength=700, justify="left")
        a_lbl.pack(anchor="w", padx=20, pady=10)

        def toggle(_event=None):
            if self._faq_states[idx]:
                a_frame.pack_forget()
                arrow_var.set("▶")
                self._faq_states[idx] = False
            else:
                a_frame.pack(fill="x")
                arrow_var.set("▼")
                self._faq_states[idx] = True

        for w in (q_frame, q_lbl, arrow_lbl):
            w.bind("<Button-1>", toggle)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 – Submit Ticket
    # ══════════════════════════════════════════════════════════════════════════
    def _build_ticket_tab(self, nb: ttk.Notebook):
        frame = tk.Frame(nb, bg="#f0f4f8")
        nb.add(frame, text="  Submit Ticket  ")

        tk.Label(
            frame,
            text="Submit a Support Ticket",
            font=("Arial", 14, "bold"),
            bg="#f0f4f8",
            fg="#003366",
        ).pack(anchor="w", padx=30, pady=(20, 4))

        tk.Label(
            frame,
            text="Describe your issue below and we will get back to you.",
            font=("Arial", 10),
            bg="#f0f4f8",
            fg="#555",
        ).pack(anchor="w", padx=30, pady=(0, 16))

        form = tk.Frame(frame, bg="#f0f4f8")
        form.pack(fill="both", expand=True, padx=30)
        form.columnconfigure(1, weight=1)

        def lbl(text, row):
            tk.Label(form, text=text, font=("Arial", 11, "bold"),
                     bg="#f0f4f8", fg="#333", anchor="w").grid(
                row=row, column=0, sticky="w", pady=8, padx=(0, 16))

        # Name
        lbl("Your Name", 0)
        self.var_name = tk.StringVar()
        ttk.Entry(form, textvariable=self.var_name, font=("Arial", 11)).grid(
            row=0, column=1, sticky="ew", pady=8)

        # Email
        lbl("Email", 1)
        self.var_ticket_email = tk.StringVar()
        ttk.Entry(form, textvariable=self.var_ticket_email, font=("Arial", 11)).grid(
            row=1, column=1, sticky="ew", pady=8)

        # Category
        lbl("Category", 2)
        self.var_category = tk.StringVar()
        cat_combo = ttk.Combobox(form, textvariable=self.var_category,
                                 state="readonly", font=("Arial", 11))
        cat_combo["values"] = (
            "Login / Registration Issue",
            "Face Detection Problem",
            "Attendance Not Marking",
            "Training Error",
            "Database / Connection Error",
            "Other",
        )
        cat_combo.current(0)
        cat_combo.grid(row=2, column=1, sticky="ew", pady=8)

        # Priority
        lbl("Priority", 3)
        self.var_priority = tk.StringVar(value="Medium")
        prio_frame = tk.Frame(form, bg="#f0f4f8")
        prio_frame.grid(row=3, column=1, sticky="w", pady=8)
        for p, color in [("Low", "#27ae60"), ("Medium", "#e67e22"), ("High", "#e74c3c")]:
            tk.Radiobutton(prio_frame, text=p, variable=self.var_priority, value=p,
                           bg="#f0f4f8", fg=color, font=("Arial", 10, "bold"),
                           activebackground="#f0f4f8").pack(side="left", padx=10)

        # Description
        lbl("Description", 4)
        self.txt_desc = tk.Text(form, font=("Arial", 10), height=6,
                                relief="solid", bd=1, wrap="word")
        self.txt_desc.grid(row=4, column=1, sticky="ew", pady=8)

        # Submit
        tk.Button(
            form,
            text="Submit Ticket",
            command=self._submit_ticket,
            font=("Arial", 12, "bold"),
            bg="#003366",
            fg="white",
            cursor="hand2",
            relief="flat",
            padx=20,
            pady=6,
        ).grid(row=5, column=1, sticky="e", pady=16)

    def _submit_ticket(self):
        name = self.var_name.get().strip()
        email = self.var_ticket_email.get().strip()
        desc = self.txt_desc.get("1.0", "end").strip()

        if not name or not email or not desc:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO help_tickets (name, email, category, priority, description, submitted_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                name,
                email,
                self.var_category.get(),
                self.var_priority.get(),
                desc,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Ticket Submitted",
                f"Your ticket has been submitted!\n\nWe'll reach out to {email} shortly.",
            )
            # Clear form
            self.var_name.set("")
            self.var_ticket_email.set("")
            self.txt_desc.delete("1.0", "end")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 – Contact
    # ══════════════════════════════════════════════════════════════════════════
    def _build_contact_tab(self, nb: ttk.Notebook):
        frame = tk.Frame(nb, bg="#f0f4f8")
        nb.add(frame, text="  Contact  ")

        tk.Label(
            frame,
            text="Contact & Support",
            font=("Arial", 14, "bold"),
            bg="#f0f4f8",
            fg="#003366",
        ).pack(anchor="w", padx=30, pady=(20, 16))

        contacts = [
            ("Technical Support", "tech.support@lab.local",
             "Mon–Fri, 9 AM – 5 PM"),
            ("System Administrator", "admin@lab.local",
             "For database / server issues"),
            ("Project Developer", "wasid@lab.local",
             "Bug reports & feature requests"),
        ]

        for title, email, note in contacts:
            card = tk.Frame(frame, bg="white",
                            highlightbackground="#d0dcea", highlightthickness=1)
            card.pack(fill="x", padx=30, pady=8, ipady=6)

            tk.Label(card, text=title, font=("Arial", 12, "bold"),
                     bg="white", fg="#003366", anchor="w").pack(
                anchor="w", padx=16, pady=(10, 2))

            email_lbl = tk.Label(card, text=f"  {email}",
                                 font=("Arial", 10), bg="white",
                                 fg="#1a73e8", cursor="hand2", anchor="w")
            email_lbl.pack(anchor="w", padx=16)
            email_lbl.bind("<Button-1>", lambda e, em=email:
                           webbrowser.open(f"mailto:{em}"))

            tk.Label(card, text=f"  {note}", font=("Arial", 9),
                     bg="white", fg="#777", anchor="w").pack(
                anchor="w", padx=16, pady=(2, 8))

        # Quick-tip box
        tip = tk.Frame(frame, bg="#e8f4fd",
                       highlightbackground="#90caf9", highlightthickness=1)
        tip.pack(fill="x", padx=30, pady=20, ipady=8)

        tk.Label(tip, text="Tip", font=("Arial", 11, "bold"),
                 bg="#e8f4fd", fg="#0d47a1", anchor="w").pack(
            anchor="w", padx=16, pady=(8, 2))

        tk.Label(
            tip,
            text="Before submitting a ticket, check the FAQ tab — most common issues\n"
                 "are already answered there.",
            font=("Arial", 10),
            bg="#e8f4fd",
            fg="#333",
            anchor="w",
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 8))

    # ══════════════════════════════════════════════════════════════════════════
    # DB – ensure help_tickets table exists
    # ══════════════════════════════════════════════════════════════════════════
    def _ensure_table(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS help_tickets (
                    id            INT AUTO_INCREMENT PRIMARY KEY,
                    name          VARCHAR(100),
                    email         VARCHAR(150),
                    category      VARCHAR(100),
                    priority      VARCHAR(20),
                    description   TEXT,
                    submitted_at  DATETIME
                )
            """)
            conn.commit()
            conn.close()
        except Exception:
            pass   # silently skip if DB not available


# ── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    Help_Desk(root)
    root.mainloop()