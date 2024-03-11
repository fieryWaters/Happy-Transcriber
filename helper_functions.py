import subprocess

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None
    

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

save_requirements()