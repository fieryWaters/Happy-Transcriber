#install_7z.py #works
import os
import platform
import subprocess
import sys
import tempfile
import urllib.request
import ctypes

def download_file(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        return True
    except urllib.error.URLError:
        return False

def is_7zip_installed():
    seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"
    return os.path.exists(seven_zip_path)

def install_7zip():
    # Check if 7-Zip is already installed
    if is_7zip_installed():
        print("7-Zip is already installed.")
        input("press enter")
        return True

    # Download 7-Zip installer
    print("Downloading 7-Zip installer...")
    url = "https://www.7-zip.org/a/7z2201-x64.exe"
    with tempfile.TemporaryDirectory() as temp_dir:
        installer_path = os.path.join(temp_dir, "7zip_installer.exe")
        if not download_file(url, installer_path):
            print("Failed to download 7-Zip installer.")
            input("press enter to continue")
            return False

        # Install 7-Zip silently
        print("Installing 7-Zip...")
        subprocess.run([installer_path, "/S"], check=True)

    # Add 7-Zip to PATH using setx
    print("Adding 7-Zip to PATH...")
    seven_zip_dir = r"C:\Program Files\7-Zip"
    try:
        # This will add the directory to the PATH, which is the usual approach
        subprocess.run(f'setx PATH "%PATH%;{seven_zip_dir}"', shell=True)

        # If you really wanted to add the executable itself (unusual), you would use:
        # subprocess.run(f'setx PATH "%PATH%;{seven_zip_path}"', shell=True)
    except Exception as e:
        print(f"Failed to add 7-Zip to PATH. Error: {e}")
        input("press enter to continue")
        return False

    print("7-Zip installation completed successfully!")
    input("press enter to continue")
    return True

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

if __name__ == "__main__":
    run_as_admin()
    install_7zip()
