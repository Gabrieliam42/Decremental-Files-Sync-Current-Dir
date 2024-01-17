import os
import shutil
import tkinter as tk
from tkinter import filedialog
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def main():
    # Use the current working directory as the source directory
    source = os.getcwd()

    # Open a file dialog to choose the destination directory
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    destination = filedialog.askdirectory(title="Select Destination Folder")

    # If the user cancels the dialog, exit the script
    if not destination:
        print("Destination folder not selected. Exiting.")
        exit()

    # Get file sizes and create a list of (size, path) tuples
    file_sizes = [(os.path.getsize(os.path.join(root, file)), os.path.join(root, file))
                  for root, dirs, files in os.walk(source) for file in files]

    # Sort the list in descending order by file size
    file_sizes.sort(reverse=True)

    # Copy files to the destination directory
    for size, file_path in file_sizes:
        relative_path = os.path.relpath(file_path, source)
        destination_path = os.path.join(destination, relative_path)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy2(file_path, destination_path)
        print(f"Copied: {os.path.basename(file_path)} -> {destination_path}")

    print("Files copied successfully.")

if __name__ == "__main__":
    main()
