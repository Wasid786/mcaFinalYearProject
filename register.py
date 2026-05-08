import tkinter as tk
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
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)

        # ================= VARIABLES =================
        self.var_fname = tk.StringVar()
        self.var_lname = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_securityQ = tk.StringVar()
        self.var_securityA = tk.StringVar()
        self.var_pass = tk.StringVar()
        self.var_confpass = tk.StringVar()
        self.var_check = tk.IntVar()

        # ================= BACKGROUND IMAGE =================
        bg_img = Image.open(
            r"C:\Users\Wasid\OneDrive\Pictures\1858536-green-sea-turtles-maui-hawaii.jpg"
        )
        bg_img = bg_img.resize((1600, 900))
        self.bg = ImageTk.PhotoImage(bg_img)

        bg_lbl = tk.Label(self.root, image=self.bg)
        bg_lbl.place(relwidth=1, relheight=1)

        # ================= MAIN FRAME =================
        frame = tk.Frame(self.root, bg="white")
        frame.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.8)

        # ================= TITLE =================
        tk.Label(
            frame,
            text="Register Here",
            font=("Times New Roman", 24, "bold"),
            bg="white",
            fg="green",
        ).pack(pady=20)

        # ================= FORM FRAME =================
        form_frame = tk.Frame(frame, bg="white")
        form_frame.pack(fill="both", expand=True, padx=40)

        # ================= LABEL + ENTRY HELPER =================
        def create_field(label_text, text_var, row, show=None):
            tk.Label(
                form_frame,
                text=label_text,
                font=("Arial", 12, "bold"),
                bg="white",
            ).grid(row=row, column=0, sticky="w", pady=10)

            entry = ttk.Entry(
                form_frame,
                textvariable=text_var,
                font=("Arial", 12),
                show=show,  # type: ignore
            )
            entry.grid(row=row, column=1, pady=10, padx=20, sticky="ew")

        form_frame.columnconfigure(1, weight=1)

        # ================= FIELDS =================
        create_field("First Name", self.var_fname, 0)
        create_field("Last Name", self.var_lname, 1)
        create_field("Contact", self.var_contact, 2)
        create_field("Email", self.var_email, 3)

        # Security Question
        tk.Label(
            form_frame,
            text="Security Question",
            font=("Arial", 12, "bold"),
            bg="white",
        ).grid(row=4, column=0, sticky="w", pady=10)

        self.combo_security_Q = ttk.Combobox(
            form_frame,
            textvariable=self.var_securityQ,
            state="readonly",
            font=("Arial", 12),
        )
        self.combo_security_Q["values"] = (
            "Select",
            "Your Birth Place",
            "Your Friend Name",
            "Your Pet Name",
        )
        self.combo_security_Q.current(0)
        self.combo_security_Q.grid(row=4, column=1, sticky="ew", pady=10, padx=20)

        create_field("Security Answer", self.var_securityA, 5)
        create_field("Password", self.var_pass, 6, show="*")
        create_field("Confirm Password", self.var_confpass, 7, show="*")

        # Password strength hint
        self.strength_lbl = tk.Label(
            form_frame,
            text="",
            font=("Arial", 9),
            bg="white",
        )
        self.strength_lbl.grid(row=8, column=1, sticky="w", padx=20)
        self.var_pass.trace_add("write", self._update_strength)

        # ================= CHECKBOX =================
        tk.Checkbutton(
            form_frame,
            text="I Agree to the Terms & Conditions",
            variable=self.var_check,
            bg="white",
            font=("Arial", 11),
        ).grid(row=9, columnspan=2, pady=15)

        # ================= BUTTONS =================
        tk.Button(
            form_frame,
            text="Register",
            command=self.register_data,
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            cursor="hand2",
        ).grid(row=10, column=0, pady=20, sticky="ew")

        tk.Button(
            form_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2",
        ).grid(row=10, column=1, pady=20, padx=20, sticky="ew")

    # ================= PASSWORD STRENGTH =================
    def _update_strength(self, *_):
        pwd = self.var_pass.get()
        score = 0
        hints = []

        if len(pwd) >= 8:
            score += 1
        else:
            hints.append("8+ chars")

        if any(c.isupper() for c in pwd):
            score += 1
        else:
            hints.append("uppercase")

        if any(c.islower() for c in pwd):
            score += 1
        else:
            hints.append("lowercase")

        if any(c.isdigit() for c in pwd):
            score += 1
        else:
            hints.append("digit")

        if any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in pwd):
            score += 1
        else:
            hints.append("special char")

        labels = {1: ("Weak", "red"), 2: ("Fair", "orange"),
                  3: ("Moderate", "#e6a817"), 4: ("Strong", "blue"),
                  5: ("Very Strong", "green")}

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

    # ================= VALIDATION =================
    def _validate(self) -> bool:
        """Returns True if all fields pass validation."""
        if (
            self.var_fname.get() == ""
            or self.var_email.get() == ""
            or self.var_securityA.get() == ""
            or self.var_securityQ.get() == "Select"
        ):
            messagebox.showerror("Error", "All fields are required!")
            return False

        if "@" not in self.var_email.get() or "." not in self.var_email.get():
            messagebox.showerror("Error", "Enter a valid email address.")
            return False

        if self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror(
                "Error", "Password and Confirm Password must match."
            )
            return False

        if len(self.var_pass.get()) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters.")
            return False

        if self.var_check.get() == 0:
            messagebox.showerror("Error", "Please agree to Terms & Conditions.")
            return False

        return True

    # ================= REGISTER =================
    def register_data(self):
        if not self._validate():
            return

        # Check if email already exists before sending OTP
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Wasid@5284mysql",   # ← your password
                database="register",
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM register WHERE email=%s", (self.var_email.get(),))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Email already registered. Try another.")
                conn.close()
                return
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        # Launch OTP window; on success → save to DB
        EmailOTPWindow(
            self.root,
            email=self.var_email.get(),
            on_success=self._save_to_db,
        )

    # ================= SAVE (called after OTP verified) =================
    def _save_to_db(self):
        try:
            # Hash password with bcrypt
            hashed = bcrypt.hashpw(
                self.var_pass.get().encode("utf-8"),
                bcrypt.gensalt(),
            ).decode("utf-8")

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Wasid@5284mysql",   # ← your password
                database="register",
            )
            cursor = conn.cursor()

            insert_query = """
            INSERT INTO register
            (fname, lname, contact, email, securityQ, securityA, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                self.var_fname.get(),
                self.var_lname.get(),
                self.var_contact.get(),
                self.var_email.get(),
                self.var_securityQ.get(),
                self.var_securityA.get(),
                hashed,                       # ← bcrypt hash stored, NOT plain text
            )

            cursor.execute(insert_query, values)
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Registered Successfully!")
            #close registration window
            self.root.destroy()

            #open face recogintion window
            new_root = tk.Tk()
            app =  Face_recognition_System(new_root)
            new_root.mainloop()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")


# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = Register(root)
    root.mainloop()