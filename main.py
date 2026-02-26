from tkinter import *
from PIL import Image, ImageTk

class Face_recognition_System:
    def __init__(self, root):
        self.root = root
        self.images = []  # store all images

        # Get screen size dynamically
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.title("Face Recognition System")

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
        Label(bg_img, text="Lab Attendance System",
              font=("times new roman", int(self.screen_width*0.02), "bold"),
              bg="white", fg="red").place(x=0, y=0, width=self.screen_width, height=50)

        #  Button size relative
        btn_w = int(self.screen_width * 0.12)
        btn_h = int(self.screen_height * 0.20)

        x_positions = [
            int(self.screen_width * 0.13),
            int(self.screen_width * 0.32),
            int(self.screen_width * 0.52),
            int(self.screen_width * 0.72),
        ]

        y_top = int(self.screen_height * 0.2)
        y_bottom = int(self.screen_height * 0.55)

        def create_button(img_path, text, x, y):
           img = load_image(img_path, btn_w, btn_h)
           self.images.append(img) 

           btn = Button(bg_img, image=img, cursor="hand2")
           btn.place(x=x, y=y, width=btn_w, height=btn_h)

           Button(bg_img, text=text, cursor="hand2",
           font=("times new roman", 14, "bold"),
           bg="darkblue", fg="white").place(
          x=x, y=y + btn_h, width=btn_w, height=40
    )

        # Row 1
        create_button(r"D:\Projects\mcaProject\static\images\img05.jpg", "Student Details", x_positions[0], y_top)
        create_button(r"D:\Projects\mcaProject\static\images\img06.jpg", "Face Detection", x_positions[1], y_top)
        create_button(r"D:\Projects\mcaProject\static\images\img07.png", "Attendance", x_positions[2], y_top)
        create_button(r"D:\Projects\mcaProject\static\images\img08.jpg", "Help Desk", x_positions[3], y_top)

        # Row 2
        create_button(r"D:\Projects\mcaProject\static\images\img09.jpg", "Train Data", x_positions[0], y_bottom)
        create_button(r"D:\Projects\mcaProject\static\images\img10.jpg", "Photos", x_positions[1], y_bottom)
        create_button(r"D:\Projects\mcaProject\static\images\img11.png", "Developer", x_positions[2], y_bottom)
        create_button(r"D:\Projects\mcaProject\static\images\img12.jpg", "Exit", x_positions[3], y_bottom)


if __name__ == "__main__":
    root = Tk()
    obj = Face_recognition_System(root)
    root.mainloop()














