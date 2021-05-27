from termcolor import colored


class FormatText():

    @staticmethod
    def title(text: str) -> str:
        return colored(text=text, color='red', attrs=['bold'])

    @staticmethod
    def description(text: str) -> str:
        return colored(text=text, color='white', attrs=['dark'])
