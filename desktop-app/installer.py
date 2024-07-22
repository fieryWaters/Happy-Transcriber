import os
import sys
import shutil
import winshell
from win32com.client import Dispatch
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def install_happy_transcriber():
    # Get the current user's home directory
    home_dir = os.path.expanduser("~")

    # Set the installation directory
    install_dir = os.path.join(home_dir, "HappyTranscriber")

    # Create the installation directory if it doesn't exist
    os.makedirs(install_dir, exist_ok=True)

    # Copy the HappyTranscriber.exe, ffmpeg.exe, and ffprobe.exe to the installation directory
    try:
        shutil.copy(resource_path("HappyTranscriber.exe"), install_dir)
        shutil.copy(resource_path("ffmpeg.exe"), install_dir)
        shutil.copy(resource_path("ffprobe.exe"), install_dir)
        print("Files copied successfully.")
    except Exception as e:
        print(f"Error copying files: {str(e)}")
        messagebox.showerror("Installation Error", f"An error occurred during installation:\n\n{str(e)}")
        return

    # Create a shortcut in the user's Start menu
    start_menu_dir = winshell.start_menu()
    shortcut_path = os.path.join(start_menu_dir, "Programs", "HappyTranscriber.lnk")
    target_path = os.path.join(install_dir, "HappyTranscriber.exe")
    icon_path = target_path

    try:
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.IconLocation = icon_path
        shortcut.save()
        print("Shortcut created successfully.")
    except Exception as e:
        print(f"Error creating shortcut: {str(e)}")
        messagebox.showerror("Installation Error", f"An error occurred while creating the shortcut:\n\n{str(e)}")
        return

    print("Installation completed successfully.")
    messagebox.showinfo("Installation Successful", "Happy Transcriber has been installed successfully.\n\nTo open the app, press the Start button and type 'HappyTranscriber'.")

if __name__ == "__main__":
    install_happy_transcriber()
