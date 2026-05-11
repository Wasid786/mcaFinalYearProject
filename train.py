from tkinter import *
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os
import numpy as np
import cv2


class Train:
    def __init__(self, root):
        self.root = root
        self.root.title("Train Data Set")
        self.root.state("zoomed")

        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{sw}x{sh}+0+0")

        # ── Load helper ──────────────────────────────────────────────────────
        def load_image(path, w, h):
            img = Image.open(path)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)

        # ── Title bar (full width, 50 px tall) ───────────────────────────────
        title_size = max(20, int(sw * 0.020))
        Label(
            self.root, text="Train Data Set",
            font=("times new roman", title_size, "bold"),
            bg="white", fg="blue",
        ).place(relx=0, rely=0, relwidth=1, height=50)

        # ── Two image panels (each half width, 40 % of screen height) ────────
        panel_h = int(sh * 0.40)

        self.photoimg01 = load_image(r"static\images\train_01.jpg", sw // 2, panel_h)
        Label(self.root, image=self.photoimg01).place(
            x=0, y=50, relwidth=0.5, height=panel_h
        )

        self.photoimg02 = load_image(r"static\images\train_02.jpg", sw // 2, panel_h)
        Label(self.root, image=self.photoimg02).place(
            relx=0.5, y=50, relwidth=0.5, height=panel_h
        )

        # ── Action buttons (side by side, below first image row) ─────────────
        btn_y    = 50 + panel_h
        btn_h    = max(55, int(sh * 0.07))
        btn_font = max(16, int(sw * 0.014))

        Button(
            self.root, text="Capture New Samples",
            command=self.capture_faces,
            cursor="hand2",
            font=("times new roman", btn_font, "bold"),
            bg="#2196F3", fg="white",
        ).place(x=0, y=btn_y, relwidth=0.5, height=btn_h)

        Button(
            self.root, text="Train Model",
            command=self.train_classifier,
            cursor="hand2",
            font=("times new roman", btn_font, "bold"),
            bg="#F44336", fg="white",
        ).place(relx=0.5, y=btn_y, relwidth=0.5, height=btn_h)

        # ── Second decorative image row ───────────────────────────────────────
        row2_y = btn_y + btn_h
        row2_h = sh - row2_y   # fill whatever space is left

        self.photoimg03 = load_image(r"static\images\train_03.jpg", sw // 2, max(1, row2_h))
        Label(self.root, image=self.photoimg03).place(
            x=0, y=row2_y, relwidth=0.5, height=row2_h
        )

        self.photoimg04 = load_image(r"static\images\train_04.jpg", sw // 2, max(1, row2_h))
        Label(self.root, image=self.photoimg04).place(
            relx=0.5, y=row2_y, relwidth=0.5, height=row2_h
        )

    # ── Capture face samples from webcam ────────────────────────────────────
    def capture_faces(self):
        student_id = simpledialog.askstring("Student ID", "Enter Student ID:")
        if not student_id or not student_id.strip().isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Student ID.")
            return

        student_id = student_id.strip()
        os.makedirs("data", exist_ok=True)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # type: ignore
        )
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            messagebox.showerror("Error", "Could not open webcam.")
            return

        MAX_SAMPLES = 50
        messagebox.showinfo(
            "Capturing",
            f"Webcam will open.\nLook at the camera — {MAX_SAMPLES} photos will be saved.\n"
            "Press ESC to stop early.",
        )

        count = 0
        while count < MAX_SAMPLES:
            ret, frame = cam.read()
            if not ret:
                break

            gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                count += 1
                cv2.imwrite(f"data/User.{student_id}.{count}.jpg", gray[y:y+h, x:x+w])
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(
                    frame, f"Sample {count}/{MAX_SAMPLES}",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,
                )

            cv2.imshow(f"Capturing — Student {student_id} (ESC to stop)", frame)
            if cv2.waitKey(1) == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Done", f"Captured {count} samples for Student ID {student_id}.")

    # ── Train model on saved samples ─────────────────────────────────────────
    def train_classifier(self):
        data_dir = "data"

        if not os.path.exists(data_dir) or not os.listdir(data_dir):
            messagebox.showerror(
                "Error", "No images found in data folder!\nCapture samples first."
            )
            return

        faces, ids = [], []

        for fname in os.listdir(data_dir):
            image_path = os.path.join(data_dir, fname)
            img = Image.open(image_path).convert("L")
            img_np = np.array(img, "uint8")

            try:
                student_id = int(fname.split(".")[1])
            except (IndexError, ValueError):
                continue  # skip files with unexpected names

            faces.append(img_np)
            ids.append(student_id)

            cv2.imshow("Training", img_np)
            cv2.waitKey(1)

        if not faces:
            messagebox.showerror("Error", "No valid training images found.")
            cv2.destroyAllWindows()
            return

        clf = cv2.face.LBPHFaceRecognizer_create()  # type: ignore
        clf.train(faces, np.array(ids))
        clf.write("classifier.xml")

        cv2.destroyAllWindows()
        messagebox.showinfo("Result", f"Training complete!\n{len(faces)} images used.")


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    Train(root)
    root.mainloop()