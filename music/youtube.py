import os, time, subprocess
from config import DOWNLOAD_DIR

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def yt_download(query: str):
    filename = f"{DOWNLOAD_DIR}/{int(time.time())}.mp3"
    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", filename,
        f"ytsearch1:{query}"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return filename if os.path.exists(filename) else None
