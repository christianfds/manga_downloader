import typing

from util.utils import FormatText


class Manga:
    def __init__(
            self, title: str, link: str, description: str = "", alternative_title: typing.Union[list[str], str] = "", manga_id: str = "", ) -> None:
        """
        Initialize the Manga class
        Args:
            title (string): specify the manga title.
        Args:
            link (string): -> specify the manga link to be downloaded.
        Args:
            description (string): -> specify the manga description to be added.
        Args:
            alternative_title (string): -> specify the alternate name for the manga.
        Args:
            manga_id (string): -> mention the manga id.
        """
        self.title = title
        self.link = link
        self.description = description

        if isinstance(alternative_title, list):
            self.alternative_title = alternative_title
        else:
            self.alternative_title = [
                title for title in alternative_title.split(",") if title
            ]

        self.manga_id = manga_id

    def show(self):
        """
        Method to view the title and description of the manga.
        """
        print(FormatText.title(self.title))
        if self.alternative_title:
            print(FormatText.description(", ".join(self.alternative_title)))
        print(FormatText.description(self.description))
