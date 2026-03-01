from tkinter import *
from PIL import Image, ImageTk

class Student:
    def __init__(self, root):
        self.root = root
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Face recognition Page")

        # Title (full width, fixed height)
        title_lbl = Label(self.root, text="Train Data Set",
                          font=("times new roman", 30, "bold"),
                          bg="white", fg="blue")
        title_lbl.place(relx=0, rely=0, relwidth=1, height=50)

        header_height = int(self.screen_height * 0.4)
        header_width = int(self.screen_width / 2)
    

        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        self.photoimg01 = load_image(r"static\images\img01.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg01).place(x=0, y=46, width=header_width, height=header_height)

        self.photoimg02 = load_image(r"static\images\img02.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg02).place(x=header_width, y=46, width=header_width, height=header_height)


        b1_1 = Button(self.root, text="Train Data", cursor="hand2", font=("times new roman", 30,"bold"), bg="red", fg="white")
        b1_1.place(x=0,y=500, width=2000, height=60)

        self.photoimg03 = load_image(r"static\images\img01.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg03).place(x=0, y=600, width=header_width, height=header_height)

        self.photoimg04 = load_image(r"static\images\img02.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg04).place(x=header_width, y=600, width=header_width, height=header_height)

        










if __name__ == "__main__":
    root = Tk()
    app = Student(root)
    root.mainloop()