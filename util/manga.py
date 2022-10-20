import typing

from util.utils import FormatText


class Manga:
    def __init__(
        self,
        title: str,
        link: str,
        description: str = "",
        alternative_title: typing.Union[list[str], str] = "",
        manga_id: str = "",
    ) -> None:
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
        print(f"{FormatText.id(self.manga_id)}: {FormatText.title(self.title)}")
        if self.alternative_title:
            print(FormatText.description(", ".join(self.alternative_title)))
        print(FormatText.description(self.description))
