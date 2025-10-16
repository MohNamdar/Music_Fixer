import re
import os
from datetime import datetime

LOG_FILE = "logs/log.txt"
os.makedirs("logs", exist_ok=True)


class Logger():

    def __init__(self):
        self.cover_changed_count = 0

    def count_cover_change(self):
        self.cover_changed_count += 1

    def summary(self):
        self.log(
            f"✅ Total covers changed: {self.cover_changed_count}", level="SUMMERY")

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"[{timestamp}] [{level}] {message}"
        print(text)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")


logger = Logger()


def clean_music_filename(filename: str) -> str:
    filename = re.sub(r'\.\w+$', '', filename)
    filename = re.sub(r'\d+', '', filename)
    filename = filename.replace('_', ' ').replace('-', ' ')
    filename = re.sub(r'\(.*?\)', '', filename)
    filename = re.sub(r'\[.*?\]', '', filename)
    filename = re.sub(r'\s+', ' ', filename).strip()
    return filename
