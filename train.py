from tkinter import *
from tkinter import messagebox, simpledialog
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
        self.root.title("Face Recognition Page")

        # Title
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

        # ── Button 1: Capture new face samples ──────────────────────────
        btn_capture = Button(
            self.root, text="Capture New Samples",
            command=self.capture_faces,
            cursor="hand2",
            font=("times new roman", 25, "bold"),
            bg="#2196F3", fg="white"        # blue = "collect data"
        )
        btn_capture.place(x=0, y=500, width=self.screen_width // 2, height=60)

        # ── Button 2: Train model on saved samples ───────────────────────
        btn_train = Button(
            self.root, text="Train Model",
            command=self.train_classifier,
            cursor="hand2",
            font=("times new roman", 25, "bold"),
            bg="#F44336", fg="white"        # red = "build the model"
        )
        btn_train.place(x=self.screen_width // 2, y=500, width=self.screen_width // 2, height=60)

        self.photoimg03 = load_image(r"static\images\img01.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg03).place(x=0, y=600, width=header_width, height=header_height)

        self.photoimg04 = load_image(r"static\images\img02.jpg", header_width, header_height)
        Label(self.root, image=self.photoimg04).place(x=header_width, y=600, width=header_width, height=header_height)

    # ── NEW: Capture face samples from webcam ────────────────────────────
    def capture_faces(self):
        student_id = simpledialog.askstring("Student ID", "Enter Student ID:")
        if not student_id or not student_id.strip().isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Student ID.")
            return

        student_id = student_id.strip()
        os.makedirs("data", exist_ok=True)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") # type: ignore
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            return

        count = 0
        MAX_SAMPLES = 50   # ← change this if you want more/fewer photos

        messagebox.showinfo(
            "Capturing",
            f"Webcam will open.\nLook at the camera — {MAX_SAMPLES} photos will be saved.\nPress ESC to stop early."
        )

        while count < MAX_SAMPLES:
            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                count += 1
                face_img = gray[y:y+h, x:x+w]
                filename = f"data/User.{student_id}.{count}.jpg"
                cv2.imwrite(filename, face_img)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Sample {count}/{MAX_SAMPLES}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow(f"Capturing — Student {student_id} (ESC to stop)", frame)
            if cv2.waitKey(1) == 27:   # ESC key
                break

        cam.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Done", f"Captured {count} samples for Student ID {student_id}.")

    # ── EXISTING: Train model on saved samples ───────────────────────────
    def train_classifier(self):
        data_dir = "data"

        if not os.path.exists(data_dir) or len(os.listdir(data_dir)) == 0:
            messagebox.showerror("Error", "No images found in data folder!\nCapture samples first.")
            return

        path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
        faces, ids = [], []

        for image_path in path:
            img = Image.open(image_path).convert('L')
            imageNp = np.array(img, 'uint8')

            # Filename format: User.<id>.<count>.jpg
            file_name = os.path.split(image_path)[1]
            try:
                student_id = int(file_name.split('.')[1])
            except (IndexError, ValueError):
                continue   # skip files that don't match the pattern

            faces.append(imageNp)
            ids.append(student_id)

            cv2.imshow("Training", imageNp)
            cv2.waitKey(1)

        if not faces:
            messagebox.showerror("Error", "No valid training images found.")
            cv2.destroyAllWindows()
            return

        ids = np.array(ids)
        clf = cv2.face.LBPHFaceRecognizer_create()  # type: ignore
        clf.train(faces, ids)
        clf.write("classifier.xml")

        cv2.destroyAllWindows()
        messagebox.showinfo("Result", f"Training complete!\n{len(faces)} images used.")


if __name__ == "__main__":
    root = Tk()
    app = Train(root)
    root.mainloop()