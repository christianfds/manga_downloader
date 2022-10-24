import os


class SearchRender:
    search_query = None
    query_length = 0
    ITEM_PER_PAGE = 10

    def __init__(self, items):
        self.search_query = list(items)
        self.query_length = len(self.search_query)

    def select(self):
        selection = None
        page = 1
        page_item_start = 0
        page_item_end = self.ITEM_PER_PAGE * page
        print("Getting " + str(len(self.search_query)) + " Search Result")
        while selection != "Q":
            os.system("clear")
            print("============ MANGA DOWNLOADER ============")
            print(
                "Showing Result {}-{} of {} ".format(
                    page_item_start + 1, page_item_end, self.query_length
                )
            )
            print("------------------------------------------")
            for index, item in enumerate(self.search_query):
                if page_item_start <= index <= page_item_end - 1:
                    item.show_compact_with_index(index)

            print("------------------------------------------")
            print("Navigate: [P] Previous Page         [N] Next Page")
            print("Action  : [NUM] Download Selected   [Q] Quit")
            print("------------------------------------------")
            selection = input("Select Option : ").upper()
            if selection == "N":
                if page_item_end < self.query_length:
                    page_item_start += self.ITEM_PER_PAGE
                    page_item_end += self.ITEM_PER_PAGE
                else:
                    input(
                        "This is the Last Page!!\nPress [ENTER] to select other option"
                    )
            if selection == "P":
                if page_item_start > 0:
                    page_item_start -= self.ITEM_PER_PAGE
                    page_item_end -= self.ITEM_PER_PAGE
                else:
                    input(
                        "This is the First Page!!\nPress [ENTER] to select other option"
                    )
            elif selection.isdigit():
                selection = int(selection) - 1
                os.system("clear")
                print("============ MANGA DETAILS ============")
                self.search_query[selection].show()
                print("=======================================\n")

                is_proceed = input(
                    "Are you sure want to download this Manga? [Y/N]:"
                ).upper()
                if is_proceed == "Y":
                    return self.search_query[selection]

        print("Exiting Manga Downloader.....")
        quit(0)
