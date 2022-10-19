from unittest.mock import patch

import pytest

from manga_downloader import (
    SECTION_RANGE_ERROR_MSG,
    chose_manga,
    parse_chapter_selection,
)
from manga_provider.mangahost import MangaHost
from util.manga import Manga


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


class TestChoseManga:
    title = "some title"
    link = "some link"
    manga_id = "some-id"

    @patch.object(MangaHost, "find_mangas", autospec=True)
    def test_chose_manga(self, find_mangas):
        manga_tuple = tuple(
            [
                Manga(title=self.title, link=self.link, manga_id=self.manga_id),
                Manga(title="a", link="b", manga_id="c"),
            ]
        )
        find_mangas.return_value = manga_tuple
        provider = MangaHost()
        assert provider.find_mangas("Some Manga") == manga_tuple

        with patch("builtins.input", return_value=self.manga_id):
            chosen_manga = chose_manga(MangaHost(), "Some Manga", 1)
        assert chosen_manga == manga_tuple[0]
