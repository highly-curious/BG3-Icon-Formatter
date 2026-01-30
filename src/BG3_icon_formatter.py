from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import string
import sys
import platform
import subprocess


def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def resize_image(input_path, output_path, size):
    """Resizes image(s) to the 3 resolutions required for bg3."""
    try:
        with Image.open(input_path) as img:
            img = img.resize(size, Image.LANCZOS)
            img.save(output_path, format="PNG")
    except Exception as e:
        print(f"Error resizing image {input_path}: {e}")


def fade_image(image_path):
    """Applies a fade effect to the bottom of an image."""
    try:
        image = Image.open(image_path).convert("RGBA")
        width, height = image.size

        fade_start = int(height * 0.1)  # Start fade 10% from the bottom
        fade_range = height * 0.8  # Fade over 80% of the height

        # Applies fade
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                r, g, b, a = pixels[x, y]
                if y > fade_start:
                    fade_factor = ((y - fade_start) / fade_range) ** 2.5
                    fade_factor = min(fade_factor, 1)
                    new_alpha = int(a * (1 - fade_factor))
                    pixels[x, y] = (r, g, b, new_alpha)

        image.save(image_path, format="PNG")
    except Exception as e:
        print(f"Error fading image {image_path}: {e}")


def generate_random_prefix(length=3):
    """Generates a random prefix for filenames."""
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def open_output_folder(output_folder):
    """Opens the output folder in the system file explorer."""
    try:
        if platform.system() == "Windows":
            os.startfile(output_folder)  # Windows
        elif platform.system() == "Darwin":
            subprocess.run(["open", output_folder])  # macOS
        else:
            subprocess.run(["xdg-open", output_folder])  # Linux
    except Exception as e:
        print(f"Error opening output folder: {e}")


def process_images(input_folder, output_folder, prefix, sizes):
    """Processes all PNG images in the selected input folder."""
    try:
        # Creates output folders for each size
        for size_label in sizes.keys():
            os.makedirs(os.path.join(output_folder, size_label), exist_ok=True)

        # Looks for PNG files in the input folder
        png_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".png")]
        if not png_files:
            messagebox.showwarning("No PNG Files", "No PNG files found in the input folder.")
            return

        # Process
        for filename in png_files:
            input_path = os.path.join(input_folder, filename)
            prefixed_filename = f"{prefix}{filename}"

            for size_label, size in sizes.items():
                output_path = os.path.join(output_folder, size_label, prefixed_filename)
                resize_image(input_path, output_path, size)

                # Applies fade effect only to 380x380 images
                if size_label == "380x380":
                    fade_image(output_path)

        messagebox.showinfo("Processing Complete", "All images processed successfully!")
        open_output_folder(output_folder)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# GUI Setup
def select_input_folder():
    """Open a dialog to select the input folder."""
    folder = filedialog.askdirectory(title="Select Input Folder")
    input_folder_var.set(folder)


def select_output_folder():
    """Opens a dialog to select the output folder."""
    folder = filedialog.askdirectory(title="Select Output Folder")
    output_folder_var.set(folder)


def generate_random_prefix_ui():
    """Generates a random prefix and update the UI."""
    prefix_var.set(generate_random_prefix() + "_")


def start_processing():
    """Starts processing images."""
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    prefix = prefix_var.get()

    if not input_folder or not output_folder:
        messagebox.showwarning("Input/Output Missing", "Please select both input and output folders.")
        return

# #Uncomment this block if you always want a random prefix without clicking the random button
    # if not prefix:
    #     prefix = generate_random_prefix() + "_"

    sizes = {
        "144x144": (144, 144),
        "380x380": (380, 380),
        "64x64": (64, 64)
    }

    # Disables the start button to prevent multiple clicks
    start_button.config(state=tk.DISABLED)

    # Process images (blocking operation)
    process_images(input_folder, output_folder, prefix, sizes)

    # Re-enables the start button
    start_button.config(state=tk.NORMAL)


# Main GUI
root = tk.Tk()
root.title("BG3 Icon Formatter")

# Icon
try:
    root.iconbitmap(resource_path('iconformatter.ico'))
except Exception as e:
    print(f"Error loading icon: {e}")

# Variables
input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
prefix_var = tk.StringVar()

# UI Elements
tk.Label(root, text="Input Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=input_folder_var, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_input_folder).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="File Prefix:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=prefix_var, width=50).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Random", command=generate_random_prefix_ui).grid(row=2, column=2, padx=5, pady=5)

start_button = tk.Button(root, text="Start Processing", command=start_processing, bg="purple", fg="white")
start_button.grid(row=3, column=1, padx=5, pady=20)

# Start GUI
root.mainloop()