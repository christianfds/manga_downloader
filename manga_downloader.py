import argparse
import logging
import os
import re
import shutil
from typing import List

from manga_provider.mangahost import MangaHost
from util.manga import Manga
from util.pdf import PdfUtils
from util.utils import FormatText, clear_tmp, dynamic_pad

logger = logging.getLogger("manga_downloader")
handler = logging.StreamHandler()
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)

SECTION_RANGE_ERROR_MSG = "Chapter selection has invalid type. Choices must be integer"


def validate_section_range(section_range: List[str]):
    for section in section_range:
        if not section.isdigit():
            raise TypeError(SECTION_RANGE_ERROR_MSG)


def parse_chapter_selection(selection: str) -> list[int]:
    chapters = []
    for section in selection.split(","):
        section_range = section.split("-")
        validate_section_range(section_range)
        if len(section_range) > 2:
            raise IndexError(f"Invalid range: {section}")
        elif len(section_range) == 2:
            chapters = chapters + list(
                range(int(section_range[0]), int(section_range[1]) + 1)
            )
        elif len(section_range) == 1:
            chapters = chapters + [int(section_range[0])]

    return chapters


def chose_manga(provider: MangaHost, manga_name: str, bulk_display: int = 5):
    chosen_manga = None
    manga_collection = {}
    for counter, manga in enumerate(provider.find_mangas(manga_name)):
        manga.show()
        manga_collection[manga.manga_id] = manga
        response = None
        if counter >= 1 and counter % bulk_display == 0:
            while not response:
                response = input(
                    FormatText.option("Type the desired manga id or C to continue: ")
                )
            if response == "C":
                continue
            else:
                try:
                    match_exists = re.match("^([-A-Za-z0-9])+$", response)
                    if match_exists:
                        chosen_manga = manga_collection[response]
                        break
                except KeyError:
                    print("Chosen manga ID doesn't exist")
                    quit(2)

    if chosen_manga is None:
        print("Couldn't find this manga")
        quit(0)
    return chosen_manga


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
    os.makedirs(output, exist_ok=True)
    shutil.move(path, output)


def manga_downloader(args: dict):
    clear_tmp()

    provider = MangaHost()
    try:
        manga = chose_manga(provider, args.manga)
        selected_chapters, chapters = select_chapters(provider, manga)
        # TODO Run all operations below atomic for each chapter
        all_folders = download_chapters(provider, manga, selected_chapters, chapters)
    except (TypeError, IndexError) as error:
        print(error)
        quit(1)

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
