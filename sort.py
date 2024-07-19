import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import shutil

class ImageSorter:
    def __init__(self, root, image_dir, goal_dir):
        self.root = root
        self.image_dir = image_dir
        self.goal_dir = goal_dir

        self.image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        self.current_image = None

        self.create_widgets()
        self.load_random_image()

    def create_widgets(self):
        self.root.title("Image Sorter")

        self.load_button = tk.Button(self.root, text="Load Random Image", command=self.load_random_image)
        self.load_button.pack()

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.sort_left_button = tk.Button(self.root, text="Sort Left", command=lambda: self.sort_image("left"))
        self.sort_left_button.pack(side=tk.LEFT)

        self.sort_right_button = tk.Button(self.root, text="Sort Right", command=lambda: self.sort_image("right"))
        self.sort_right_button.pack(side=tk.RIGHT)

    def load_random_image(self):
        if self.image_files:
            self.current_image = random.choice(self.image_files)
            file_path = os.path.join(self.image_dir, self.current_image)
            img = Image.open(file_path)
            img = img.resize((400, 400), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

    def sort_image(self, category):
        if self.current_image:
            src = os.path.join(self.image_dir, self.current_image)
            dest_dir = os.path.join(self.goal_dir, category)

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            dest = os.path.join(dest_dir, self.current_image)
            shutil.move(src, dest)
            self.image_files.remove(self.current_image)
            self.current_image = None
            self.load_random_image()

if __name__ == "__main__":
    root = tk.Tk()

    image_dir = "/home/coding/gui/image/directory"  # Replace with your image directory path
    goal_dir = "/home/coding/gui/imag/directory"    # Replace with your goal directory path

    app = ImageSorter(root, image_dir, goal_dir)
    root.mainloop()
