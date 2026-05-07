import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector


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
        title = tk.Label(
            frame,
            text="Register Here",
            font=("Times New Roman", 24, "bold"),
            bg="white",
            fg="green",
        )
        title.pack(pady=20)

        # ================= FORM FRAME =================
        form_frame = tk.Frame(frame, bg="white")
        form_frame.pack(fill="both", expand=True, padx=40)

        # ================= LABEL + ENTRY FUNCTION =================
        def create_field(label_text, text_var, row, show=None):
            label = tk.Label(
                form_frame,
                text=label_text,
                font=("Arial", 12, "bold"),
                bg="white",
            )
            label.grid(row=row, column=0, sticky="w", pady=10)

            entry = ttk.Entry(
                form_frame,
                textvariable=text_var,
                font=("Arial", 12),
                show=show, # type: ignore
            )
            entry.grid(row=row, column=1, pady=10, padx=20, sticky="ew")

        form_frame.columnconfigure(1, weight=1)

        # ================= FIELDS =================
        create_field("First Name", self.var_fname, 0)
        create_field("Last Name", self.var_lname, 1)
        create_field("Contact", self.var_contact, 2)
        create_field("Email", self.var_email, 3)

        # Security Question
        security_lbl = tk.Label(
            form_frame,
            text="Security Question",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        security_lbl.grid(row=4, column=0, sticky="w", pady=10)

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
        self.combo_security_Q.grid(
            row=4, column=1, sticky="ew", pady=10, padx=20
        )

        create_field("Security Answer", self.var_securityA, 5)
        create_field("Password", self.var_pass, 6, show="*")
        create_field("Confirm Password", self.var_confpass, 7, show="*")

        # ================= CHECKBOX =================
        check_btn = tk.Checkbutton(
            form_frame,
            text="I Agree to the Terms & Conditions",
            variable=self.var_check,
            bg="white",
            font=("Arial", 11),
        )

        check_btn.grid(row=8, columnspan=2, pady=15)

        # ================= BUTTONS =================
        register_btn = tk.Button(
            form_frame,
            text="Register",
            command=self.register_data,
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            cursor="hand2",
        )

        register_btn.grid(row=9, column=0, pady=20, sticky="ew")

        login_btn = tk.Button(
            form_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2",
        )

        login_btn.grid(row=9, column=1, pady=20, padx=20, sticky="ew")

    # ================= REGISTER FUNCTION =================
    def register_data(self):

        if (
            self.var_fname.get() == ""
            or self.var_email.get() == ""
            or self.var_securityQ.get() == "Select"
        ):
            messagebox.showerror("Error", "All fields are required!")
            return

        if self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror(
                "Error",
                "Password and Confirm Password must be the same",
            )
            return

        if self.var_check.get() == 0:
            messagebox.showerror(
                "Error",
                "Please agree to Terms & Conditions",
            )
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Test@123",
                database="mydata",
            )

            cursor = conn.cursor()

            query = "SELECT * FROM register WHERE email=%s"
            value = (self.var_email.get(),)

            cursor.execute(query, value)

            row = cursor.fetchone()

            if row is not None:
                messagebox.showerror(
                    "Error",
                    "User already exists. Please try another email.",
                )

            else:
                insert_query = """
                INSERT INTO register
                (fname, lname, contact, email, securityQ, securityA, password)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """

                values = (
                    self.var_fname.get(),
                    self.var_lname.get(),
                    self.var_contact.get(),
                    self.var_email.get(),
                    self.var_securityQ.get(),
                    self.var_securityA.get(),
                    self.var_pass.get(),
                )

                cursor.execute(insert_query, values)

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Registered Successfully!",
                )

            conn.close()

        except Exception as es:
            messagebox.showerror(
                "Database Error",
                f"Error due to: {str(es)}",
            )


# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = Register(root)
    root.mainloop()