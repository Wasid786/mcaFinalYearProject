import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import bcrypt
from emailOTP import EmailOTPWindow
from main import Face_recognition_System


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.state("zoomed")  # start maximised

        # ── StringVars ──────────────────────────────────────────────────────
        self.var_fname     = tk.StringVar()
        self.var_lname     = tk.StringVar()
        self.var_contact   = tk.StringVar()
        self.var_email     = tk.StringVar()
        self.var_securityQ = tk.StringVar()
        self.var_securityA = tk.StringVar()
        self.var_pass      = tk.StringVar()
        self.var_confpass  = tk.StringVar()
        self.var_check     = tk.IntVar()

        # ── Background: store original so it can be re-scaled ───────────────
        self.original_bg = Image.open(r"static\images\register.jpg")

        self.bg_lbl = tk.Label(self.root)
        self.bg_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ── Main card frame (centred) ────────────────────────────────────────
        self.frame = tk.Frame(self.root, bg="white")
        # relwidth / relheight make it proportional to window; anchored at centre
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER,
                         relwidth=0.52, relheight=0.82)

        # ── Title ────────────────────────────────────────────────────────────
        self.title_lbl = tk.Label(
            self.frame, text="Register Here",
            font=("Times New Roman", 24, "bold"),
            bg="white", fg="green",
        )
        self.title_lbl.pack(pady=16)

        # ── Scrollable form area ─────────────────────────────────────────────
        # Using a canvas + inner frame so the form scrolls on very small screens
        canvas = tk.Canvas(self.frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.form_frame = tk.Frame(canvas, bg="white")
        self.form_window = canvas.create_window((0, 0), window=self.form_frame, anchor="nw")

        # Make the canvas window stretch to canvas width
        def _on_canvas_configure(event):
            canvas.itemconfig(self.form_window, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)
        self.form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Mouse-wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ── Column weight so entries expand ──────────────────────────────────
        self.form_frame.columnconfigure(1, weight=1)

        # ── Helper: create a label + entry row ───────────────────────────────
        def create_field(label_text, text_var, row, show=None):
            tk.Label(
                self.form_frame, text=label_text,
                font=("Arial", 12, "bold"), bg="white",
            ).grid(row=row, column=0, sticky="w", padx=16, pady=8)

            entry = ttk.Entry(
                self.form_frame, textvariable=text_var,
                font=("Arial", 12), show=show,  # type: ignore
            )
            entry.grid(row=row, column=1, sticky="ew", padx=16, pady=8)

        # ── Fields ───────────────────────────────────────────────────────────
        create_field("First Name",    self.var_fname,    0)
        create_field("Last Name",     self.var_lname,    1)
        create_field("Contact",       self.var_contact,  2)
        create_field("Email",         self.var_email,    3)

        tk.Label(
            self.form_frame, text="Security Question",
            font=("Arial", 12, "bold"), bg="white",
        ).grid(row=4, column=0, sticky="w", padx=16, pady=8)

        self.combo_security_Q = ttk.Combobox(
            self.form_frame, textvariable=self.var_securityQ,
            state="readonly", font=("Arial", 12),
        )
        self.combo_security_Q["values"] = (
            "Select", "Your Birth Place", "Your Friend Name", "Your Pet Name",
        )
        self.combo_security_Q.current(0)
        self.combo_security_Q.grid(row=4, column=1, sticky="ew", padx=16, pady=8)

        create_field("Security Answer",  self.var_securityA, 5)
        create_field("Password",         self.var_pass,      6, show="*")
        create_field("Confirm Password", self.var_confpass,  7, show="*")

        # Password strength label
        self.strength_lbl = tk.Label(
            self.form_frame, text="", font=("Arial", 9), bg="white",
        )
        self.strength_lbl.grid(row=8, column=1, sticky="w", padx=16)
        self.var_pass.trace_add("write", self._update_strength)

        # Terms checkbox
        tk.Checkbutton(
            self.form_frame,
            text="I Agree to the Terms & Conditions",
            variable=self.var_check,
            bg="white", font=("Arial", 11),
        ).grid(row=9, columnspan=2, pady=14)

        # Buttons
        tk.Button(
            self.form_frame, text="Register",
            command=self.register_data,
            font=("Arial", 12, "bold"), bg="green", fg="white", cursor="hand2",
        ).grid(row=10, column=0, sticky="ew", padx=16, pady=18)

        tk.Button(
            self.form_frame, text="Login",
            command=self.login_data,
            font=("Arial", 12, "bold"), bg="blue", fg="white", cursor="hand2",
        ).grid(row=10, column=1, sticky="ew", padx=16, pady=18)

        # ── Resize handling ──────────────────────────────────────────────────
        self.root.bind("<Configure>", self._resize)
        self.root.update_idletasks()
        self._resize()

    # ────────────────────────────────────────────────────────────────────────
    # RESIZE
    # ────────────────────────────────────────────────────────────────────────
    def _resize(self, event=None):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w < 2 or h < 2:
            return

        # Re-scale background
        resized = self.original_bg.resize((w, h), Image.Resampling.LANCZOS)
        self._bg_photo = ImageTk.PhotoImage(resized)
        self.bg_lbl.config(image=self._bg_photo)

        # Scale fonts
        title_size = max(16, int(w * 0.018))
        label_size = max(10, int(w * 0.009))

        self.title_lbl.config(font=("Times New Roman", title_size, "bold"))

        # Update all labels + entries inside form_frame
        for widget in self.form_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(font=("Arial", label_size, "bold"))
            elif isinstance(widget, (ttk.Entry, ttk.Combobox)):
                widget.config(font=("Arial", label_size))

        # Strength label gets a smaller font
        self.strength_lbl.config(font=("Arial", max(8, label_size - 2)))

    # ────────────────────────────────────────────────────────────────────────
    # PASSWORD STRENGTH
    # ────────────────────────────────────────────────────────────────────────
    def _update_strength(self, *_):
        pwd   = self.var_pass.get()
        score = 0
        hints = []

        if len(pwd) >= 8:       score += 1
        else:                   hints.append("8+ chars")
        if any(c.isupper() for c in pwd):  score += 1
        else:                   hints.append("uppercase")
        if any(c.islower() for c in pwd):  score += 1
        else:                   hints.append("lowercase")
        if any(c.isdigit() for c in pwd):  score += 1
        else:                   hints.append("digit")
        if any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in pwd):
            score += 1
        else:
            hints.append("special char")

        labels = {
            1: ("Weak",        "red"),
            2: ("Fair",        "orange"),
            3: ("Moderate",    "#e6a817"),
            4: ("Strong",      "blue"),
            5: ("Very Strong", "green"),
        }

        if pwd == "":
            self.strength_lbl.config(text="", fg="black")
        elif score <= 2:
            text, color = labels.get(score, ("Weak", "red"))
            self.strength_lbl.config(
                text=f"{text} — add: {', '.join(hints)}", fg=color
            )
        else:
            text, color = labels[score]
            self.strength_lbl.config(text=text, fg=color)

    # ────────────────────────────────────────────────────────────────────────
    # VALIDATION
    # ────────────────────────────────────────────────────────────────────────
    def _validate(self) -> bool:
        if (
            not self.var_fname.get()
            or not self.var_email.get()
            or not self.var_securityA.get()
            or self.var_securityQ.get() == "Select"
        ):
            messagebox.showerror("Error", "All fields are required!")
            return False

        if "@" not in self.var_email.get() or "." not in self.var_email.get():
            messagebox.showerror("Error", "Enter a valid email address.")
            return False

        if self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("Error", "Password and Confirm Password must match.")
            return False

        if len(self.var_pass.get()) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters.")
            return False

        if self.var_check.get() == 0:
            messagebox.showerror("Error", "Please agree to Terms & Conditions.")
            return False

        return True

    # ────────────────────────────────────────────────────────────────────────
    # REGISTER
    # ────────────────────────────────────────────────────────────────────────
    def register_data(self):
        if not self._validate():
            return

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="YOUR_PASSWORD", database="register",
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM register WHERE email=%s", (self.var_email.get(),)
            )
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Email already registered. Try another.")
                conn.close()
                return
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        EmailOTPWindow(
            self.root,
            email=self.var_email.get(),
            on_success=self._save_to_db,
        )

    # ────────────────────────────────────────────────────────────────────────
    # NAVIGATE TO LOGIN
    # ────────────────────────────────────────────────────────────────────────
    def login_data(self):
        from login import Login_Window
        self.root.destroy()
        root = tk.Tk()
        Login_Window(root)
        root.mainloop()

    # ────────────────────────────────────────────────────────────────────────
    # SAVE (called after OTP verified)
    # ────────────────────────────────────────────────────────────────────────
    def _save_to_db(self):
        try:
            hashed = bcrypt.hashpw(
                self.var_pass.get().encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="YOUR_PASSWORD", database="register",
            )
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO register
                (fname, lname, contact, email, securityQ, securityA, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    self.var_fname.get(),
                    self.var_lname.get(),
                    self.var_contact.get(),
                    self.var_email.get(),
                    self.var_securityQ.get(),
                    self.var_securityA.get(),
                    hashed,
                ),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Registered Successfully!")
            self.root.destroy()

            new_root = tk.Tk()
            Face_recognition_System(new_root)
            new_root.mainloop()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    Register(root)
    root.mainloop()