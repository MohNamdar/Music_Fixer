import re
import os
from datetime import datetime

LOG_FILE = "logs/log.txt"
os.makedirs("logs", exist_ok=True)


class Logger():

    def __init__(self):
        self.cover_changed_count = 0
        self.not_fixed_musics = []

    def count_cover_change(self):
        self.cover_changed_count += 1

    def add_not_fixed(self, query):
        self.not_fixed_musics.append(query)

    def summary(self):
        message = f"✅ Total covers changed: {self.cover_changed_count} \n\n‼️ not fixed musics: \n{"\n".join(self.not_fixed_musics)}"
        self.log(message, level="SUMMERY")

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
    filename = re.sub(r'[\\/:"*?<>|]+', '', filename)
    return filename
