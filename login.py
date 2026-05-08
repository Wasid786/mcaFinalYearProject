from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
import bcrypt

from main import Face_recognition_System
from register import Register
from emailOTP import EmailOTPWindow


class Login_Window:

    def __init__(self, root):

        self.root = root
        self.root.title("Login")
        self.root.geometry("1200x700")

        self.var_email = StringVar()
        self.var_pass = StringVar()

        # ================= BACKGROUND =================
        self.bg = ImageTk.PhotoImage(
            file=r"C:\Users\Wasid\OneDrive\Pictures\1858536-green-sea-turtles-maui-hawaii.jpg"
        )
        bg_lbl = Label(self.root, image=self.bg)
        bg_lbl.place(relwidth=1, relheight=1)

        # ================= FRAME =================
        frame = Frame(self.root, bg="black")
        frame.place(relx=0.38, rely=0.2, relwidth=0.25, relheight=0.5)

        Label(
            frame,
            text="Login",
            font=("Arial", 22, "bold"),
            bg="black",
            fg="white",
        ).pack(pady=20)

        # Email
        Label(frame, text="Email", font=("Arial", 12), bg="black", fg="white").pack(
            anchor="w", padx=30
        )
        self.txtuser = ttk.Entry(frame, textvariable=self.var_email, font=("Arial", 12))
        self.txtuser.pack(padx=30, fill=X, pady=10)

        # Password
        Label(frame, text="Password", font=("Arial", 12), bg="black", fg="white").pack(
            anchor="w", padx=30
        )
        self.txtpass = ttk.Entry(
            frame, textvariable=self.var_pass, show="*", font=("Arial", 12)
        )
        self.txtpass.pack(padx=30, fill=X, pady=10)

        # Login Button
        Button(
            frame,
            text="Login",
            command=self.login,
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
        ).pack(pady=20)

        # Register Button
        Button(
            frame,
            text="Register",
            command=self.register_window,
            bg="blue",
            fg="white",
        ).pack(pady=10)

        # Forgot Password
        Button(
            frame,
            text="Forgot Password",
            command=self.forget_password_window,
            bg="black",
            fg="white",
            borderwidth=0,
        ).pack()

    # ================= LOGIN =================
    def login(self):
        email = self.var_email.get().strip()
        password = self.var_pass.get()

        if not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Wasid@5284mysql",
                database="register",
            )
            cursor = conn.cursor()

            # Fetch the stored bcrypt hash by email only (never compare password in SQL)
            cursor.execute(
                "SELECT password FROM register WHERE email=%s", (email,)
            )
            row = cursor.fetchone()
            conn.close()

            if row is None:
                messagebox.showerror("Error", "Invalid Email or Password")
                return

            stored_hash = row[0].encode("utf-8") # type: ignore

            # bcrypt comparison — safe against timing attacks
            if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                messagebox.showerror("Error", "Invalid Email or Password")
                return

            # Credentials correct → confirm before opening main window
            if messagebox.askyesno("Access", "Access only for authorised personnel. Continue?"):
                self.new_window = Toplevel(self.root)
                self.app = Face_recognition_System(self.new_window)

        except Exception as es:
            messagebox.showerror("Error", str(es))

    # ================= REGISTER WINDOW =================
    def register_window(self):
        self.new_window = Toplevel(self.root)
        Register(self.new_window)

    # ================= FORGOT PASSWORD =================
    def forget_password_window(self):
        email = self.var_email.get().strip()

        if not email:
            messagebox.showerror("Error", "Please enter your email address first")
            return

        self.root2 = Toplevel(self.root)
        self.root2.title("Forgot Password")
        self.root2.geometry("400x400")

        Label(self.root2, text="Reset Password", font=("Arial", 18, "bold")).pack(pady=20)

        Label(self.root2, text="Security Question").pack()
        self.combo_security_Q = ttk.Combobox(self.root2, state="readonly")
        self.combo_security_Q["values"] = (
            "Select",
            "Your Birth Place",
            "Your Friend Name",
            "Your Pet Name",
        )
        self.combo_security_Q.current(0)
        self.combo_security_Q.pack(pady=10)

        Label(self.root2, text="Security Answer").pack()
        self.txt_security = ttk.Entry(self.root2)
        self.txt_security.pack(pady=10)

        Label(self.root2, text="New Password").pack()
        self.txt_newpass = ttk.Entry(self.root2, show="*")
        self.txt_newpass.pack(pady=10)

        Button(
            self.root2,
            text="Reset Password",
            command=self.reset_pass,
            bg="green",
            fg="white",
        ).pack(pady=20)

    # ================= RESET PASSWORD =================
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
                "Error", "Password must be at least 8 characters.", parent=self.root2
            )
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Wasid@5284mysql",
                database="register",
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

            if row is None:
                messagebox.showerror(
                    "Error", "Incorrect Security Details", parent=self.root2
                )
                conn.close()
                return

            # Send OTP to verify identity before changing password
            conn.close()
            EmailOTPWindow(
                self.root2,
                email=self.var_email.get().strip(),
                on_success=lambda: self._do_password_update(new_password),
            )

        except Exception as es:
            messagebox.showerror("Error", str(es), parent=self.root2)

    def _do_password_update(self, new_password: str):
        """Hash and save the new password after OTP is confirmed."""
        try:
            hashed = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Wasid@5284mysql",
                database="register",
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


if __name__ == "__main__":
    root = Tk()
    app = Login_Window(root)
    root.mainloop()