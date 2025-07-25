import os
import subprocess
import datetime
import tkinter as tk
from tkinter import messagebox

# --- Helper Functions -------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """Remove characters that are not safe for Windows filenames."""
    return ''.join(c for c in name if c.isalnum() or c in ' _-').strip()

def download_audio_clip(url: str, start: str, end: str, out_dir: str = r"C:\\YoutubeCuts") -> str:
    """Download a segment of a YouTube video and convert it to MP3."""
    os.makedirs(out_dir, exist_ok=True)

    # Get video title
    try:
        title = subprocess.check_output(["yt-dlp", "--get-title", url], text=True).strip()
    except Exception:
        title = "video"
    safe_title = sanitize_filename(title)[:20] or "video"

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    temp_pattern = os.path.join(out_dir, f"temp_{timestamp}.%(ext)s")

    # Download only the selected section
    cmd_dl = [
        "yt-dlp",
        "-f", "bestaudio",
        "--download-sections", f"*{start}-{end}",
        "-o", temp_pattern,
        url
    ]
    subprocess.run(cmd_dl, check=True)

    # Find the downloaded file (yt-dlp replaces %%(ext)s)
    temp_file = None
    for f in os.listdir(out_dir):
        if f.startswith(f"temp_{timestamp}") and not f.endswith('.mp3'):
            temp_file = os.path.join(out_dir, f)
            break
    if not temp_file:
        raise FileNotFoundError("Downloaded file not found")

    mp3_name = f"{safe_title}_{timestamp}.mp3"
    mp3_path = os.path.join(out_dir, mp3_name)

    cmd_ff = [
        "ffmpeg", "-y", "-i", temp_file,
        "-vn", "-acodec", "libmp3lame",
        mp3_path
    ]
    subprocess.run(cmd_ff, check=True)

    os.remove(temp_file)
    return mp3_path

# --- GUI Application -------------------------------------------------------

class YoutubeCutterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube MP3 Cutter")
        self.geometry("400x220")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="YouTube URL:", bg="#f0f0f0").pack(pady=(10,0))
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5)

        tk.Label(self, text="Start time (mm:ss or hh:mm:ss):", bg="#f0f0f0").pack()
        self.start_entry = tk.Entry(self, width=20)
        self.start_entry.pack(pady=5)

        tk.Label(self, text="End time (mm:ss or hh:mm:ss):", bg="#f0f0f0").pack()
        self.end_entry = tk.Entry(self, width=20)
        self.end_entry.pack(pady=5)

        self.button = tk.Button(self, text="Download clip", command=self.on_download)
        self.button.pack(pady=15)
        self.button.bind("<Enter>", lambda e: self.button.config(bg="lightblue"))
        self.button.bind("<Leave>", lambda e: self.button.config(bg="SystemButtonFace"))

    def on_download(self):
        url = self.url_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        if not url or not start or not end:
            messagebox.showerror("Error", "Please fill out all fields")
            return
        try:
            output = download_audio_clip(url, start, end)
            messagebox.showinfo("Success", f"Saved to: {output}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

if __name__ == "__main__":
    app = YoutubeCutterApp()
    app.mainloop()
