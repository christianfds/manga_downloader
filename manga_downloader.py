import argparse
import logging

from manga_provider.mangahost import MangaHost


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
        manga.show()
        chapters = provider.find_manga_chapters(manga)

        max_size = len(str(len(chapters)))
        int_format = f':0{max_size}d'
        for index, elem in enumerate(chapters, 1):
            print(('{' + int_format + '} - ' + '{}').format(index, elem))

        break
