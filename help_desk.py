import tkinter as tk
from tkinter import ttk


class Help_Desk:
    def __init__(self, root: tk.Toplevel | tk.Tk):
        self.root = root
        self.root.title("Help Desk")
        self.root.state("zoomed")
        self.root.minsize(700, 500)
        self.root.configure(bg="#f0f4f8")

        self._build_header()
        self._build_faq()

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

    # ── FAQ ──────────────────────────────────────────────────────────────────
    def _build_faq(self):
        tk.Label(
            self.root,
            text="Frequently Asked Questions",
            font=("Arial", 14, "bold"),
            bg="#f0f4f8",
            fg="#003366",
        ).pack(anchor="w", padx=24, pady=(16, 8))

        # Scrollable canvas
        canvas = tk.Canvas(self.root, bg="#f0f4f8", highlightthickness=0)
        sb = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#f0f4f8")
        win = canvas.create_window((0, 0), window=inner, anchor="nw")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
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
             "numpy. Install them with:  pip install opencv-python Pillow mysql-connector-python "
             "bcrypt face_recognition numpy"),
        ]

        self._faq_states: list[bool] = []
        for i, (q, a) in enumerate(faqs):
            self._faq_states.append(False)
            self._add_faq_item(inner, i, q, a)

    def _add_faq_item(self, parent, idx, question, answer):
        card = tk.Frame(parent, bg="white", bd=0, relief="flat",
                        highlightbackground="#d0dcea", highlightthickness=1)
        card.pack(fill="x", padx=24, pady=6, ipady=2)

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
                         anchor="w", cursor="hand2",
                         wraplength=900, justify="left")
        q_lbl.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        a_frame = tk.Frame(card, bg="#f7f9fc")
        tk.Label(a_frame, text=answer,
                 bg="#f7f9fc", fg="#333",
                 font=("Arial", 10),
                 anchor="w", wraplength=900, justify="left").pack(
            anchor="w", padx=20, pady=10)

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


# ── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    Help_Desk(root)
    root.mainloop()