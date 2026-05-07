from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
import cv2
from time import strftime
from datetime import datetime


class Developer:
    def __init__(self, root):
        self.root = root
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Developer page")


        # Title (full width, fixed height)
        title_lbl = Label(self.root, text="Train Data Set",
                          font=("times new roman", 30, "bold"),
                          bg="white", fg="blue")
        title_lbl.place(relx=0, rely=0, relwidth=1, height=50)

        # header_height = int(self.screen_height * 0.4)
        header_width = int(self.screen_width / 2)

        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
    

        bg_height = self.screen_height - 50

        self.photobg_image = load_image(
    r"static\images\img04.jpg",
    self.screen_width,
    bg_height
)

        bg_img = Label(self.root, image=self.photobg_image)

        bg_img.place(
    x=0,
    y=50,
    width=self.screen_width,
    height=bg_height
)
    







if __name__ == "__main__":
    root = Tk()
    app = Developer(root)
    root.mainloop()