import tkinter as tk
from tkinter import filedialog, messagebox
import os
from transcribe_module import transcribe_folder

# File to store the API key
api_key_file = 'api_key.txt'

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(tk.END, folder_path)

def transcribe_audio():
    folder_path = folder_entry.get()
    
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder.")
        return
    
    if not os.path.exists(api_key_file):
        api_key = api_key_entry.get()
        
        if not api_key:
            messagebox.showwarning("Warning", "Please enter your OpenAI API key.")
            return
        
        with open(api_key_file, 'w') as file:
            file.write(api_key)
    else:
        with open(api_key_file, 'r') as file:
            api_key = file.read().strip()
    
    transcribe_folder(folder_path, api_key)
    messagebox.showinfo("Success", "Transcription completed.")

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

# API key input
api_key_label = tk.Label(window, text="OpenAI API Key:")
api_key_label.pack()

api_key_entry = tk.Entry(window, width=50)
api_key_entry.pack()

# Transcribe button
transcribe_button = tk.Button(window, text="Transcribe", command=transcribe_audio)
transcribe_button.pack()

# Run the GUI
window.mainloop()
