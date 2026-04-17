# ETHO — Windows AI Desktop Assistant

ETHO is a lightweight, keyboard-driven Windows desktop assistant that lets you control your PC, open apps and websites, organize files, generate code with a local AI model, and summarize documents — all from a single command bar triggered by a hotkey.

It also runs silently in the background with a Pomodoro-style work/break timer and periodic hydration reminders, delivered as native Windows desktop notifications.

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands Reference](#commands-reference)
- [Work Modes](#work-modes)
- [AI Features](#ai-features)
- [File Organization](#file-organization)

---

## Features

- **Global hotkey** (`Ctrl+Shift+Space`) — summons an inline command toast notification to type commands without switching windows
- **Floating command bar** — a custom, borderless Tkinter UI that appears in the bottom-right corner of the screen
- **App launcher** — open mapped applications by name
- **Website shortcuts** — open 25+ pre-mapped websites or fall back to a Bing search
- **File system** — create files (`.txt`, `.xlsx`, `.docx`) at any path and optionally open them immediately
- **Folder organizer** — sorts all top-level files in a directory into categorized subfolders (images, videos, documents, code, archives)
- **Everything search** — finds folders instantly using the [Everything](https://www.voidtools.com/) search engine CLI (`es.exe`)
- **Process manager** — list running apps by memory, launch apps, or kill processes by name
- **Document summarizer** — extracts text from PDF/DOCX/TXT and produces a bullet-point summary using LexRank, saved as a `_summary.txt` file
- **Code generator** — generates code using a local Ollama model (`qwen2.5-coder:0.5b`) and pastes it directly into the active window
- **Pomodoro work/break loop** — background async timer with two modes (90/30 min or 25/5 min)
- **Hydration reminders** — periodic water-drink notifications every 30 minutes
- **Mode switching** — toggle between default (90/30) and alternate (25/5) Pomodoro modes at runtime

---

## Architecture

```
Ctrl+Shift+Space (global hotkey)
        │
        ├─► command_toast()        ← inline reply field in notification
        │         │
        │         ▼
        │   execute_command(text)
        │
        └─► command_input()        ← floating Tkinter command bar
                  │
                  ▼
          execute_command(text)
                  │
        ┌─────────┼─────────────────────────────────┐
        │         │                                  │
      open      create      organize    summary    generate
        │                                  │           │
  ┌─────┴─────┐                      Summarizer.py  Code_Generator.py
  │           │                      (sumy + MarkItDown) (Ollama qwen2.5)
websites    apps
(webbrowser) (subprocess)
                         Background (asyncio)
                         ├── work_break_loop()   ← Pomodoro timer
                         └── reminder_loop()     ← Hydration every 30 min
```

---

## Project Structure

```
ETHO/
├── Constant_running_modes.py   # Async event loop: Pomodoro timer, hydration reminders, hotkey listener
├── Command_Executor.py         # Core command parser and executor — all commands live here
├── Launcher.py                 # Floating Tkinter command bar UI
├── Notifier.py                 # Desktop notifications (desktop_notifier) + sound (winsound)
├── Searching.py                # Everything search (es.exe) + process checker
├── Constants.py                # All config: app_map, websites, FILE_CATEGORIES, MODES, reminder lines
├── AI/
│   ├── Code_Generator.py       # Ollama-based code gen — generates and pastes via pyautogui
│   └── Summarizer.py           # Document summarizer (sumy LexRank + MarkItDown)
├── info/
│   └── organizer.log           # Log file for file organization operations
├── launcher.png                # Icon shown in the command bar UI (optional)
└── README.md
```

---

## Requirements

**Platform:** Windows only (uses `winsound`, `os.startfile`, `keyboard` global hotkey)

**Python:** 3.10+

**External tools that must be installed separately:**

| Tool | Purpose | Download |
|---|---|---|
| [Everything](https://www.voidtools.com/) | Folder search via `es.exe` | voidtools.com |
| [Ollama](https://ollama.com/) | Local LLM for code generation | ollama.com |
| `qwen2.5-coder:0.5b` model | The code generation model | `ollama pull qwen2.5-coder:0.5b` |

**Python dependencies** (install via pip):

```
desktop-notifier
keyboard
pyautogui
pyperclip
sumy
markitdown
openpyxl
python-docx
psutil
Pillow
```

Install all at once:

```bash
pip install desktop-notifier keyboard pyautogui pyperclip sumy markitdown openpyxl python-docx psutil Pillow
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/etho.git
cd etho

# 2. Install Python dependencies
pip install desktop-notifier keyboard pyautogui pyperclip sumy markitdown openpyxl python-docx psutil Pillow

# 3. Install and run Ollama (for code generation)
#    Download from https://ollama.com and then:
ollama pull qwen2.5-coder:0.5b

# 4. Install Everything (for folder search)
#    Download from https://www.voidtools.com/

# 5. Configure paths (see Configuration below)

# 6. Run ETHO
python Constant_running_modes.py
```

---

## Configuration

All configuration is in `Constants.py`. Edit it to match your system before running.

### App Paths (`app_map`)

Map short names to executable paths on your machine:

```python
app_map = {
    "vscode": r"C:\Path\To\Code.exe",
    "cmd":    r"C:\Windows\system32\cmd.exe",
    "everything": r"C:\Program Files\Everything\Everything.exe",
    # Add your own apps here
}
```

### Everything Search Path (`Searching.py`)

Update the `ES_PATH` variable to point to your `es.exe`:

```python
ES_PATH = r"C:\Program Files\Everything\es.exe"   # adjust to your install path
```

Also update `EVERYTHING_EXE` in `Constants.py` to point to the main `Everything.exe`.

### Notification Icon (`Notifier.py`)

Replace the placeholder with your logo path:

```python
notifier = DesktopNotifier(
    app_name="ETHO",
    app_icon=Path(r"C:\path\to\your\logo.png")   # update this
)
```

### Work Modes (`Constants.py`)

```python
MODES = {
    "default":   {"work": 90*60, "break": 30*60},   # 90 min work, 30 min break
    "alternate": {"work": 25*60, "break":  5*60}    # Classic Pomodoro
}
```

### Websites (`Constants.py`)

Add custom shortcuts to the `websites` dict:

```python
websites = {
    "myapp": "https://your-internal-tool.com",
    # ...
}
```

---

## Usage

### Starting ETHO

Run the main entry point to start the background loop (reminders + Pomodoro timer):

```bash
python Constant_running_modes.py
```

ETHO will show a welcome notification and begin running silently. It starts two background async tasks — the Pomodoro work/break loop and the 30-minute hydration reminder.

### Triggering the Command Bar

**Method 1 — Global hotkey:** Press `Ctrl+Shift+Space` from anywhere on your desktop. A desktop notification will appear with a reply field where you can type a command directly.

**Method 2 — Floating UI:** Call `command_input()` from `Launcher.py` to open the floating command bar window. It appears in the bottom-right corner of the screen, stays on top, and is draggable.

In either case, press `Enter` to execute, or `Escape` to dismiss.

---

## Commands Reference

| Command | Syntax | Description |
|---|---|---|
| `help` | `help` | List all available commands |
| `switch` | `switch` | Toggle between default (90/30) and alternate (25/5) Pomodoro mode |
| `open <site>` | `open youtube` | Open a mapped website; unknown names fall back to Bing search |
| `open <folder> <app>` | `open myproject vscode` | Find a folder with Everything and open it in the specified app |
| `create <path>` | `create F:/notes/todo.txt` | Create a file (`.txt`, `.xlsx`, `.docx`, or any format) |
| `create <path> open` | `create F:/notes/todo.txt open` | Create and immediately open the file |
| `organize <path>` | `organize F:/Downloads` | Organize all files in a folder into category subfolders |
| `summary <path>` | `summary F:/report.pdf` | Summarize a document and open the result |
| `generate <task>` | `generate python sort function` | Generate code via Ollama and paste it into the active window |
| `search <query>` | `search asyncio python` | Open Bing search for the given query |
| `list apps` | `list apps` | Show top 15 running processes by memory usage |
| `run <app>` | `run notepad` | Launch a mapped application |
| `kill <name>` | `kill chrome` | Kill all processes matching the name |

---

## Work Modes

ETHO manages your focus using an async Pomodoro-style loop running in the background.

**Default mode** (90 min work / 30 min break) — suited for deep work sessions.

**Alternate mode** (25 min work / 5 min break) — classic Pomodoro technique.

Switch modes at any time with the `switch` command. The current mode label is stored in `Constants.py` as `current_mode` and mutated at runtime by `switch_mode()` in `Constant_running_modes.py`.

At each interval boundary, ETHO sends a notification with a randomly chosen message from `break_lines` (break time) or `restart_lines` (back to work), keeping the tone intentionally terse and direct.

---

## AI Features

### Code Generator (`AI/Code_Generator.py`)

Uses a locally running **Ollama** instance with the `qwen2.5-coder:0.5b` model to generate code from a plain English prompt and paste it directly into whatever window is currently active.

**Flow:**
1. You type: `generate python binary search function`
2. ETHO runs the Ollama model locally (no internet required)
3. Strips any markdown formatting from the output
4. Notifies: *"Ready! Click where you want the code..."*
5. After a 2-second pause (for you to click into your editor), pastes via `Ctrl+V`
6. Restores your original clipboard contents

> Ollama must be running (`ollama serve`) and the model must be pulled before use.

### Document Summarizer (`AI/Summarizer.py`)

Summarizes any document into bullet-point key sentences using **LexRank** (graph-based extractive summarization via `sumy`).

**Supported formats:** PDF, DOCX, TXT, and any format supported by `MarkItDown`.

**Flow:**
1. You type: `summary F:/report.pdf`
2. ETHO estimates processing time based on file size and format
3. Extracts text using `MarkItDown`
4. Runs LexRank summarization (3 sentences by default)
5. Saves the result to `<original_filename>_summary.txt` in the same directory
6. Opens the summary file automatically

---

## File Organization

The `organize <path>` command sorts all files in the target directory's top level into named subfolders based on extension:

| Folder | Extensions |
|---|---|
| `images/` | `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp` |
| `videos/` | `.mp4`, `.mkv`, `.avi` |
| `documents/` | `.pdf`, `.docx`, `.txt`, `.xlsx` |
| `code/` | `.py`, `.js`, `.java`, `.cpp` |
| `archives/` | `.zip`, `.rar`, `.tar`, `.gz` |
| `others/` | Everything else |

Duplicate filenames are handled automatically by appending `_1`, `_2`, etc. Moves are atomic (write to `.tmp` first, then rename) to prevent data loss on interruption. All operations are logged to `info/organizer.log`.
