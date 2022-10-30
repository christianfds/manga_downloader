import logging
import os
import re
import typing

from bs4 import BeautifulSoup

from manga_provider.generic import MangaProvider
from util.manga import Manga

logger = logging.getLogger("manga_downloader.manga_provider.mangahost")


SETTINGS = {
    "base_url": "https://mangahostz.com",
    "find_path": "find",
    "manga_path": "manga",
    "manga_chapter_path": "manga",
    "manga_link_regex": r"https://mangahostz.com/manga/\S+",
}


class MangaHost(MangaProvider):
    def __init__(self) -> None:
        super().__init__(**SETTINGS)

    def get_headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
        }

    def download_chapter(
        self, manga: Manga, manga_chapter: str
    ) -> tuple[str, list[str]]:
        list_imgs = self.find_chapter_pages(manga, manga_chapter)

        folder_path = os.path.join(
            ".tmp", manga.title, f"{manga.title} - Capitulo #{manga_chapter}"
        )

        print(f"Downloading chapter {manga_chapter}")
        downloaded_paths = self.download_all_images(list_imgs, folder_path)

        return folder_path, downloaded_paths

    @staticmethod
    def encode_manga_name(manga_name: str) -> str:
        return manga_name.replace(" ", "+")

    @staticmethod
    def extract_manga_id(uri: str) -> str:
        return uri.split("/")[-1]

    def find_mangas(self, manga_name: str) -> typing.Iterable[Manga]:
        manga_name = self.encode_manga_name(manga_name)
        search = "/".join([self.base_url, self.find_path, manga_name])

        request_result = self.perform_request_html(search)
        soup = BeautifulSoup(request_result, features="html.parser")

        table = soup.find("table")

        counter = 0
        for row in table.findAll("td"):
            if counter % 2:
                manga_link = row.find("a")["href"]
                if re.match(self.manga_link_regex, manga_link):
                    mg = Manga(
                        row.find("a")["title"],
                        manga_link,
                        alternative_title=[
                            title for title in row.find("span").text.split(",") if title
                        ],
                        description=row.find("div", {"class": "entry-content"})
                        .text.strip()
                        .replace("\r\n", " "),
                        manga_id=MangaHost.extract_manga_id(manga_link),
                    )
                    logger.debug(mg)
                else:
                    print("Manga contains invalid link")
                yield mg

            counter = counter + 1

    def find_manga_chapters(self, manga: Manga) -> list[str]:
        search = "/".join([self.base_url, self.manga_path, manga.manga_id])

        request_result = self.perform_request_html(search)
        soup = BeautifulSoup(request_result, features="html.parser")

        chapters_element = soup.find("div", {"class": "chapters"})
        chapters = [
            cap.text for cap in chapters_element.findAll("a", {"class": "btn-caps"})
        ]
        logger.debug("All queried chapters:")
        logger.debug(chapters)

        numeric_chapter = [cap for cap in chapters if cap.replace(".", "").isdigit()]
        logger.debug("All numeric chapters:")
        logger.debug(numeric_chapter)
        numeric_chapter.sort(key=float)

        non_numeric_chapter = [
            cap for cap in chapters if not cap.replace(".", "").isdigit()
        ]
        logger.debug("All non numeric chapters:")
        logger.debug(non_numeric_chapter)
        non_numeric_chapter.sort()

        all_chapters = []
        if numeric_chapter:
            all_chapters += numeric_chapter

        if non_numeric_chapter:
            all_chapters += non_numeric_chapter

        logger.debug(all_chapters)

        return all_chapters

    def find_chapter_pages(self, manga: Manga, chapter: str) -> list[str]:
        search = "/".join(
            [self.base_url, self.manga_chapter_path, manga.manga_id, chapter]
        )

        request_result = self.perform_request_html(search)
        soup = BeautifulSoup(request_result, features="html.parser")

        imgs = soup.find("div", {"id": "slider"}).findAll("img")
        pages = [p["src"] for p in imgs]

        logger.debug(pages)

        return pages
