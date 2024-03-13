import os
import subprocess
import shutil
import sys

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

def install_pyinstaller():
    python_exe = sys.executable
    command = f'"{python_exe}" -m pip install pyinstaller'
    output = run_command(command)
    if output is not None:
        print("PyInstaller installed successfully")
    else:
        print("Failed to install PyInstaller")

def build_exe(script_name):
    python_dir = os.path.dirname(sys.executable)
    pyinstaller_path = os.path.join(python_dir, "pyinstaller.exe")
    
    if os.path.exists(pyinstaller_path):
        command = f'"{pyinstaller_path}" --onefile {script_name}'
        output = run_command(command)
        if output is not None:
            print("EXE built successfully")
        else:
            print("Failed to build EXE")
    else:
        print("PyInstaller not found in the virtual environment Scripts directory")

def move_exe(script_name):
    dist_dir = "./dist"
    exe_name = f"{os.path.splitext(script_name)[0]}.exe"
    exe_path = os.path.join(dist_dir, exe_name)
    
    if os.path.exists(exe_path):
        destination = "./"
        destination_path = os.path.join(destination, exe_name)
        
        if os.path.exists(destination_path):
            os.remove(destination_path)
        
        shutil.move(exe_path, destination)
        print(f"Moved {exe_name} to the current directory")
    else:
        print(f"Could not find {exe_name} in the dist directory")

def clean_up():
    build_dir = "./build"
    dist_dir = "./dist"
    spec_file = "gui_main.spec"
    
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print("Removed build directory")
    
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
        print("Removed dist directory")
    
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print("Removed spec file")

def generate_exe(script_name):
    install_pyinstaller()
    build_exe(script_name)
    move_exe(script_name)
    clean_up()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the script name as a command-line argument.")
        sys.exit(1)
    
    script_name = sys.argv[1]
    generate_exe(script_name)

