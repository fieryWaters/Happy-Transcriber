import os
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
import tempfile
import shutil
import ctypes
import sys

def download_file(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        return True
    except urllib.error.URLError:
        return False

def extract_archive(filename, destination):
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
        try:
            subprocess.run(["7z", "x", f"-o{destination}", filename], check=True)
        except subprocess.CalledProcessError as e:
            raise ValueError("Failed to extract .7z archive using 7-Zip: " + str(e))
    else:
        raise ValueError("Unsupported archive format")

def add_to_path(directory):
    if platform.system() == "Windows":
        subprocess.run(f'setx /m PATH "{directory};%PATH%"', shell=True)
    else:
        with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
            bashrc.write(f'\nexport PATH="{directory}:$PATH"\n')
        subprocess.run(["source", "~/.bashrc"], shell=True)

def install_ffmpeg(download_url):
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

        print("FFmpeg installation completed successfully!")
        input("press enter")


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

    # Default download link
    default_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"

    # Install FFmpeg
    install_ffmpeg(default_url)

    input("enter")