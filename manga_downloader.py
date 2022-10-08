import argparse
import logging
import shutil
import typing

from manga_provider.mangahost import MangaHost
from util.manga import Manga
from util.pdf import PdfUtils
from util.utils import FormatText, clear_tmp, dynamic_pad

logger = logging.getLogger("manga_downloader")
handler = logging.StreamHandler()
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_chapter_selection(selection: str) -> typing.List[int]:
    chapters = []
    for section in selection.split(","):
        section_range = section.split("-")
        if len(section_range) > 2:
            raise IndexError(f"Invalid range: {section}")
        elif len(section_range) == 2:
            chapters = chapters + list(
                range(int(section_range[0]), int(section_range[1]) + 1)
            )
        elif len(section_range) == 1:
            chapters = chapters + [int(section_range[0])]

    return chapters


def chose_manga(provider: MangaHost, manga_name: str):
    chosen_manga = None
    for manga in provider.find_mangas(manga_name):
        manga.show()
        response = None
        while response not in ("Y", "N"):
            response = input(FormatText.option("Download this manga? Y/N  ")).upper()

        if response == "N":
            continue
        elif response == "Y":
            chosen_manga = manga
            break

    if chosen_manga is None:
        print("Couldn't find this manga")
        quit(0)
    return manga


def select_chapters(provider: MangaHost, manga: Manga):
    chapters = provider.find_manga_chapters(manga)

    for index, elem in enumerate(chapters, 1):
        print(("{} - Chapter #{}").format(dynamic_pad(len(chapters), index), elem))

    response = input(FormatText.option("Which indexes to download?  "))
    selected_chapters = parse_chapter_selection(response)
    return selected_chapters, chapters


def download_chapters(provider: MangaHost, manga: Manga, selected_chapters, chapters):
    all_folders = []
    for chapter in selected_chapters:
        folder, _ = provider.download_chapter(manga, chapters[chapter - 1])
        all_folders.append(folder)
    return all_folders


def move_to_output(path: str, output: str):
    shutil.move(path, output)


def manga_downloader(args: dict):
    clear_tmp()

    provider = MangaHost()

    manga = chose_manga(provider, args.manga)

    selected_chapters, chapters = select_chapters(provider, manga)

    # TODO Run all operations below atomic for each chapter
    all_folders = download_chapters(provider, manga, selected_chapters, chapters)

    if not args.image:
        result_pdfs = PdfUtils.convert_multiple_folders_to_pdf(all_folders)
        results = result_pdfs
    else:
        results = all_folders

    for f in results:
        move_to_output(f, args.output)

    clear_tmp()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="manga_downloader")
    parser.add_argument("-m", "--manga", required=True, help="Manga to be downloaded.")
    parser.add_argument("-o", "--output", required=True, help="Output folder.")
    parser.add_argument(
        "--image", action="store_true", help="Store downloaded chapter as images."
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug flag")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    manga_downloader(args)
