import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os
import subprocess
from transcribe_module import transcribe_file

# File to store the API key
api_key_file = 'api_key.txt'

def select_folder():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = filedialog.askdirectory(initialdir=current_directory)
    folder_entry.delete(0, tk.END)
    folder_entry.insert(tk.END, folder_path)

def open_file_location(folder_path):
    transcriptions_directory = os.path.join(folder_path, 'Transcriptions')
    if os.path.exists(transcriptions_directory):
        if os.name == 'nt':  # For Windows
            os.startfile(transcriptions_directory)
        else:  # For macOS and Linux
            subprocess.Popen(['open', transcriptions_directory])
    else:
        messagebox.showinfo("Info", "No transcriptions found.")

def transcribe_audio():
    folder_path = folder_entry.get()
    
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder.")
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
    
    total_files = sum(filename.endswith(('.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a')) for filename in os.listdir(folder_path))
    current_file = 0
    
    for filename in os.listdir(folder_path):
        if filename.endswith(('.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a')):
            current_file += 1
            progress_bar["value"] = (current_file / total_files) * 100
            status_text.set(f"Transcribing file {current_file} of {total_files}: {filename}")
            window.update()
            
            audio_path = os.path.join(folder_path, filename)
            transcribe_file(audio_path, api_key)
    
    # Enable the Transcribe button after processing
    transcribe_button.config(state=tk.NORMAL)
    
    # Reset progress bar and status text
    progress_bar["value"] = 0
    status_text.set("")
    
    # Show completion message with the option to open the file location
    if messagebox.askyesno("Transcription Complete", "Transcription completed. Do you want to open the file location?"):
        open_file_location(folder_path)

# Create the main window
window = tk.Tk()
window.title("Audio Transcription")

# Folder selection
folder_label = tk.Label(window, text="Select Folder:")
folder_label.pack()

folder_entry = tk.Entry(window, width=50)
folder_entry.pack()

folder_button = tk.Button(window, text="Browse", command=select_folder)
folder_button.pack()

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

# Run the GUI
window.mainloop()