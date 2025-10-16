import os
import glob
from handlers.utils import logger
from handlers.converter import process_music_file

# Directories
MUSIC_FOLDER = "musics" # musics you want to fix
IMAGE_FOLDER = "images" # Saving cover images


# get all musics in the directory
music_files = glob.glob(os.path.join(MUSIC_FOLDER, '*.mp3')) + \
    glob.glob(os.path.join(MUSIC_FOLDER, '*.m4a'))

# process each music in musics directory
for file_path in music_files:
    process_music_file(file_path)

# summery after process
logger.summary()
