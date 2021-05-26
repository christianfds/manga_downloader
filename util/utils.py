from termcolor import colored


# TODO manga class?
def format_manga(manga: dict):
    title = colored(manga['title'], color='red', attrs=['bold'])
    alternative_title = colored('Titulo alternativo: ' + ', '.join(manga['alternative-title']), color='white', attrs=['dark']) if len(manga['alternative-title']) > 0 else None
    description = colored('Descrição: ' + manga['description'], color='white', attrs=['dark'])

    print(title)
    if alternative_title:
        print(alternative_title)
    print(description)
