from email import message
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os 
import numpy as np
import cv2


class Train:
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


        b1_1 = Button(self.root, text="Train Data",command=self.train_classifier,  cursor="hand2", font=("times new roman", 30,"bold"), bg="red", fg="white")
        b1_1.place(x=0,y=500, width=2000, height=60)

        self.photoimg03 = load_image(r"static\images\img01.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg03).place(x=0, y=600, width=header_width, height=header_height)

        self.photoimg04 = load_image(r"static\images\img02.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg04).place(x=header_width, y=600, width=header_width, height=header_height)

        
    def train_classifier(self):
        data_dir = "data"

        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        if len(path) == 0:
            messagebox.showerror("Error", "No images found in data folder!")
            return

        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')
            imageNp = np.array(img, 'uint8')

            file_name = os.path.split(image)[1]
            student_id = int(file_name.split('.')[1])

            faces.append(imageNp)
            ids.append(student_id)

            cv2.imshow("Training", imageNp)
            cv2.waitKey(1)

        ids = np.array(ids)

        clf = cv2.face.LBPHFaceRecognizer_create()  # type: ignore # use opencv-contrib-python instead of cv-python
        clf.train(faces, ids)
        clf.write("classifier.xml")

        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training datasets completed!")













if __name__ == "__main__":
    root = Tk()
    app = Train(root)
    root.mainloop()