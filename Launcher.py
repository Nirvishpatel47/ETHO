import os
import tkinter as tk
from Command_Executor import execute_command

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def command_input():
    def submit(event=None):
        text = entry.get("1.0", "end-1c").strip()
        if text:
            root.destroy()
            execute_command(text)
        return "break"

    def close_app(event=None):
        root.destroy()

    def start_move(event):
        root._drag_x = event.x_root
        root._drag_y = event.y_root

    def on_move(event):
        dx = event.x_root - root._drag_x
        dy = event.y_root - root._drag_y
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.geometry(f"+{x}+{y}")
        root._drag_x = event.x_root
        root._drag_y = event.y_root

    def focus_input():
        root.update_idletasks()
        root.deiconify()
        root.lift()
        root.attributes("-topmost", True)
        root.focus_force()

        root.after(30, lambda: entry.focus_force())
        root.after(50, lambda: entry.mark_set("insert", "end"))
        root.after(70, lambda: entry.see("insert"))
        root.after(120, lambda: root.attributes("-topmost", False))

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.config(bg="#0b0d12")

    width = 520
    height = 138

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    margin_x = 16
    margin_y = 52

    pos_x = screen_w - width - margin_x
    pos_y = screen_h - height - margin_y
    root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    shadow = tk.Frame(root, bg="#0a0c10")
    shadow.pack(fill="both", expand=True, padx=0, pady=0)

    card = tk.Frame(
        shadow,
        bg="#151922",
        highlightthickness=1,
        highlightbackground="#2b3140"
    )
    card.place(x=0, y=0, width=width, height=height)

    left_w = 138
    image_panel = tk.Frame(card, bg="#1d2330")
    image_panel.place(x=0, y=0, width=left_w, height=height)

    image_label = tk.Label(
        image_panel,
        bg="#1d2330",
        bd=0
    )
    image_label.place(x=0, y=0, width=left_w, height=height)

    image_path = "launcher.png"

    if os.path.exists(image_path):
        try:
            if PIL_AVAILABLE:
                img = Image.open(image_path)
                img = img.resize((left_w, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                image_label.configure(image=photo)
                image_label.image = photo
            else:
                fallback = tk.Label(
                    image_panel,
                    text="IMG",
                    fg="#8ad7ff",
                    bg="#1d2330",
                    font=("Segoe UI Semibold", 18)
                )
                fallback.place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            image_label.configure(
                text="⌘",
                fg="#8ad7ff",
                bg="#1d2330",
                font=("Segoe UI Symbol", 28)
            )
    else:
        image_label.configure(
            text="⌬",
            fg="#8ad7ff",
            bg="#1d2330",
            font=("Segoe UI Symbol", 28)
        )

    right = tk.Frame(card, bg="#151922")
    right.place(x=left_w, y=0, width=width - left_w, height=height)

    title = tk.Label(
        right,
        text="Type! Now.",
        bg="#151922",
        fg="#f3f6fb",
        font=("Segoe UI Semibold", 11)
    )
    title.place(x=18, y=14)

    subtitle = tk.Label(
        right,
        text="",
        bg="#151922",
        fg="#8c97ab",
        font=("Segoe UI", 9)
    )
    subtitle.place(x=18, y=34)

    close_btn = tk.Label(
        right,
        text="✕",
        bg="#151922",
        fg="#96a0b2",
        font=("Segoe UI", 10),
        cursor="hand2"
    )
    close_btn.place(x=width - left_w - 28, y=12)
    close_btn.bind("<Button-1>", close_app)

    input_box = tk.Frame(
        right,
        bg="#0f131b",
        highlightthickness=1,
        highlightbackground="#313a4a"
    )
    input_box.place(x=18, y=62, width=width - left_w - 36, height=52)

    entry = tk.Text(
        input_box,
        bd=0,
        relief="flat",
        wrap="word",
        bg="#0f131b",
        fg="#ffffff",
        insertbackground="#ffffff",
        font=("Cascadia Code", 13),
        padx=12,
        pady=10,
        height=2
    )
    entry.place(x=0, y=0, width=width - left_w - 36, height=52)

    entry.bind("<Return>", submit)
    root.bind("<Escape>", close_app)

    for widget in (card, image_panel, right, title, subtitle):
        widget.bind("<Button-1>", start_move)
        widget.bind("<B1-Motion>", on_move)

    root.after(10, focus_input)
    root.mainloop()