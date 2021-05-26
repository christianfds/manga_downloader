import re
import logging
import typing

from bs4 import BeautifulSoup
from manga_provider.generic import MangaProvider

logger = logging.getLogger('manga_downloader.manga_provider.mangahost')


SETTINGS = {
    'base_url': 'https://mangahost4.com',
    'find_path': 'find',
    'search_regex': re.compile('entry-title">\\s*<a\\s*href="(.*)?"\\s*title="(.*)"'),
    'chapter_link_regex': re.compile('capitulo.*?Ler\\s+Online\\s+-\\s+(.*?)[\'"]\\s+href=[\'"](.*?)[\'"]'),
    'img_link_regex': re.compile('img_\\d+[\'"]\\s+src=[\'"](.*?)[\'"]')
}


class MangaHost(MangaProvider):
    def __init__(self) -> None:
        super().__init__(**SETTINGS)

    def encode_manga_name(self, manga_name: str) -> str:
        return manga_name.replace(' ', '+')

    def find_mangas(self, manga_name: str) -> typing.Iterable[dict]:
        manga_name = self.encode_manga_name(manga_name)
        search = '/'.join([self.base_url, self.find_path, manga_name])

        request_result = self.perform_request(search)
        soup = BeautifulSoup(request_result.content, features='html.parser')

        table = soup.find('table')

        counter = 0
        for row in table.findAll('td'):
            if counter % 2:
                manga = {
                    'title': row.find('a')['title'],
                    'alternative-title': [title for title in row.find('span').text.split(',') if title],
                    'description': row.find('div', {'class': 'entry-content'}).text.strip().replace('\r\n', ' '),
                    'link': row.find('a')['href']
                }
                logger.debug(manga)
                yield manga

            counter = counter + 1
