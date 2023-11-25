import subprocess
import time

def run_script():
    while True:
        print("Starting main script...")
        process = subprocess.Popen(['python', 'slimeocr.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()
        if stdout:
            print(f"Standard Output: {stdout.decode('utf-8')}")
        if stderr:
            print(f"Error: {stderr.decode('utf-8')}")

        print("Restarting main script in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    run_script()
