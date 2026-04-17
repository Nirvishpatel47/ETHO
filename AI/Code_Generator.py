import subprocess
import pyperclip
import pyautogui
import time
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Notifier import notify_user 

def inject_code(user_prompt):
    """
    Generates code using Qwen2.5-Coder and pastes it immediately.
    """
    model_name = "qwen2.5-coder:0.5b"
    # Added instructions to strip Markdown formatting for a clean paste
    system_instruction = (
        "You are an expert programmer. Provide only the code. "
        "No chat, no intro, no 'Here is your code'. Just the raw code block."
    )

    try:
        # 1. Start generation immediately
        result = subprocess.run(
            ["ollama", "run", model_name, f"{system_instruction}\nTask: {user_prompt}"],
            capture_output=True, text=True, encoding='utf-8'
        )
        
        # 2. Clean up output (just in case the model adds backticks)
        generated_code = result.stdout.strip().replace("```python", "").replace("```java", "").replace("```", "")

        if not generated_code:
            notify_user("Generation failed: Empty output.")
            return

        # 3. Inform the user and wait for cursor placement
        # 2 seconds is usually the 'sweet spot' for speed vs. reaction time
        notify_user("Ready! Click where you want the code...")
        time.sleep(2)

        # 4. Perform the Paste
        original_clipboard = pyperclip.paste()
        pyperclip.copy(generated_code)
        
        # Cross-platform hotkey
        hotkey = 'command' if pyautogui.platform == 'darwin' else 'ctrl'
        pyautogui.hotkey(hotkey, 'v')

        # 5. Cleanup
        time.sleep(0.5) 
        pyperclip.copy(original_clipboard) # Restore user's previous clipboard

    except Exception as e:
        notify_user("Injection error. Check Ollama status.")
        print(f"Error: {e}")

if __name__ == "__main__":
    inject_code("Python add function")