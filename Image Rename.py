import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import datetime
import requests
import random

class ImageRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Renamer")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f0f0")

        # Fetch background image
        self.bg_images = self.fetch_background_images()

        self.image_files = []
        self.current_index = 0
        self.renamed_count = 0
        self.start_time = datetime.datetime.now()  # Start time of the program
        self.start_rename_time = datetime.datetime.now()  # Initialize start time for renaming
        self.rename_speed = 0
        self.last_60_seconds_renamed_count = 0

        # Styling
        self.font = ("Arial", 12)
        self.bg_color = "#f0f0f0"
        self.fg_color = "#333333"
        self.entry_bg_color = "#ffffff"

        # Background label
        self.bg_label = tk.Label(root)
        self.bg_label.place(relwidth=1, relheight=1)
        self.change_background()

        self.image_label = tk.Label(root, bg=self.bg_color)
        self.image_label.pack(pady=10)

        self.rename_entry_var = tk.StringVar()
        self.rename_entry = tk.Entry(root, textvariable=self.rename_entry_var, font=self.font, bg=self.entry_bg_color, fg=self.fg_color)
        self.rename_entry.pack(pady=5, padx=10)
        self.rename_entry.bind("<Return>", self.rename_image)

        self.counter_label = tk.Label(root, font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.counter_label.pack(pady=5)

        self.elapsed_time_label = tk.Label(root, font=self.font, bg=self.bg_color, fg=self.fg_color)
        self.elapsed_time_label.pack(pady=5)

        self.change_theme_button = tk.Button(root, text="Theme", command=self.change_background, font=self.font, bg=self.bg_color, fg=self.fg_color, relief=tk.FLAT)
        self.change_theme_button.pack(side="left", padx=10, pady=10)

        self.update_rename_speed()

    def fetch_background_images(self):
        default_bg = self.fetch_background_image("https://i.ibb.co/ThxNP6t/bg.jpg")
        example_bg1 = self.fetch_background_image("https://i.ibb.co/4WZ6h0p/background-gradient-lights.jpg")
        example_bg2 = self.fetch_background_image("https://i.ibb.co/1d2TNMM/charlesdeluvio-pc-Zvxr-Ay-Yo-Q-unsplash.jpg")
        example_bg3 = self.fetch_background_image("https://i.ibb.co/mC4vLZk/codioful-formerly-gradienta-n2-Xq-Pm7-Bqhk-unsplash.jpg")
        return [default_bg, example_bg1, example_bg2, example_bg3]

    def fetch_background_image(self, url):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                image_data = response.raw
                bg_image = ImageTk.PhotoImage(Image.open(image_data))
                return bg_image
            else:
                return None
        except Exception as e:
            print("Error fetching background image:", e)
            return None

    def change_background(self):
        bg_image = random.choice(self.bg_images)
        if bg_image:
            self.bg_label.configure(image=bg_image)
            self.bg_label.image = bg_image
        else:
            self.bg_label.configure(bg="white")

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.lower().endswith(('.jpg', '.jpeg', '.png')) and len(os.path.splitext(filename)[0]) != 4]
            if self.image_files:
                self.current_index = 0
                self.renamed_count = 0
                self.last_60_seconds_renamed_count = 0
                self.start_rename_time = datetime.datetime.now()  # Reset start rename time
                self.update_rename_speed()
                self.show_next_image()
                self.select_folder_button.pack_forget()  # Remove "Select Folder" button
        else:
            messagebox.showinfo("Error", "Please select a folder.")

    def show_next_image(self):
        if self.current_index < len(self.image_files):
            image = Image.open(self.image_files[self.current_index])
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo, bg=self.bg_color)
            self.image_label.image = photo
            self.rename_entry_var.set("")  # Clear the entry box
            self.rename_entry.focus_set()  # Set focus to the entry box
            remaining_images = len(self.image_files) - self.current_index
            self.counter_label.config(text=f"Renamed: {self.renamed_count}/{remaining_images}", bg=self.bg_color, fg=self.fg_color)
        else:
            messagebox.showinfo("Info", "All images have been renamed.")

    def rename_image(self, event=None):
        new_file_name = os.path.join(os.path.dirname(self.image_files[self.current_index]), self.rename_entry.get() + os.path.splitext(self.image_files[self.current_index])[1])
        os.rename(self.image_files[self.current_index], new_file_name)
        self.renamed_count += 1
        self.last_60_seconds_renamed_count += 1
        self.current_index += 1
        self.show_next_image()

    def update_rename_speed(self):
        elapsed_time = (datetime.datetime.now() - self.start_time).total_seconds()
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.elapsed_time_label.config(text=f"Elapsed Time: {int(hours)}h {int(minutes)}m {int(seconds)}s", bg=self.bg_color, fg=self.fg_color)
        if elapsed_time >= 60:
            self.rename_speed = self.last_60_seconds_renamed_count / elapsed_time
            self.last_60_seconds_renamed_count = 0  # Reset the count for the next interval
        else:
            self.rename_speed = self.last_60_seconds_renamed_count / elapsed_time if elapsed_time > 0 else 0
        self.root.after(1000, self.update_rename_speed)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRenamer(root)
    app.select_folder_button = tk.Button(root, text="Select Folder", command=app.select_folder, font=app.font, bg=app.bg_color, fg=app.fg_color, relief=tk.FLAT)
    app.select_folder_button.pack(pady=5)
    root.mainloop()
