from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class Student:
    def __init__(self, root):
        self.root = root

        # Get screen size dynamically
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Student Info Page")

        # Header image size (divide screen into 3 parts)
        header_height = int(self.screen_height * 0.15)
        header_width = int(self.screen_width / 3)

        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        # Top 3 images
        self.photoimg01 = load_image(r"D:\Projects\mcaProject\static\images\img01.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg01).place(x=0, y=0, width=header_width, height=header_height)

        self.photoimg02 = load_image(r"D:\Projects\mcaProject\static\images\img02.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg02).place(x=header_width, y=0, width=header_width, height=header_height)

        self.photoimg03 = load_image(r"D:\Projects\mcaProject\static\images\img03.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg03).place(x=header_width*2, y=0, width=header_width, height=header_height)

        # Background image
        bg_height = self.screen_height - header_height
        self.photobg_image = load_image(r"D:\Projects\mcaProject\static\images\img04.jpg", self.screen_width, bg_height)
        bg_img = Label(self.root, image=self.photobg_image)
        bg_img.place(x=0, y=header_height, width=self.screen_width, height=bg_height)

        # Title
        Label(bg_img, text="Student Management System",
              font=("times new roman", int(self.screen_width*0.02), "bold"),
              bg="white", fg="blue").place(x=0, y=0, width=self.screen_width, height=50)



if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()