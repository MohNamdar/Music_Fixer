import os
import glob
from .utils import logger
from icrawler.builtin import GoogleImageCrawler


IMAGE_FOLDER = "images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def download_cover(query):
    try:
        crawler = GoogleImageCrawler(storage={'root_dir': IMAGE_FOLDER})
        crawler.crawl(
            keyword=query,
            max_num=1,
            overwrite=True
        )
        last_file = max(glob.glob(f'{IMAGE_FOLDER}/*'), key=os.path.getctime)
        new_path = os.path.join(IMAGE_FOLDER, f'{query}.jpg')
        if os.path.exists(new_path):
            os.remove(new_path)
        os.rename(last_file, new_path)
        logger.log(f'cover saved in ({new_path})')
        return new_path
    except Exception as e:
        logger.log(f'!Error downloading cover for "{query}": {e}')
        return None
