"""
Manages the loading of HTML templates, the filtering and formatting of animal data
into HTML cards, and the saving and verification of the final web page.
"""
import os
from data.json_manager import DataInfo

FILE = os.path.join("web", "animals_template.html")
DEST = os.path.join("web", "animals.html")
ENCODE = "utf-8"


class FileError(Exception):
    """Custom exception raised when there is an error while loading a file."""
    pass


class HtmlLoad:
    """
    Base class responsible for loading content from both the source HTML template
    and the final destination HTML file for verification.
    """

    def __init__(self, file: str = FILE, dest: str = DEST):
        """
        Initializes HtmlLoad with file paths and loads the template content.

        :param file: The path to the HTML template file. Defaults to FILE.
        :param dest: The path to the destination HTML file. Defaults to DEST.
        """
        self.file = file
        self.dest = dest
        self._template: str | None = None

    @property
    def load_html(self) -> str:
        """
        Reads and returns the content of the HTML template file.

        The content is loaded **lazily**—it's read from the disk only on the first call
        and then stored in `self._template` for later calls.

        :raises FileError: If the file at `self.file` is not found.
        :return: The content of the HTML template as a single string.
        """
        if self._template is not None:
            return self._template

        if not os.path.exists(self.file):
            raise FileError(f"Error: The required HTML file was not found at path: {self.file}")

        with open(self.file, "r", encoding=ENCODE) as f:
            self._template = f.read()
            return self._template


class HtmlSave(HtmlLoad):
    """
    Extends HtmlLoad to provide functionality for saving generated HTML content
    to the destination file.
    """

    def __init__(self, file: str = FILE, dest: str = DEST):
        """
        Initializes HtmlSave, setting the destination path for saving.

        :param file: The path to the HTML template file. Defaults to FILE.
        :param dest: The path where the final HTML file will be saved. Defaults to DEST.
        """
        super().__init__(file, dest)
        self.dest_path: str = dest

    def save_html(self, content: str) -> None:
        """
        Writes the provided string content to the destination HTML file.

        Creates the file if it does not exist or overwrites it if it does.

        :param content: The complete HTML content string to be saved.
        """
        with open(self.dest_path, "w", encoding=ENCODE) as f:
            f.write(content)


class HtmlForm:
    """Handles the formatting of a single animal's data into a repeatable HTML list item (card) string."""

    def __init__(self, animal: dict[str, str]):
        """
        Initializes HtmlForm with a dictionary containing the animal's attributes.

        :param animal: A dictionary of animal attributes, where the 'Name' key is used for the card title.
        """
        self.animal: dict[str, str] = animal

    @property
    def top(self) -> str:
        """
        Generates the opening HTML structure for an animal card, including
        the list item (`li`), card title (`.card__title`), and the opening tags for the detail list (`ul.cards__list`).

        :return: A formatted string containing the opening HTML tags.
        """
        return (
            f'{" " * 12}<li class="cards__item">\n'
            f'{" " * 16}<div class="card__title">{self.animal["Name"]}</div>\n'
            f'{" " * 16}<div class="card__text">\n'
            f'{" " * 20}<ul class="cards__list">\n'
        )

    @property
    def middle(self) -> str:
        """
        Generates the middle section containing the animal's characteristic list items.

        It iterates over the animal dictionary and creates `<li>` tags for each key/value pair,
        excluding the 'Name' key and any values that are empty.

        :return: A formatted string of `<li>` tags containing the animal details.
        """
        return "".join(
            [f'{" " * 24}<li><strong>{key}:</strong> {value}</li>\n'
             for key, value in self.animal.items() if key != "Name" and value]
        )

    @property
    def bottom(self) -> str:
        """
        Generates the closing HTML structure for an animal card.

        :return: A formatted string containing the closing HTML tags (`</ul>`, `</div>`, `</li>`).
        """
        return (
            f'{" " * 20}</ul>\n'
            f'{" " * 16}</div>\n'
            f'{" " * 12}</li>\n\n'
        )

    @property
    def serialize(self) -> str:
        """
        Concatenates the top, middle, and bottom parts to form the complete HTML
        string for a single animal card.

        :return: The complete, formatted HTML string for one animal card.
        """
        return self.top + self.middle + self.bottom


class HtmlData(HtmlSave):
    """
    The main class for orchestrating the web page generation process.

    It handles filtering data, formatting it, injecting necessary styles and encoding
    into the template, and saving the final output file.
    """

    def __init__(self, file: str = FILE, dest: str = DEST, skin: str = ""):
        """
        Initializes HtmlData.

        :param file: The path to the HTML template file.
        :param dest: The path where the final HTML file will be saved.
        :param skin: The filter string (e.g., 'Fur', 'Hair') to apply to the animals. Defaults to an empty string (no filter).
        """
        super().__init__(file, dest)
        self.form = HtmlForm
        self.info = DataInfo
        self.skin = skin

    @property
    def animal_data(self) -> str:
        """
        Retrieves all animal data, filters it based on `self.skin`, and formats the
        matching animals into concatenated HTML card strings.

        :return: A single string containing the concatenated HTML cards for the filtered animals.
        """
        output = ""
        for i in range(self.info().count):
            animal: dict[str, str] = {
                "Name": self.info(i).name,
                "Scientific Name": self.info(i).scientific_name,
                "Diet": self.info(i).diet,
                "Locations": self.info(i).locations,
                "Type": self.info(i).type,
                "Color": self.info(i).color,
                "Skin Type": self.info(i).skin_type,
            }

            # If the skin type matches filter OR no filter is set (self.skin is empty)
            if animal.get("Skin Type") == self.skin or not self.skin:
                output += self.form(animal).serialize
        return output

    @property
    def list_style(self) -> str:
        """
        Injects custom CSS rules for list styling (`.cards__list`) into the 
        template's existing `<style>` block.

        :return: The template string with the new CSS rules added.
        """
        return self.load_html.replace("</style>", '''
        .cards__list {
          list-style-type: disc;
          list-style-position: inside;
          margin: 0;
          padding: 20px 0 0 0;
        }
        </style>''')

    @property
    def encoding(self) -> str:
        """
        Inserts the UTF-8 charset meta-tag into the `<head>` section of the
        style-modified template (`self.list_style`).

        :return: The template string with a charset meta-tag is added.
        """
        return self.list_style.replace('<head>', '''<head>
        <meta charset="UTF-8">''')

    @property
    def replacer(self) -> str:
        """
        Replaces the `__REPLACE_ANIMALS_INFO__` placeholder in the encoded template
        with the dynamically generated HTML card strings (`self.animal_data`).

        :return: The final complete HTML string ready to be saved.
        """
        return self.encoding.replace(f"{" " * 12}__REPLACE_ANIMALS_INFO__", self.animal_data)

    def web_generator_empty(self) -> None:
        new_html = self.load_html.replace(f"{" " * 12}__REPLACE_ANIMALS_INFO__", f"<h2>The animal doesn't exist.</h2>")
        self.save_html(new_html)

    def web_generator(self) -> None:
        """
        Executes the full web page generation and verification process:
        1. Generates the final HTML content using `self.replacer`.
        2. Saves the new content to the destination file using `self.save_html()`.

        :raises FileError: If an error occurs while attempting to load the saved destination file.
        :return: **True** if the saved content exactly matches the newly generated content, indicating a successful save; otherwise, **False**.
        """
        new_html = self.replacer
        self.save_html(new_html)
