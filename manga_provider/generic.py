import abc
import http.client
import logging
import multiprocessing
import os
import shutil
import typing

import requests
import tqdm

from util.manga import Manga
from util.utils import dynamic_pad

# Fix issue when downloading a lot of chapters
http.client._MAXHEADERS = 100000
logger = logging.getLogger("manga_downloader.manga_provider")


class DownloadIssue(Exception):
    pass


class MangaProvider(abc.ABC):
    def __init__(self, base_url: str, find_path: str, manga_path: str, manga_chapter_path: str) -> None:
        """
        Initialize the MangaProvider class
        Args:
            base_url (string): Url to download [Mandatory].
        Args:
            find_path (string): -> find location for dumping payload [default = "./downloads"]
        Args:
            manga_path (string): -> Storage location for dumping payload
        Args:
            manga_chapter_path (string): -> Specify the chapter path
        """
        self.base_url = base_url
        self.find_path = find_path
        self.manga_path = manga_path
        self.manga_chapter_path = manga_chapter_path

    def perform_request(self, url: str) -> requests.Response:
        """
        Method to perform request to the url and dump the response to its downstream
        Args:
            url (string): Url to download [Mandatory].
        """
        logger.debug(f"Sending request to {url}")
        response = requests.get(url, headers = self.get_headers())

        logger.debug("Request result:")
        logger.debug(response)
        return response

    @abc.abstractclassmethod
    def get_headers(self) -> dict:
        return {}

    # @abc.abstractclassmethod
    # def download_manga(self):
    #     pass

    @abc.abstractclassmethod
    def download_chapter(self, manga: Manga, manga_chapter: str) -> tuple[str, list[str]]:
        pass

    def download_all_images(self, uri_list: list[str], save_path: str) -> list[str]:
        """
        Method to download all the image files from the response.
        Args:
            uri_list (string): Url to download [Mandatory].
        Args:
            save_path (string): path to save the file.
        """
        with multiprocessing.Pool() as pool:
            inputs = list(
                zip(
                    uri_list,
                    [save_path] * len(uri_list),
                    [dynamic_pad(len(uri_list), num) for num in range(len(uri_list))],
                )
            )
            results = list(
                tqdm.tqdm(
                    pool.imap(self._multiproc_intermediary_to_download_image, inputs),
                    total = len(inputs),
                    unit = "Image",
                )
            )

        return results

    def _multiproc_intermediary_to_download_image(self, params: tuple):
        return self.download_image(params[0], params[1], params[2])

    def download_image(self, uri: str, save_path: str, file_name: str) -> str:
        """
        Method to download the image files from the response.
        Args:
            uri (string): Url to download [Mandatory].
        Args:
            save_path (string): path to save the file.
        Args:
            file_name (string): specify the name of the image file.
        """
        file_format = uri.split(".")[-1]
        file_name = f"{file_name}.{file_format}"
        file_path = os.path.join(save_path, file_name)

        os.makedirs(save_path, exist_ok = True)

        logging.debug(f"Downloading {uri}")
        r = requests.get(uri, headers = self.get_headers(), stream = True)

        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(file_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)

            # Logging twice? but there is a single handler
            logger.debug(f"Image successfully downloaded: {file_path}")
        else:
            raise DownloadIssue(f"Couldn't retrieve {uri}")

        return file_path

    @abc.abstractclassmethod
    def find_mangas(self, manga_name: str) -> typing.Iterable[dict]:
        pass

    @abc.abstractclassmethod
    def find_manga_chapters(self, manga: Manga):
        pass
