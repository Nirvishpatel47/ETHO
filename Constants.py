water_lines = [
    "Drink water.",
    "Hydrate. Now.",
    "You need water.",
    "Drink. Then continue."
]

break_lines = [
    "Stop. Rest.",
    "Take a break.",
    "Step away.",
    "Rest now.",
    "You're slowing down. Pause.",
    "Short break. Then return.",
    "Fatigue is showing.",
    "Pause. Reset.",
    "Step back.",
    "Break. Now."
]

restart_lines = [
    "Break is over. Continue.",
    "Resume.",
    "Back to work.",
    "Focus. Continue.",
    "Move.",
    "Enough pause.",
    "Continue working.",
    "Return to task.",
    "Work resumes.",
    "Proceed."
]

giyu_welcome_messages = [
    "You're here.",
    "Welcome.",
    "Good. You're here."
]

FILE_CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "videos": [".mp4", ".mkv", ".avi"],
    "documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "code": [".py", ".js", ".java", ".cpp"],
    "archives": [".zip", ".rar", ".tar", ".gz"],
}

app_map = {
            "notepad": "notepad.exe",
            "android studio": "studio64.exe",
            "vscode": r"E:\Microsoft VS Code\Code.exe",
            "vs": r"E:\Microsoft VS Code\Code.exe",
            "cmd": r"C:\Windows\system32\cmd.exe",
            "command": r"C:\Windows\system32\cmd.exe",
            "everything": r"C:\Program Files\Everything\Everything.exe",
            "es": r"C:\Program Files\Everything\Everything.exe"
        }

websites = {
        "youtube": "https://www.youtube.com",
        "yt": "https://www.youtube.com",
        "google": "https://www.google.com",
        "gmail": "https://mail.google.com",
        "drive": "https://drive.google.com",
        "maps": "https://maps.google.com",
        "translate": "https://translate.google.com",

        "bing": "https://www.bing.com",

        "github": "https://github.com",
        "stackoverflow": "https://stackoverflow.com",

        "chatgpt": "https://chat.openai.com",

        "linkedin": "https://www.linkedin.com",
        "twitter": "https://twitter.com",
        "x": "https://twitter.com",
        "instagram": "https://www.instagram.com",
        "insta": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",

        "amazon": "https://www.amazon.com",
        "flipkart": "https://www.flipkart.com",

        "netflix": "https://www.netflix.com",
        "prime": "https://www.primevideo.com",
        "hotstar": "https://www.hotstar.com",

        "reddit": "https://www.reddit.com",
        "wikipedia": "https://www.wikipedia.org"
    }

MODES = {
    "default": {"work": 90*60, "break": 30*60},
    "alternate": {"work": 25*60, "break": 5*60}
}

current_mode = "default"

EVERYTHING_EXE = r"C:\Program Files\Everything\Everything.exe"