"""
The main entry point for the Zootopia web page generator application.

This script prompts the user for a skin type filter and then generates
the final 'animals.html' file using the selected filter (or no filter)
based on the animal data.
"""
import sys
from web.html_manager import HtmlData
from data.json_manager import DataInfo


class InputError(Exception):
    """Custom exception raised when user input from the console is invalid."""
    pass


class FileMatchError(Exception):
    """
    Custom exception raised when the content of the destination HTML file
    does not match the expected generated content, indicating a save error.
    """
    pass


def get_filter() -> str:
    """
    Prompts the user to select a skin type filter from the available options.

    Handles user input validation and provides an option to exit the program.
    The function runs in a loop until valid input is provided or the user exits.

    :raises InputError: If the input is not one of the displayed numbers or empty.
    :return: The selected skin type string (e.g., 'Fur', 'Scales'), or an empty
             string if the user chooses to display all animals.
    """
    options = DataInfo().filter_options
    while True:
        try:
            skin = input("\nEnter number of the filter you would like to use.\n"
                         "Leave this empty, if you want all animals displayed.\n\nFilter: ").strip()

            if skin == "4":
                sys.exit("\nGoodbye!")

            if not (skin in options or skin == ""):
                raise InputError(f"\n{skin} is not a valid option. Try again.")
            break

        except Exception as e:
            print(e)
    return options.get(skin, "")


def main() -> None:
    """
    The main execution function of the program.

    It displays the filter menu, retrieves the user's filter choice,
    initiates the HTML generation using HtmlData, and reports the outcome.
    """
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
