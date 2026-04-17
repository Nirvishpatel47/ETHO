from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from markitdown import MarkItDown
import subprocess
import platform
import time
import os
import sys
from pathlib import Path

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Notifier import notify_user

def get_estimated_time(file_path):
    """Calculates heuristic estimation based on format and size."""
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        est = 0.5 + (file_size_mb * 1)
    elif ext == '.docx':
        est = 1.5 + (file_size_mb * 2)
    elif ext == '.pdf':
        est = 2.0 + (file_size_mb * 5)
    else:
        est = 1.0 + (file_size_mb * 2)
        
    return round(est)

def summarize_with_metrics(file_path, sentence_count=3):

    file_path = Path(file_path.strip().strip('"')).resolve()

    if not os.path.exists(file_path):
        notify_user(f"Error: File not found at {file_path}")
        return

    # 1. Estimation Phase
    file_name = os.path.basename(file_path)
    est_seconds = get_estimated_time(file_path)
    
    if est_seconds > 5:
        notify_user(f"Starting summary for '{file_name}'. Estimated time: {est_seconds} seconds.")
    else:
        notify_user(f"Summarizing '{file_name}'...")

    # 2. Processing Phase
    start_time = time.time()
    try:
        # Extraction
        md = MarkItDown()
        result = md.convert(file_path)
        text = result.text_content
        
        # Summarization
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentence_count)
        
        duration = time.time() - start_time

        # 3. Save and Open
        output_path = f"{os.path.splitext(file_path)[0]}_summary.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"SUMMARY GENERATED IN {duration:.2f} SECONDS\n")
            f.write("="*40 + "\n\n")
            for sentence in summary:
                f.write(f"- {sentence}\n")

        # Final Notification
        notify_user(f"Summary complete for '{file_name}' ({duration:.1f}s).")
        open_file(output_path)

    except Exception as e:
        notify_user(f"Failed to summarize '{file_name}': {str(e)}")

def open_file(path):
    """Cross-platform command to open a file in the default editor."""
    current_os = platform.system()
    if current_os == "Windows":
        os.startfile(path)
    elif current_os == "Darwin":  # macOS
        subprocess.call(["open", path])
    else:  # Linux
        subprocess.call(["xdg-open", path])

if __name__ == "__main__":
    summarize_with_metrics(r"F:\Research\papers\Reletivity\gr.txt", sentence_count=10)