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

def build_exe(script_name, exe_name, icon_path=None, additional_files=None):
    python_dir = os.path.dirname(sys.executable)
    pyinstaller_path = os.path.join(python_dir, "pyinstaller.exe")
    if os.path.exists(pyinstaller_path):
        command = [
            f'"{pyinstaller_path}"',
            "--onefile",
            f'--name "{exe_name}"',
        ]
        if icon_path:
            command.append(f'--icon "{icon_path}"')
            command.append(f'--add-data "{icon_path}:."')
        if additional_files:
            for file in additional_files:
                command.append(f'--add-data "{file}:."')
        command.append(script_name)
        command_str = " ".join(command)
        output = run_command(command_str)
        if output is not None:
            print(f"{exe_name}.exe built successfully")
        else:
            print(f"Failed to build {exe_name}.exe")
    else:
        print("PyInstaller not found in the virtual environment Scripts directory")

def move_exe(exe_name):
    dist_dir = "./dist"
    exe_path = os.path.join(dist_dir, f"{exe_name}.exe")
    if os.path.exists(exe_path):
        destination = "./"
        destination_path = os.path.join(destination, f"{exe_name}.exe")
        if os.path.exists(destination_path):
            os.remove(destination_path)
        shutil.move(exe_path, destination)
        print(f"Moved {exe_name}.exe to the current directory")
    else:
        print(f"Could not find {exe_name}.exe in the dist directory")

def clean_up(spec_file):
    build_dir = "./build"
    dist_dir = "./dist"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print("Removed build directory")
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
        print("Removed dist directory")
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"Removed {spec_file} file")

def generate_core_exe(script_name, exe_name, icon_path):
    install_pyinstaller()
    build_exe(script_name, exe_name, icon_path)
    move_exe(exe_name)
    clean_up(f"{script_name.split('.')[0]}.spec")

def generate_installer_exe(script_name, exe_name, icon_path, additional_files):
    install_pyinstaller()
    build_exe(script_name, exe_name, icon_path, additional_files)
    move_exe(exe_name)
    clean_up(f"{script_name.split('.')[0]}.spec")

def generate_generic_exe(script_name, exe_name, icon_path=None, additional_files=None):
    install_pyinstaller()
    build_exe(script_name, exe_name, icon_path, additional_files)
    move_exe(exe_name)
    clean_up(f"{script_name.split('.')[0]}.spec")

if __name__ == "__main__":
    # Build the core application executable
    generate_core_exe("gui_main.py", "HappyTranscriber", "happyKitty.ico")

    # Build the installer executable
    generate_installer_exe("installer.py", "HappyTranscriberInstaller", "happyKitty.ico", ["HappyTranscriber.exe", "ffmpeg.exe", "ffprobe.exe"])