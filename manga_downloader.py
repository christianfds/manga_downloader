import argparse
import logging

from manga_provider.mangahost import MangaHost
from util.utils import format_manga


logger = logging.getLogger('manga_downloader')
handler = logging.StreamHandler()
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='manga_downloader')
    parser.add_argument(
        '--manga',
        required=True,
        help='Manga to be downloaded.')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug flag')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    provider = MangaHost()

    # Testing
    for manga in provider.find_mangas(args.manga):
        format_manga(manga)
