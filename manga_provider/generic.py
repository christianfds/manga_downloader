import abc
import requests
import logging

import typing

logger = logging.getLogger('manga_downloader.manga_provider.generic')


class MangaProvider(abc.ABC):

    def __init__(self, base_url: str, find_path: str, search_regex: str, chapter_link_regex: str, img_link_regex: str) -> None:
        self.base_url = base_url
        self.find_path = find_path
        self.search_link_regex = search_regex
        self.chapter_link_regex = chapter_link_regex
        self.img_link_regex = img_link_regex

    def perform_request(self, url: str) -> requests.Response:
        logger.debug(f'Sending request to {url}')
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
        })

        logger.debug(f'Request result:')
        logger.debug(response)
        logger.debug(response.content)
        return response

    # @abc.abstractclassmethod
    # def download_manga(self):
    #     pass

    # @abc.abstractclassmethod
    # def download_chapter(self):
    #     pass

    # @abc.abstractclassmethod
    # def download_image(self):
    #     pass

    @abc.abstractclassmethod
    def find_mangas(self, manga_name: str) -> typing.Iterable[dict]:
        pass

    # @abc.abstractclassmethod
    # def find_manga_chapters(self):
    #     pass
