import subprocess
import psutil
from Constants import EVERYTHING_EXE

ES_PATH = r"F:\Downloads\ES\es.exe"

def search_everything(folder_name):
    
    query = f"folder:{folder_name}"

    try:
        result = subprocess.run(
            [ES_PATH, "-n", "1", query],   # return only 1 result
            capture_output=True,
            text=True
        )

        path = result.stdout.strip()

        if path:
            return path

    except Exception as e:
        print("Search error:", e)

    return None

def ensure_everything_running():
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if name and name.lower() == "everything.exe" or name and name.lower() == "es.exe":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Not running → start it
    subprocess.Popen(EVERYTHING_EXE)
    return False


if __name__ == "__main__":
    print(ensure_everything_running())