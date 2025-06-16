import tkinter as tk
from pynput.mouse import Listener
from datetime import datetime
import threading
from PIL import Image, ImageTk

# ---  Colors ---
BACKGROUND_COLOR = "#f0f0f0"
TEXT_COLOR = "#333333"
ACCENT_COLOR = "#007bff"

try:
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((100, 50))
    logo_image = ImageTk.PhotoImage(logo_image)
except FileNotFoundError:
    logo_image = None  

def on_click(x, y, button, pressed):
    if pressed:
        click_type = "Left Click" if button.name == "left" else "Right Click"
        click_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        display_click_info(click_type, x, y, click_time)

def display_click_info(click_type, x, y, click_time):
    text_area.insert(tk.END, f"{click_type} at ({x}, {y}) on {click_time}\n")
    text_area.see(tk.END)

def start_listener():
    with Listener(on_click=on_click) as listener:
        listener.join()

root = tk.Tk()
root.title("Mouse Click Logger")
root.configure(bg=BACKGROUND_COLOR)

try:
    root.iconbitmap("app_icon.ico")
except tk.TclError:
    print("Icon file not found or not supported on this OS.")

header_frame = tk.Frame(root, bg=ACCENT_COLOR)
header_frame.pack(side=tk.TOP, fill=tk.X)

if logo_image:
    logo_label = tk.Label(header_frame, image=logo_image, bg=ACCENT_COLOR)
    logo_label.pack(side=tk.LEFT, padx=10)

header_label = tk.Label(header_frame, text="Mouse Click Logger",
                        font=("Arial", 16, "bold"), fg="white", bg=ACCENT_COLOR)
header_label.pack(side=tk.LEFT, padx=10)

text_area = tk.Text(root, width=50, height=20, font=("Arial", 12),
                    bg="white", fg=TEXT_COLOR, wrap=tk.WORD)
text_area.pack(padx=10, pady=10)

footer_frame = tk.Frame(root, bg=ACCENT_COLOR)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

def update_copyright_year():
    current_year = datetime.now().year
    copyright_label.config(text=f"© {current_year} by @gevitop. All rights reserved.")
    root.after(1000 * 60 * 60 * 24, update_copyright_year)

copyright_label = tk.Label(footer_frame, text="",
                            font=("Arial", 10), fg="white", bg=ACCENT_COLOR)
copyright_label.pack(side=tk.RIGHT, padx=10)

update_copyright_year()

listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()

root.mainloop()
