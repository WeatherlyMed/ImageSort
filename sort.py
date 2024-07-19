import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sys

class PhotoSorter:
    def __init__(self, root, input_dir, output_dir):
        self.root = root
        self.root.title("Photo Sorter")

        self.input_dir = input_dir
        self.output_dir = output_dir
        self.counter_file = 'counter.txt'

        self.image_files = self.get_image_files()

        self.label = tk.Label(root, text=f"Sorting {len(self.image_files)} images from {self.input_dir}")
        self.label.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.categories = ["ERROR (Left)", "Negative (Up)", "Positive (Right)", "None (Down)"]
        self.category_shortcuts = ["<Left>", "<Up>", "<Right>", "<Down>"]

        self.index = 0
        self.load_image()

        # Bind arrow keys for sorting
        for category, shortcut in zip(self.categories, self.category_shortcuts):
            root.bind(shortcut, lambda event, c=category.split()[0]: self.sort_image(c))

        self.create_buttons()

    def create_buttons(self):
        self.category_buttons = []
        for category in self.categories:
            button = tk.Button(self.root, text=category, command=lambda c=category.split()[0]: self.sort_image(c))
            button.pack()
            self.category_buttons.append(button)

    def get_image_files(self):
        image_files = []
        for filename in os.listdir(self.input_dir):
            if self.is_image_file(filename):
                image_files.append(filename)
        return image_files

    def is_image_file(self, filename):
        return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

    def load_image(self):
        if self.index < len(self.image_files):
            filename = self.image_files[self.index]
            filepath = os.path.join(self.input_dir, filename)
            try:
                image = Image.open(filepath)
                image.thumbnail((400, 400))  # Resize image to fit the window
                self.photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=self.photo)
                self.image_label.image = self.photo
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            self.image_label.config(image=None)
            self.image_label.config(text="All images sorted!")

    def sort_image(self, category):
        if self.index < len(self.image_files):
            filename = self.image_files[self.index]
            src = os.path.join(self.input_dir, filename)
            dst = os.path.join(self.output_dir, category)
            if not os.path.exists(dst):
                os.makedirs(dst)
            counter = self.get_counter()
            new_filename = f"{os.path.splitext(filename)[0]}_sorted_{counter}{os.path.splitext(filename)[1]}"
            shutil.move(src, os.path.join(dst, new_filename))
            self.index += 1
            self.update_counter(counter)
            self.load_image()
        else:
            self.index = 0
            self.image_files = self.get_image_files()
            self.load_image()

    def get_counter(self):
        if os.path.exists(self.counter_file):
            with open(self.counter_file, 'r') as f:
                counter = int(f.read())
        else:
            counter = 0
        return counter

    def update_counter(self, counter):
        counter += 1
        with open(self.counter_file, 'w') as f:
            f.write(str(counter))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python photosorter.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(input_dir) or not os.path.isdir(output_dir):
        print("Error: Input or output directory does not exist.")
        sys.exit(1)

    root = tk.Tk()
    app = PhotoSorter(root, input_dir, output_dir)
    root.mainloop()
