# install_ffmpeg.py
import os
import platform
import shutil
import zipfile
import tarfile
import tempfile
import subprocess
from utils import run_command, download_file, run_as_admin, subprocess
from install_7z import install_7zip

def extract_archive(filename, destination):
    install_7zip()
    if filename.endswith(".zip"):
        with zipfile.ZipFile(filename, 'r') as zipf:
            zipf.extractall(destination)
    elif filename.endswith(".tar.gz") or filename.endswith(".tgz"):
        with tarfile.open(filename, 'r:gz') as tarf:
            tarf.extractall(destination)
    elif filename.endswith(".tar.bz2") or filename.endswith(".tbz2"):
        with tarfile.open(filename, 'r:bz2') as tarf:
            tarf.extractall(destination)
    elif filename.endswith(".7z"):
        # Use 7-Zip command line tool to extract the .7z archive
        seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"
        try:
            run_command(f'"{seven_zip_path}" x "{filename}" -o"{destination}" -y')
        except ValueError as e:
            raise ValueError("Failed to extract .7z archive using 7-Zip: " + str(e))
    else:
        raise ValueError("Unsupported archive format")

def add_to_path(directory):
    if platform.system() == "Windows":
        run_command(f'setx /m PATH "{directory};%PATH%"')
    else:
        with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
            bashrc.write(f'\nexport PATH="{directory}:$PATH"\n')
        run_command(["source", "~/.bashrc"])

def is_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_ffmpeg(download_url="https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"):
    if is_ffmpeg_installed():
        print("FFmpeg is already installed.")
        return
    run_as_admin()

    with tempfile.TemporaryDirectory() as temp_dir:
        archive_name = os.path.basename(download_url)
        archive_path = os.path.join(temp_dir, archive_name)
        print(f"Downloading FFmpeg from: {download_url}")
        if not download_file(download_url, archive_path):
            print("Download failed. Please provide a valid download link.")
            new_link = input("Enter the new download link: ")
            return install_ffmpeg(new_link)

        print("Extracting FFmpeg...")
        extract_archive(archive_path, temp_dir)

        ffmpeg_dir = os.path.join(temp_dir, "ffmpeg")
        os.makedirs(ffmpeg_dir, exist_ok=True)

        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file == "ffmpeg.exe" or file == "ffprobe.exe":
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(ffmpeg_dir, file)
                    shutil.copy2(src_path, dst_path)

        install_dir = os.path.expanduser("~/ffmpeg")
        if os.path.exists(install_dir):
            shutil.rmtree(install_dir)
        shutil.move(ffmpeg_dir, install_dir)

        print("Adding FFmpeg to system path...")
        add_to_path(install_dir)

        print("FFmpeg installation completed.")

if __name__ == "__main__":
    run_as_admin()
    # Default download link
    # Install FFmpeg
    install_ffmpeg()