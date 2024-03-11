# install_7z.py
import os
import tempfile
from utils import download_file, run_as_admin, subprocess

def is_7zip_installed():
    seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"
    return os.path.exists(seven_zip_path)

def install_7zip():
    # Check if 7-Zip is already installed
    if is_7zip_installed():
        print("7-Zip is already installed.")
        return True
    
    run_as_admin()

    # Download 7-Zip installer
    print("Downloading 7-Zip installer...")
    url = "https://www.7-zip.org/a/7z2201-x64.exe"
    with tempfile.TemporaryDirectory() as temp_dir:
        installer_path = os.path.join(temp_dir, "7zip_installer.exe")
        if not download_file(url, installer_path):
            print("Failed to download 7-Zip installer.")
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
    except Exception as e:
        print(f"Failed to add 7-Zip to PATH. Error: {e}")
        return False

    print("7-Zip installation completed successfully!")
    return True

if __name__ == "__main__":
    install_7zip()