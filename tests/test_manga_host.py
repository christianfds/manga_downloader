from unittest.mock import patch

import pytest

from manga_provider.mangahost import MangaHost
from util.manga import Manga


class TestMangaHost:
    provider = MangaHost()

    @pytest.fixture
    def test_html_content(self) -> bytes:
        with open("tests/test_site.html") as test_file:
            yield test_file.read().encode()

    def test_manga_host(self, test_html_content):
        with patch("requests.get") as response_mock:
            response_mock.return_value.content = test_html_content
            for manga in self.provider.find_mangas("some_name"):
                assert isinstance(manga, Manga)
