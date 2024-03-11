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

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def save_requirements():
    command = "pip freeze > requirements.txt"
    run_command(command)
    print("Requirements saved to requirements.txt")

def install_requirements():
    command = "pip install -r requirements.txt"
    output = run_command(command)
    if output:
        print("Requirements installed successfully")
    else:
        print("Failed to install requirements")