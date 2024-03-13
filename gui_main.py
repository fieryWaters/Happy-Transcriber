#gui_main.py
import utils
utils.install_requirements()


import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os
import subprocess
import openai
from transcribe_module import transcribe_file
from install_ffmpeg import install_ffmpeg, is_ffmpeg_installed
import pyuac
import sys

# # Check if FFmpeg is installed
# if not is_ffmpeg_installed():
#     install_ffmpeg()
#     messagebox.showinfo("FFmpeg Installation", "FFmpeg has been installed. Please rerun the application.")
#     sys.exit()
#     print("HERE")

# File to store the API key
api_key_file = 'api_key.txt'

def select_files_and_directories():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    paths = filedialog.askopenfilenames(initialdir=current_directory, title="Select Files and Directories", filetypes=[("All Files", "*.*")])
    
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, ', '.join(paths))

def open_file_location(file_path):
    directory = os.path.dirname(file_path)
    if os.path.exists(directory):
        if os.name == 'nt':  # For Windows
            os.startfile(directory)
        else:  # For macOS and Linux
            subprocess.Popen(['open', directory])
    else:
        messagebox.showinfo("Info", "Directory not found.")

def is_supported_file(file_path):
    return file_path.endswith(('.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a'))

def transcribe_audio():
    paths = path_entry.get().split(', ')
    
    if not paths:
        messagebox.showwarning("Warning", "Please select files or directories.")
        return
    
    if not os.path.exists(api_key_file):
        api_key = simpledialog.askstring("API Key", "Please enter your OpenAI API key:")
        
        if not api_key:
            messagebox.showwarning("Warning", "API key not provided.")
            return
        
        with open(api_key_file, 'w') as file:
            file.write(api_key)
    else:
        with open(api_key_file, 'r') as file:
            api_key = file.read().strip()
    
    # Disable the Transcribe button during processing
    transcribe_button.config(state=tk.DISABLED)
    
    # Update progress bar and status text
    progress_bar["value"] = 0
    status_text.set("Transcribing audio files...")
    window.update()
    
    total_files = sum(1 for path in paths for file_or_dir in (os.listdir(path) if os.path.isdir(path) else [path]) if os.path.isfile(file_or_dir) and is_supported_file(file_or_dir))
    current_file = 0
    
    try:
        for path in paths:
            if os.path.isdir(path):
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    if os.path.isfile(file_path) and is_supported_file(file_path):
                        current_file += 1
                        progress_bar["value"] = (current_file / total_files) * 100
                        status_text.set(f"Transcribing file {current_file} of {total_files}: {filename}")
                        window.update()
                        
                        transcribe_file(file_path, api_key)
            elif os.path.isfile(path) and is_supported_file(path):
                current_file += 1
                progress_bar["value"] = (current_file / total_files) * 100
                status_text.set(f"Transcribing file {current_file} of {total_files}: {os.path.basename(path)}")
                window.update()
                
                transcribe_file(path, api_key)
    except openai.error.AuthenticationError as e:
        messagebox.showerror("Authentication Error", str(e))
        response = messagebox.askyesno("Update API Key", "The provided API key is incorrect. Do you want to enter a new API key?\n\nNote: You may need to fund your OpenAI account to obtain a valid API key.")
        if response:
            api_key = simpledialog.askstring("API Key", "Please enter a new OpenAI API key:")
            if api_key:
                with open(api_key_file, 'w') as file:
                    file.write(api_key)
                messagebox.showinfo("API Key Updated", "The API key has been updated. Please try transcribing again.")
            else:
                messagebox.showwarning("Warning", "No API key provided.")
        # Reset progress bar and status text
        progress_bar["value"] = 0
        status_text.set("")
    except openai.error.APIConnectionError as e:
        messagebox.showerror("Error", "Internet connection lost. Transcription aborted.")
        # Reset progress bar and status text
        progress_bar["value"] = 0
        status_text.set("")
    finally:
        # Enable the Transcribe button after processing
        transcribe_button.config(state=tk.NORMAL)
    
    # Reset progress bar and status text
    progress_bar["value"] = 0
    status_text.set("")
    
    # Show completion message with the option to open the file location
    if current_file == total_files:
        response = messagebox.askyesno("Transcription Complete", "Transcription completed. Do you want to open the file location?")
        if response:
            open_file_location(paths[0])
# Create the main window
window = tk.Tk()
window.title("Audio Transcription")

# File and directory selection
path_label = tk.Label(window, text="Select Files and Directories:")
path_label.pack()

path_entry = tk.Entry(window, width=50)
path_entry.pack()

select_button = tk.Button(window, text="Select", command=select_files_and_directories)
select_button.pack()

# Transcribe button
transcribe_button = tk.Button(window, text="Transcribe", command=transcribe_audio)
transcribe_button.pack()

# Progress bar
progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
progress_bar.pack()

# Status text
status_text = tk.StringVar()
status_label = tk.Label(window, textvariable=status_text)
status_label.pack()

def main():
    # Check if FFmpeg is installed
    if not is_ffmpeg_installed():
        if not pyuac.isUserAdmin():
            print("Requesting administrator privileges for FFmpeg installation...")
            pyuac.runAsAdmin()
        else:
            install_ffmpeg()
            messagebox.showinfo("FFmpeg Installation", "FFmpeg has been installed. Please rerun the application.")
        # sys.exit()
    else:
        # Run the GUI
        window.mainloop()

if __name__ == "__main__":
    main()