from AI.Code_Generator import inject_code
from Searching import search_everything
from Notifier import notify_user
from Constants import app_map, websites, FILE_CATEGORIES
from pathlib import Path
import subprocess
import webbrowser
import logging
import urllib
import shutil
import psutil
import os

#Helper Coommands

logging.basicConfig(
    filename="info\organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_category(file_suffix):
    for category, extensions in FILE_CATEGORIES.items():
        if file_suffix.lower() in extensions:
            return category
    return "others"


def organize_top_level(parent_path):
    parent = Path(parent_path).resolve()

    # --- Validation ---
    if not parent.exists() or not parent.is_dir():
        raise ValueError("Invalid directory path")

    for item in parent.iterdir():

        # Skip non-files early
        if not item.is_file():
            continue

        try:
            category = get_category(item.suffix)

            target_dir = (parent / category).resolve()

            # Prevent self-move edge case
            if item.parent == target_dir:
                continue

            target_dir.mkdir(parents=True, exist_ok=True)

            target_file = target_dir / item.name

            # --- Safer duplicate handling ---
            if target_file.exists():
                counter = 1
                while True:
                    candidate = target_dir / f"{item.stem}_{counter}{item.suffix}"
                    if not candidate.exists():
                        target_file = candidate
                        break
                    counter += 1

            # --- Atomic move (safer) ---
            temp_target = target_file.with_suffix(target_file.suffix + ".tmp")

            shutil.move(str(item), str(temp_target))
            temp_target.rename(target_file)

            logging.info(f"Moved: {item} -> {target_file}")

        except Exception as e:
            logging.error(f"Failed to process {item}: {e}")
            continue  # continue processing other files safely

    notify_user("Organisation Complete.")

def normalize_path(raw_path: str) -> Path:
    p = raw_path.strip()

    # Fix missing colon after drive letter: F/ -> F:/
    if len(p) >= 2 and p[1] == "/":
        p = p[0] + ":/" + p[2:]

    # Normalize slashes
    p = p.replace("\\", "/")

    return Path(p)

def execute_command(cmd: str = None):

    if cmd == None:
        notify_user("Not executed.")

    if cmd.lower() == "help":
        notify_user("switch | open <url> | open <folder> <app> | create <path> | create <path> open | organize <path> | summary <path> | generate <task>")
        return
    
    if cmd.lower() == "switch":
        from Constant_running_modes import switch_mode
        switch_mode()

    parts = cmd.strip().split()
    action = parts[0].lower() if len(parts) > 0 else ""
    reaction = parts[1] if len(parts) > 1 else ""

    print(reaction)

    if action == "open":
        if len(parts) > 2:
            action_after_reaction = parts[2]
            path = search_everything(reaction)
            app = app_map.get(action_after_reaction)
            try:
                subprocess.Popen([app, path])
                notify_user("Done. Now Work.")
                return
            except Exception as e:
                notify_user("Failed")
                return
        else:
            url = websites.get(reaction.lower()) or f"https://www.bing.com/search?q={reaction.replace(' ', '+')}"
            webbrowser.open(url)
            notify_user(f"Opened: {reaction}")
            return

    elif action == "create":
        try:
            path = normalize_path(reaction)

            # Ensure it has a file name
            if path.name == "":
                return "Invalid path: no file name"

            # Create parent directories if not exist
            path.parent.mkdir(parents=True, exist_ok=True)

            # Create file based on extension
            ext = path.suffix.lower()

            if ext == ".txt":
                path.write_text("")  # empty file

            elif ext == ".xlsx":
                from openpyxl import Workbook
                wb = Workbook()
                wb.save(path)

            elif ext == ".docx":
                from docx import Document
                doc = Document()
                doc.save(path)

            else:
                # Default: just create empty file
                path.touch()
            
            if len(parts) > 2:
                if parts[2] == "open":
                    os.startfile(path)
                    notify_user(f"Opened: {path}")
                    return

            notify_user(f"File created: {path}")

            return 

        except Exception as e:
            notify_user("Do it yourself.")
            return 
        
    elif action == "organize":
        try:
            organize_top_level(reaction)

        except Exception:
            notify_user("Organize it yourself.")
    
    elif action == "summary" or action == "summarize":
        try:
            from AI.Summarizer import summarize_with_metrics
            
            if reaction and isinstance(reaction, str):
                summarize_with_metrics(reaction)
            else:
                notify_user("I need a valid file path to summarize.")
                
        except ImportError:
            notify_user("Summarizer module missing. Check your AI folder.")
        except Exception:
            notify_user("Summarize by yourself! (Or check if the file is open elsewhere)")

    elif action == "generate":
        try:
            full_prompt = " ".join(parts[1:])
            
            if full_prompt:
                inject_code(full_prompt)
            else:
                notify_user("What should I generate?")
                
        except ImportError:
            notify_user("Generator module missing.")
        except Exception as e:
            print(f"Error: {e}")
            notify_user("Generate it yourself!")

    elif action == "search":
        query = " ".join(parts[1:])
        
        if query:
            encoded_query = urllib.parse.quote_plus(query)
            
            search_url = f"https://www.bing.com/search?q={encoded_query}"
            
            webbrowser.open(search_url)
            notify_user(f"Searching for: {query}")
        else:
            notify_user("What should I search for?")

    elif action == "list" and reaction == "apps":
        processes = []
        for proc in psutil.process_iter(['name', 'memory_percent']):
            processes.append(proc.info)
        
        # Sort by memory and get unique names
        sorted_apps = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)
        unique_names = list(set([p['name'] for p in sorted_apps[:15]]))
        
        notify_user(f"Running: {', '.join(unique_names)}")

    elif action == "run":
        app_name = " ".join(parts[1:])
        app_path = app_map.get(app_name)
        try:
            subprocess.Popen(app_path)
            notify_user(f"Launching {app_name}...")
        except Exception:
            notify_user(f"Could not find {app_name}.")

    elif action == "kill":
        app_target = " ".join(parts[1:]).lower()
        found = False
        for proc in psutil.process_iter(['name']):
            if app_target in proc.info['name'].lower():
                proc.kill()
                found = True
        
        notify_user(f"Terminated {app_target}." if found else f"{app_target} not running.")
    else:
        notify_user("You must write clearly!")

if __name__ == "__main__":
    pass