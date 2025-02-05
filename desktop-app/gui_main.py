import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import subprocess
import openai
from transcribe_module import transcribe_file

# Get the user's home directory
home_dir = os.path.expanduser("~")

# Set the installation directory
install_dir = os.path.join(home_dir, "HappyTranscriber")

# File to store the API key
api_key_file = os.path.join(install_dir, 'api_key.txt')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def select_files_and_directories():
    desktop_dir = os.path.expanduser("~/Desktop")
    paths = filedialog.askopenfilenames(initialdir=desktop_dir, title="Select Files and Directories", filetypes=[("All Files", "*.*")])
    
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, ', '.join(paths))

def open_file_location(file_path):
    if os.path.isdir(file_path):
        directory = file_path
    else:
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

def get_api_key():
    if not os.path.exists(api_key_file):
        api_key = simpledialog.askstring("API Key", "Please enter your OpenAI API key:")
        
        if not api_key:
            messagebox.showwarning("Warning", "API key not provided.")
            return None
        
        # Create the installation directory if it doesn't exist
        os.makedirs(install_dir, exist_ok=True)
        
        with open(api_key_file, 'w') as file:
            file.write(api_key)
    else:
        with open(api_key_file, 'r') as file:
            api_key = file.read().strip()
    
    return api_key

def process_files(paths, api_key):
    total_files = sum(1 for path in paths for file_or_dir in (os.listdir(path) if os.path.isdir(path) else [path]) if os.path.isfile(file_or_dir) and is_supported_file(file_or_dir))
    current_file = 0
    
    for path in paths:
        if os.path.isdir(path):
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path) and is_supported_file(file_path):
                    current_file += 1
                    progress_bar["value"] = (current_file / total_files) * 100
                    status_text.set(f"Transcribing file {current_file} of {total_files}: {filename}")
                    window.update()
                    
                    transcribe_file(file_path, api_key, install_dir)
        elif os.path.isfile(path) and is_supported_file(path):
            current_file += 1
            progress_bar["value"] = (current_file / total_files) * 100
            status_text.set(f"Transcribing file {current_file} of {total_files}: {os.path.basename(path)}")
            window.update()
            
            transcribe_file(path, api_key, install_dir)
    
    return current_file, total_files

def transcribe_audio():
    paths = path_entry.get().split(', ')
    
    if not paths:
        messagebox.showwarning("Warning", "Please select files or directories.")
        return
    
    api_key = get_api_key()
    if not api_key:
        return
    
    # Disable the Transcribe button during processing
    transcribe_button.config(state=tk.DISABLED)
    
    # Update progress bar and status text
    progress_bar["value"] = 0
    status_text.set("Transcribing audio files...")
    window.update()
    
    try:
        current_file, total_files = process_files(paths, api_key)
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
            transcriptions_directory = os.path.join(os.path.dirname(paths[0]), "Transcriptions")
            open_file_location(transcriptions_directory)

# Create the main window
window = tk.Tk()
window.title("Happy Transcriber")
window.iconbitmap(resource_path("happyKitty.ico"))

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
    # Run the GUI
    window.mainloop()

if __name__ == "__main__":
    main()