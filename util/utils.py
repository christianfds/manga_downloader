import shutil

from termcolor import colored


class FormatText:
    @staticmethod
    def title(text: str) -> str:
        """
        Static method to initiate the manga title.
        Args:
            text (string): Specify the title of the manga.
        """
        return colored(text=text, color="red", attrs=["bold"])

    @staticmethod
    def description(text: str) -> str:
        """
        Static method to initiate the manga description.
        Args:
            text (string): Specify the description of the manga.
        """
        return colored(text=text, color="white", attrs=["dark"])

    @staticmethod
    def option(text: str) -> str:
        """
        Static method to initiate the manga option.
        Args:
            text (string): Specify the option of the manga.
        """
        return colored(text=text, color="magenta")


def dynamic_pad(list_len: int, number: int) -> str:
    """
    Method to initiate the dynamic padding.
    Args:
        list_len (int): Specify the pad length.
    Args:
        number (int): Specify the count of the pad.
    """
    max_size = len(str(list_len))
    int_format = f":0{max_size}d"

    return ("".join(["{", int_format, "}"])).format(number)


def clear_tmp():
    """
       Method to prune the unwanted files.
       """
    shutil.rmtree("./.tmp", ignore_errors=True)
