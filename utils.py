# utils.py
import os
import subprocess
import tempfile
import urllib.request
import ctypes
import sys

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

def download_file(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        return True
    except urllib.error.URLError:
        return False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



def save_requirements():
    command = "pip freeze > requirements.txt"
    run_command(command)
    print("Requirements saved to requirements.txt")

def install_requirements():
    if getattr(sys, 'frozen', False):
        # The script is running as an executable (EXE)
        print("Running as an executable. Skipping requirements installation.")
        return

    python_exe = sys.executable
    command = f'"{python_exe}" -m pip install -r requirements.txt'
    output = run_command(command)
    if output:
        print("Requirements installed successfully")
    else:
        print("Failed to install requirements")

# save_requirements()