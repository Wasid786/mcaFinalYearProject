from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
from main import Face_Recognition, Face_recognition_System
from register import Register


class Login_Window:

    def __init__(self, root):

        self.root = root
        self.root.title("Login")
        self.root.geometry("1200x700")

        self.var_email = StringVar()
        self.var_pass = StringVar()

        # Background
        self.bg = ImageTk.PhotoImage(
            file=r"C:\Users\Wasid\OneDrive\Pictures\1858536-green-sea-turtles-maui-hawaii.jpg"
        )

        bg_lbl = Label(self.root, image=self.bg)
        bg_lbl.place(relwidth=1, relheight=1)

        # Frame
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
        Label(
            frame,
            text="Email",
            font=("Arial", 12),
            bg="black",
            fg="white",
        ).pack(anchor="w", padx=30)

        self.txtuser = ttk.Entry(
            frame,
            textvariable=self.var_email,
            font=("Arial", 12),
        )

        self.txtuser.pack(padx=30, fill=X, pady=10)

        # Password
        Label(
            frame,
            text="Password",
            font=("Arial", 12),
            bg="black",
            fg="white",
        ).pack(anchor="w", padx=30)

        self.txtpass = ttk.Entry(
            frame,
            textvariable=self.var_pass,
            show="*",
            font=("Arial", 12),
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

        if (
            self.var_email.get() == ""
            or self.var_pass.get() == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required",
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

            query = """
            SELECT * FROM register
            WHERE email=%s AND password=%s
            """

            values = (
                self.var_email.get(),
                self.var_pass.get(),
            )

            cursor.execute(query, values)

            row = cursor.fetchone()

            if row is None:
                messagebox.showerror(
                    "Error",
                    "Invalid Email or Password",
                )
            else:
                open_main=messagebox.askyesno("YesNo","Access only Authority Person")
                if open_main >0:
                    self.new_window=Toplevel(self.root)
                    self.app = Face_recognition_System(self.new_window)
                else:
                    if not open_main:
                        return
                
                

            # conn.close()

        except Exception as es:
            messagebox.showerror(
                "Error",
                f"{str(es)}",
            )

    # ================= REGISTER WINDOW =================
    def register_window(self):

        self.new_window = Toplevel(self.root)
        Register(self.new_window)

    # ================= FORGOT PASSWORD =================
    def forget_password_window(self):

        if self.var_email.get() == "":
            messagebox.showerror(
                "Error",
                "Please enter email address",
            )
            return

        self.root2 = Toplevel(self.root)
        self.root2.title("Forgot Password")
        self.root2.geometry("400x400")

        Label(
            self.root2,
            text="Reset Password",
            font=("Arial", 18, "bold"),
        ).pack(pady=20)

        # Security Question
        Label(
            self.root2,
            text="Security Question",
        ).pack()

        self.combo_security_Q = ttk.Combobox(
            self.root2,
            state="readonly",
        )

        self.combo_security_Q["values"] = (
            "Select",
            "Your Birth Place",
            "Your Friend Name",
            "Your Pet Name",
        )

        self.combo_security_Q.current(0)
        self.combo_security_Q.pack(pady=10)

        # Answer
        Label(
            self.root2,
            text="Security Answer",
        ).pack()

        self.txt_security = ttk.Entry(self.root2)
        self.txt_security.pack(pady=10)

        # New Password
        Label(
            self.root2,
            text="New Password",
        ).pack()

        self.txt_newpass = ttk.Entry(
            self.root2,
            show="*",
        )

        self.txt_newpass.pack(pady=10)

        # Reset Button
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
            messagebox.showerror(
                "Error",
                "Select Security Question",
                parent=self.root2,
            )

            return

        if self.txt_security.get() == "":
            messagebox.showerror(
                "Error",
                "Enter Security Answer",
                parent=self.root2,
            )

            return

        if self.txt_newpass.get() == "":
            messagebox.showerror(
                "Error",
                "Enter New Password",
                parent=self.root2,
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

            query = """
            SELECT * FROM register
            WHERE email=%s
            AND securityQ=%s
            AND securityA=%s
            """

            values = (
                self.var_email.get(),
                self.combo_security_Q.get(),
                self.txt_security.get(),
            )

            cursor.execute(query, values)

            row = cursor.fetchone()

            if row is None:
                messagebox.showerror(
                    "Error",
                    "Incorrect Security Details",
                    parent=self.root2,
                )

            else:

                update_query = """
                UPDATE register
                SET password=%s
                WHERE email=%s
                """

                update_values = (
                    self.txt_newpass.get(),
                    self.var_email.get(),
                )

                cursor.execute(
                    update_query,
                    update_values,
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Password Updated Successfully",
                    parent=self.root2,
                )

                self.root2.destroy()

            conn.close()

        except Exception as es:
            messagebox.showerror(
                "Error",
                f"{str(es)}",
                parent=self.root2,
            )


if __name__ == "__main__":

    root = Tk()
    app = Login_Window(root)
    root.mainloop()