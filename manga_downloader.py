import argparse
import logging
import typing
from util.manga import Manga

from util.utils import FormatText, dynamic_pad
from util.pdf import PdfUtils
from manga_provider.mangahost import MangaHost


logger = logging.getLogger('manga_downloader')
handler = logging.StreamHandler()
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_chapter_selection(selection: str) -> typing.List[int]:
    chapters = []
    for section in selection.split(','):
        section_range = section.split('-')
        if len(section_range) > 2:
            raise IndexError(f'Range invalido: {section}')
        elif len(section_range) == 2:
            chapters = chapters + list(range(int(section_range[0]), int(section_range[1]) + 1))
        elif len(section_range) == 1:
            chapters = chapters + [int(section_range[0])]

    return chapters


def chose_manga(provider: MangaHost):
    chosen_manga = None
    for manga in provider.find_mangas(args.manga):
        manga.show()
        response = None
        while response not in ('S', 'N'):
            response = input(FormatText.option('Deseja baixar este manga? S/N  ')).upper()

        if response == 'N':
            continue
        elif response == 'S':
            chosen_manga = manga
            break

    if chosen_manga is None:
        print("O seu manga desejado não foi encontrado")
        quit(0)
    return manga


def select_chapters(provider: MangaHost, manga: Manga):
    chapters = provider.find_manga_chapters(manga)

    for index, elem in enumerate(chapters, 1):
        print(('{} - Capítulo #{}').format(dynamic_pad(len(chapters), index), elem))

    response = input(FormatText.option('Quais indices deseja baixar?  '))
    selected_chapters = parse_chapter_selection(response)
    return selected_chapters, chapters


def download_chapters(provider: MangaHost, manga: Manga, selected_chapters, chapters):
    all_folders = []
    for chapter in selected_chapters:
        folder, _ = provider.download_chapter(manga, chapters[chapter - 1])
        all_folders.append(folder)
    return all_folders


def manga_downloader(args: dict):
    provider = MangaHost()

    manga = chose_manga(provider)

    selected_chapters, chapters = select_chapters(provider, manga)

    all_folders = download_chapters(provider, manga, selected_chapters, chapters)

    if not args.image:
        _ = PdfUtils.convert_multiple_folders_to_pdf(all_folders)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='manga_downloader')
    parser.add_argument(
        '-m', '--manga',
        required=True,
        help='Manga to be downloaded.')
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output folder.')
    parser.add_argument(
        '--image',
        action='store_true',
        help='Store downloaded chapter as images.')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug flag')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    manga_downloader(args)
