import shutil

from termcolor import colored


class FormatText:
    @staticmethod
    def id(text: str) -> str:
        return colored(text=text, color="cyan", attrs=["bold"])

    @staticmethod
    def title(text: str) -> str:
        return colored(text=text, color="red", attrs=["bold"])

    @staticmethod
    def description(text: str) -> str:
        return colored(text=text, color="white", attrs=["dark"])

    @staticmethod
    def option(text: str) -> str:
        return colored(text=text, color="magenta")


def dynamic_pad(list_len: int, number: int) -> str:
    max_size = len(str(list_len))
    int_format = f":0{max_size}d"

    return ("".join(["{", int_format, "}"])).format(number)


def clear_tmp():
    shutil.rmtree("./.tmp", ignore_errors=True)
