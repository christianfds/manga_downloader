import abc
import requests
import logging

import typing
from util.manga import Manga

logger = logging.getLogger('manga_downloader.manga_provider.generic')


class MangaProvider(abc.ABC):

    def __init__(self, base_url: str, find_path: str, manga_chapters_path: str) -> None:
        self.base_url = base_url
        self.find_path = find_path
        self.manga_chapters_path = manga_chapters_path

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

    @abc.abstractclassmethod
    def find_manga_chapters(self, manga: Manga):
        pass
