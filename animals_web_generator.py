import sys
from web.html_manager import HtmlData
from data.json_manager import DataInfo


class InputError(Exception):
    """raise when user input is invalid"""
    pass


class FileMatchError(Exception):
    """raise when the content of a destination file does not match expected content"""
    pass


def get_filter() -> str:
    options = DataInfo().filter_options
    while True:
        try:
            skin = input("\nEnter number of the filter you would like to use.\n"
                         "Leave this empty, if you want all animals displayed.\n\nFilter: ")

            if skin == "4":
                sys.exit("\nGoodbye!")

            if not (skin in options or skin == ""):
                raise InputError(f"\n{skin} is not a valid option. Try again.")
            break

        except Exception as e:
            print(e)
    return options.get(skin, "")


def main() -> None:
    print("Welcome to My Animal Repository\n\nFilter options:")
    print(DataInfo().filter_menu)

    skin = get_filter()

    print(f"\nCreating website with filter: {skin}\n" if skin else f"\nCreating website without filter\n")

    try:
        success = HtmlData(skin=skin).web_generator

        if not success:
            raise FileMatchError("Something went wrong while saving")

        print("File saved successfully")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
