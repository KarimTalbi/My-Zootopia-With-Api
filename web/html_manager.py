import os
import sys
from data.json_manager import DatabaseInfo

TEMPLATE_PATH = os.path.join("web", "animals_template.html")
DESTINATION_PATH = os.path.join("web", "animals.html")
REPLACE_STRING = f"{" " * 12}__REPLACE_ANIMALS_INFO__"
ENCODER = "utf-8"


class LoadHtml:
    """
    Loads HTML-Template File content
    Parent class of HtmlDest
    """

    def __init__(self, file_path: str = TEMPLATE_PATH):
        self.file_path = file_path
        self.template = self.load_html

    @property
    def load_html(self) -> str:
        """Returns the content of the HTML, terminates the program if the HTML doesn't exist"""
        if not os.path.exists(self.file_path):
            sys.exit(f"File: {self.file_path} could not be loaded. Exiting program...")  # TODO

        with open(self.file_path, "r", encoding=ENCODER) as f:
            return f.read()


class SaveHtml(LoadHtml):
    """Saves data to new HTML File"""

    def __init__(self, file_path: str = TEMPLATE_PATH, dest_path: str = DESTINATION_PATH):
        super().__init__(file_path)
        self.destination = dest_path

    def save_html(self, content: str) -> None:
        """Saves data to an HTML file, creates a file if it doesn't exist"""
        with open(self.destination, "w", encoding=ENCODER) as f:
            f.write(content)


class FormatHtml:
    """Formats strings into HTML Format"""

    def __init__(self, animal: dict[str, str]):
        self.animal = animal
        self.indent = " " * 4

    @property
    def top(self) -> str:
        return (
            f'{self.indent * 3}<li class="cards__item">\n'
            f'{self.indent * 4}<div class="card__title">{self.animal["Name"]}</div>\n'
            f'{self.indent * 4}<div class="card__text">\n'
            f'{self.indent * 5}<ul>\n'
        )

    @property
    def middle(self) -> str:
        return "".join(
            [f'{self.indent * 6}<li><strong>{key}:</strong> {value}</li>\n'
             for key, value in self.animal.items() if key != "Name" and value]
        )

    @property
    def bottom(self) -> str:
        return (
            f'{self.indent * 5}</ul>\n'
            f'{self.indent * 4}</div>\n'
            f'{self.indent * 3}</li>\n\n'
        )

    @property
    def serialize(self) -> str:
        return self.top + self.middle + self.bottom


class HtmlData(SaveHtml):

    def __init__(self, file_path: str = TEMPLATE_PATH, dest_path: str = DESTINATION_PATH, to_replace: str = REPLACE_STRING):
        super().__init__(file_path, dest_path)
        self.form = FormatHtml
        self.info = DatabaseInfo
        self.to_replace = to_replace

    @property
    def animal_data(self) -> str:
        """Filters AnimalData for Name, Diet, Location, Type and returns as a list"""
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

            output += self.form(animal).serialize
        return output

    @property
    def encoding(self) -> str:
        return self.template.replace('<head>', f'<head>\n{" " * 8}<meta charset="UTF-8">')

    @property
    def replacer(self) -> str:
        return self.encoding.replace(self.to_replace, self.animal_data)

    def web_generator(self) -> None:
        self.save_html(self.replacer)
