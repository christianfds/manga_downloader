import pytest
from requests import exceptions

from manga_downloader import SECTION_RANGE_ERROR_MSG, parse_chapter_selection
from manga_provider.mangahost import MangaHost


class TestParseChapterSelection:
    @pytest.mark.parametrize(
        "selection, assert_chapters",
        [("1,2", [1, 2]), ("1", [1]), ("2-3,7-8", [2, 3, 7, 8])],
    )
    def test_parse_chapter_selection_on_integer_input(self, selection, assert_chapters):
        chapters = parse_chapter_selection(selection)
        assert chapters == assert_chapters

    def test_parse_chapter_selection_on_blank_string(self):
        with pytest.raises(TypeError) as type_error:
            parse_chapter_selection("")
        assert str(type_error.value) == SECTION_RANGE_ERROR_MSG


class TestGeneric:
    def test_connection_timeout(self):
        provider = MangaHost()
        with pytest.raises(exceptions.ConnectionError) as connection_error:
            provider.perform_request(url="http://example.com:81")
        assert connection_error.value
