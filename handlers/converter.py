import os
from .utils import clean_music_filename
from .utils import logger
from .downloader import download_cover
from mutagen import File
from .tagger import set_tags_cover
from pydub import AudioSegment


def process_music_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    new_file_path = file_path

    # M4A →
    if ext == ".m4a":
        new_file_path = os.path.splitext(file_path)[0] + ".mp3"
        try:
            sound = AudioSegment.from_file(file_path, format="m4a")
            sound.export(new_file_path, format="mp3", bitrate="320k")
            del sound
            os.remove(file_path)
            logger.log(f"🔁 Converted M4A to MP3: {os.path.basename(new_file_path)}")
        except Exception as e:
            logger.log(f"❌ Error converting to MP3: {e}")
            return

    # extract title and artist
    audio_meta = File(new_file_path, easy=True)
    if audio_meta:
        title = audio_meta.get('title', [None])[0]
        artist = audio_meta.get('artist', [None])[0]
    else:
        title = None
        artist = None

    if not title or not artist:
        filename = os.path.basename(new_file_path)
        clean_name = clean_music_filename(filename)
        parts = clean_name.split('-', 1)
        if len(parts) == 2:
            artist = parts[0].strip()
            title = parts[1].strip()
        else:
            title = clean_name
            artist = "Unknown"

    title = clean_music_filename(title)
    artist = clean_music_filename(artist)

    # create query for searching the cover image
    if not artist or "unknown" in artist.lower():
        query = title + " music"
    else:
        query = f"{title} - {artist}"

    logger.log(f'🎵 Searching cover for: "{query}"')
    cover_path = download_cover(query)

    set_tags_cover(
        file_path=new_file_path,
        title=title,
        artist=artist,
        album=title + '(single)',
        cover_path=cover_path
    )
    


