from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import bcrypt

from main import Face_recognition_System
from register import Register
from emailOTP import EmailOTPWindow


class Login_Window:

    def __init__(self, root):

        self.root = root
        self.root.title("Login System")
        self.root.state("zoomed")  # start maximized; works on Windows

        # Variables
        self.var_email = StringVar()
        self.var_pass  = StringVar()

        # Store original background so we can re-scale it on resize
        self.original_bg = Image.open(r"static\images\login.jpg")

        # ── Background label (fills the whole window) ──────────────────────
        self.bg_lbl = Label(self.root)
        self.bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # ── Login card frame (centred, fixed minimum) ───────────────────────
        self.frame = Frame(self.root, bg="black", bd=0, highlightthickness=0)
        # We position it with place() in resize_window; just place it now
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # ── Title ───────────────────────────────────────────────────────────
        self.title_lbl = Label(
            self.frame, text="Login",
            font=("Arial", 24, "bold"), bg="black", fg="white",
        )
        self.title_lbl.pack(pady=(20, 30))

        # ── Email ───────────────────────────────────────────────────────────
        self.email_lbl = Label(
            self.frame, text="Email",
            font=("Arial", 13), bg="black", fg="white",
        )
        self.email_lbl.pack(anchor="w", padx=30)

        self.txtuser = ttk.Entry(
            self.frame, textvariable=self.var_email, font=("Arial", 13),
        )
        self.txtuser.pack(fill=X, padx=30, pady=10)

        # ── Password ────────────────────────────────────────────────────────
        self.pass_lbl = Label(
            self.frame, text="Password",
            font=("Arial", 13), bg="black", fg="white",
        )
        self.pass_lbl.pack(anchor="w", padx=30)

        self.txtpass = ttk.Entry(
            self.frame, textvariable=self.var_pass,
            show="*", font=("Arial", 13),
        )
        self.txtpass.pack(fill=X, padx=30, pady=10)

        # ── Login button ────────────────────────────────────────────────────
        self.login_btn = Button(
            self.frame, text="Login", command=self.login,
            bg="#ff3b3b", fg="white",
            activebackground="#ff1f1f", activeforeground="white",
            font=("Arial", 13, "bold"), cursor="hand2",
            relief=FLAT, pady=8,
        )
        self.login_btn.pack(fill=X, padx=30, pady=(25, 10))

        # ── Register button ─────────────────────────────────────────────────
        self.register_btn = Button(
            self.frame, text="Register", command=self.register_window,
            bg="#0066ff", fg="white",
            activebackground="#0052cc", activeforeground="white",
            font=("Arial", 12), cursor="hand2",
            relief=FLAT, pady=8,
        )
        self.register_btn.pack(fill=X, padx=30, pady=10)

        # ── Forgot password ─────────────────────────────────────────────────
        self.forgot_btn = Button(
            self.frame, text="Forgot Password?",
            command=self.forget_password_window,
            bg="black", fg="white",
            activebackground="black", activeforeground="white",
            borderwidth=0, font=("Arial", 11), cursor="hand2",
        )
        self.forgot_btn.pack(pady=(10, 20))

        # ── Bind resize ────────────────────────────────────────────────────
        self.root.bind("<Configure>", self.resize_window)
        self.root.update_idletasks()
        self.resize_window()

    # ────────────────────────────────────────────────────────────────────────
    # RESPONSIVE RESIZE
    # ────────────────────────────────────────────────────────────────────────
    def resize_window(self, event=None):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w < 2 or h < 2:
            return  # window not ready yet

        # Re-scale background to fill the whole window
        resized_bg = self.original_bg.resize((w, h), Image.Resampling.LANCZOS)
        self.bg = ImageTk.PhotoImage(resized_bg)
        self.bg_lbl.config(image=self.bg)

        # Card frame: 38 % of window width, 60 % of height, with a minimum
        frame_w = max(420, int(w * 0.38))
        frame_h = max(400, int(h * 0.60))
        self.frame.config(width=frame_w, height=frame_h)

        # Scale fonts proportionally
        title_size = max(18, int(w * 0.020))
        label_size = max(11, int(w * 0.010))
        btn_size   = max(11, int(w * 0.009))

        self.title_lbl.config(font=("Arial", title_size, "bold"))
        self.email_lbl.config(font=("Arial", label_size))
        self.pass_lbl.config(font=("Arial", label_size))
        self.txtuser.config(font=("Arial", label_size))
        self.txtpass.config(font=("Arial", label_size))
        self.login_btn.config(font=("Arial", btn_size, "bold"))
        self.register_btn.config(font=("Arial", btn_size))
        self.forgot_btn.config(font=("Arial", max(10, btn_size - 1)))

    # ────────────────────────────────────────────────────────────────────────
    # LOGIN
    # ────────────────────────────────────────────────────────────────────────
    def login(self):
        email    = self.var_email.get().strip()
        password = self.var_pass.get()

        if not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="Wasid@5284mysql", database="register",
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM register WHERE email=%s", (email,)
            )
            row = conn.close() or cursor.fetchone()  # close before checking
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="Wasid@5284mysql", database="register",
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM register WHERE email=%s", (email,)
            )
            row = cursor.fetchone()
            conn.close()

            if row is None:
                messagebox.showerror("Error", "Invalid Email or Password")
                return

            stored_hash = row[0].encode("utf-8")  # type: ignore

            if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                messagebox.showerror("Error", "Invalid Email or Password")
                return

            if messagebox.askyesno(
                "Access", "Access only for authorised personnel.\nContinue?"
            ):
                self.new_window = Toplevel(self.root)
                self.app = Face_recognition_System(self.new_window)

        except Exception as es:
            messagebox.showerror("Error", str(es))

    # ────────────────────────────────────────────────────────────────────────
    # REGISTER WINDOW
    # ────────────────────────────────────────────────────────────────────────
    def register_window(self):
        self.new_window = Toplevel(self.root)
        Register(self.new_window)

    # ────────────────────────────────────────────────────────────────────────
    # FORGOT PASSWORD WINDOW
    # ────────────────────────────────────────────────────────────────────────
    def forget_password_window(self):
        email = self.var_email.get().strip()
        if not email:
            messagebox.showerror("Error", "Please enter your email first")
            return

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        # Window is 35 % wide, 55 % tall, centred
        win_w = max(420, int(sw * 0.35))
        win_h = max(430, int(sh * 0.55))
        x_pos = (sw - win_w) // 2
        y_pos = (sh - win_h) // 2

        self.root2 = Toplevel(self.root)
        self.root2.title("Forgot Password")
        self.root2.geometry(f"{win_w}x{win_h}+{x_pos}+{y_pos}")
        self.root2.resizable(True, True)

        Label(
            self.root2, text="Reset Password",
            font=("Arial", max(16, int(sw * 0.015)), "bold"),
        ).pack(pady=int(sh * 0.025))

        # Security question
        Label(self.root2, text="Security Question",
              font=("Arial", max(11, int(sw * 0.010)))).pack()

        self.combo_security_Q = ttk.Combobox(
            self.root2, state="readonly",
            font=("Arial", max(10, int(sw * 0.009))),
            width=30,
        )
        self.combo_security_Q["values"] = (
            "Select", "Your Birth Place", "Your Friend Name", "Your Pet Name",
        )
        self.combo_security_Q.current(0)
        self.combo_security_Q.pack(pady=int(sh * 0.012))

        # Security answer
        Label(self.root2, text="Security Answer",
              font=("Arial", max(11, int(sw * 0.010)))).pack()

        self.txt_security = ttk.Entry(
            self.root2, font=("Arial", max(10, int(sw * 0.009))), width=33,
        )
        self.txt_security.pack(pady=int(sh * 0.012))

        # New password
        Label(self.root2, text="New Password",
              font=("Arial", max(11, int(sw * 0.010)))).pack()

        self.txt_newpass = ttk.Entry(
            self.root2, show="*",
            font=("Arial", max(10, int(sw * 0.009))), width=33,
        )
        self.txt_newpass.pack(pady=int(sh * 0.012))

        Button(
            self.root2, text="Reset Password", command=self.reset_pass,
            bg="green", fg="white",
            font=("Arial", max(11, int(sw * 0.009)), "bold"),
            cursor="hand2", relief=FLAT, pady=8,
        ).pack(pady=int(sh * 0.030))

    # ────────────────────────────────────────────────────────────────────────
    # RESET PASSWORD
    # ────────────────────────────────────────────────────────────────────────
    def reset_pass(self):
        if self.combo_security_Q.get() == "Select":
            messagebox.showerror("Error", "Select Security Question", parent=self.root2)
            return
        if not self.txt_security.get():
            messagebox.showerror("Error", "Enter Security Answer", parent=self.root2)
            return

        new_password = self.txt_newpass.get()
        if not new_password:
            messagebox.showerror("Error", "Enter New Password", parent=self.root2)
            return
        if len(new_password) < 8:
            messagebox.showerror(
                "Error", "Password must be at least 8 characters", parent=self.root2
            )
            return

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="Wasid@5284mysql", database="register",
            )
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM register
                WHERE email=%s AND securityQ=%s AND securityA=%s
                """,
                (
                    self.var_email.get().strip(),
                    self.combo_security_Q.get(),
                    self.txt_security.get(),
                ),
            )
            row = cursor.fetchone()
            conn.close()

            if row is None:
                messagebox.showerror(
                    "Error", "Incorrect Security Details", parent=self.root2
                )
                return

            EmailOTPWindow(
                self.root2,
                email=self.var_email.get().strip(),
                on_success=lambda: self._do_password_update(new_password),
            )

        except Exception as es:
            messagebox.showerror("Error", str(es), parent=self.root2)

    # ────────────────────────────────────────────────────────────────────────
    # UPDATE PASSWORD
    # ────────────────────────────────────────────────────────────────────────
    def _do_password_update(self, new_password):
        try:
            hashed = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="Wasid@5284mysql", database="register",
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE register SET password=%s WHERE email=%s",
                (hashed, self.var_email.get().strip()),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Password updated successfully!")
            self.root2.destroy()

        except Exception as es:
            messagebox.showerror("Error", str(es))


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    app  = Login_Window(root)
    root.mainloop()