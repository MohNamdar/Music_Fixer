import os
import io
import re
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
from mutagen.mp3 import MP3, HeaderNotFoundError
from pydub import AudioSegment
from PIL import Image
from .utils import logger




def safe_load_mp3(path):
    try:
        return MP3(path, ID3=EasyID3)
    except (HeaderNotFoundError, ID3NoHeaderError):
        # If file is bad -> Re-encoding with pydub
        logger.log(f"⚠️ File invalid or not MP3: {os.path.basename(path)}. Re-encoding...")
        temp_path = path + ".tmp.mp3"
        sound = AudioSegment.from_file(path)
        sound.export(temp_path, format="mp3", bitrate="320k")
        del sound
        os.replace(temp_path, path)
        return MP3(path, ID3=EasyID3)


def set_tags_cover(file_path, title=None, artist=None, album=None, year=None, cover_path=None):
    if not os.path.exists(file_path):
        logger.log(f"❌ File not found: {file_path}")
        return

    audio = safe_load_mp3(file_path)

    if title:
        audio["title"] = title
    if artist:
        audio["artist"] = artist
    if album:
        audio["album"] = album
    if year:
        audio["date"] = str(year)
    audio.save()

    # Adding Cover
    if cover_path and os.path.exists(cover_path):
        with Image.open(cover_path) as im:
            im.thumbnail((800, 800))
            bio = io.BytesIO()
            im.save(bio, format='JPEG')
            img_bytes = bio.getvalue()

        audio = MP3(file_path, ID3=ID3)
        if not audio.tags:
            audio.add_tags()
        audio.tags.delall('APIC')
        audio.tags.add(APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=img_bytes
        ))
        audio.save(v2_version=3)
        
        # count the number of music fixed
        logger.count_cover_change()

        logger.log(f"🖼️ Cover added for: {os.path.basename(file_path)}")

        # Remove Image file after done the cover fixing
        os.remove(cover_path)
    else:
        logger.add_not_fixed(file_path)

    # rename file to the certain format
    if title and artist:
        new_filename = f"{title} - {artist}.mp3"
        # remvove unnecessary characters
        new_filename = re.sub(r'[\\/:"*?<>|]+', '', new_filename)
        new_path = os.path.join(os.path.dirname(file_path), new_filename)
        if os.path.abspath(file_path) != os.path.abspath(new_path):
            os.rename(file_path, new_path)
            file_path = new_path
            logger.log(f"📝 File renamed to: {new_filename}")
    
    logger.log(f"✅ Tags saved successfully for: {os.path.basename(file_path)}")    

    return file_path


